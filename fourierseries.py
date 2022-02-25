# Code to draw cool things using the math of complex Fourier-series
# This is an updated version of the code from youtuber Theorem of Beethoven as seen here:
# Theorem of Beethoven link:    https://www.youtube.com/watch?v=2tTshwWTEic
# Adapted from CairoManim to ManimCE
# Inspired by brilliant math youtuber 3Blue1Brown, creator of the Manim Python library:
# 3lue1Brown link:              https://www.youtube.com/watch?v=r6sGWTCMz2k

from manim import *
import numpy as np
# import timeit

# config.use_opengl_renderer = True

# Abstract scene
class FourierScene(ZoomedScene):
    def __init__(self):
        super().__init__()
        self.n_vectors = 100
        self.vector_config = {
            "buff": 0,
            "max_tip_length_to_length_ratio": 0.25,
            "tip_length": 0.15,
            "max_stroke_width_to_length_ratio": 10,
            "stroke_width": 1.4
        }
        self.circle_config = {
            "stroke_width": 1,
            "stroke_opacity": 0.3,
            "color": WHITE
        }
        self.cycle_time = 3 # Seconds
        self.parametric_func_step = 1e-4    
        self.drawn_path_stroke_width = 5
        self.interpolate_config = [0, 1]    # Width of drawn path at end and beginning respectively
        self.path_n_samples = 1e4
        self.freqs = list(range(-self.n_vectors // 2, self.n_vectors // 2 + 1, 1))
        self.freqs.sort(key=abs)            # NOTE moved freqs to be property of scene, so need only be calculated once, 

    def setup(self):                        # Manim calls setup, unsure why valuetrackers kept here, is it so able to call on from methods within class?
        super().setup()
        self.vector_clock = ValueTracker()
        self.slow_factor_tracker = ValueTracker(0)
        self.add(self.vector_clock)

    def start_vector_clock(self):           # This updates vector_clock to follow the add_updater parameter dt
        self.vector_clock.add_updater(
            lambda t, dt: t.increment_value(dt * self.slow_factor_tracker.get_value() / self.cycle_time)
        )

    def stop_vector_clock(self):
        self.vector_clock.remove_updater(self.start_vector_clock)

    def get_fourier_coefs(self, path):
        dt = 1 / self.path_n_samples
        t_range = np.arange(0, 1, dt)
        # Sample points
        points = np.array([
            path.point_from_proportion(t)
            for t in t_range
        ])
        complex_points = points[:, 0] + 1j * points[:, 1]
        coefficients = [
            np.sum(np.array([
                c_point * np.exp(-TAU * 1j * freq * t) * dt
                for t, c_point in zip(t_range, complex_points)
                ]))
            for freq in self.freqs
        ]
        return coefficients

    def get_fourier_vectors(self, path):
        coefficients = self.get_fourier_coefs(path)
        vectors = VGroup()
        v_is_first_vector = True
        for coef, freq in zip(coefficients,self.freqs):
            v = Vector([np.real(coef), np.imag(coef)], **self.vector_config)
            # Center function to position at tip of last vector
            if v_is_first_vector:
                center_func = VectorizedPoint(ORIGIN).get_location
                v_is_first_vector = False
            else:
                center_func = last_v.get_end
            v.center_func = center_func
            last_v = v
            v.freq = freq
            v.coef = coef
            v.phase = np.angle(coef)
            v.shift(v.center_func()-v.get_start())
            v.set_angle(v.phase)
            vectors.add(v)
        return vectors

    def update_vectors(self, vectors):
            for v in vectors:
                time = self.vector_clock.get_value()
                v.shift(v.center_func()-v.get_start())
                v.set_angle(v.phase + time * v.freq * TAU)  # NOTE Rotate() did not work here for unknown reason, probably related to how manin handles updaters
              
    def get_circles(self, vectors):                         # TODO Add circle config as argument
        circles = VGroup()
        for v in vectors:
            c = Circle(radius = v.get_length(), **self.circle_config)
            c.center_func = v.get_start
            c.move_to(c.center_func())
            circles.add(c)
        return circles

    def update_circles(self, circles):
        for c in circles:
            c.move_to(c.center_func())
            
    def get_drawn_path(self, vectors):    # TODO Find out application of None, is for placeholder, may be how keyword argument default is set

        def fourier_series_func(t):
            fss = np.sum(np.array([
                v.coef * np.exp(TAU * 1j * v.freq * t)
                for v in vectors
            ]))
            real_fss = np.array([np.real(fss), np.imag(fss), 0])
            return real_fss
        
        t_range = np.array([0, 1, self.parametric_func_step])
        vector_sum_path = ParametricFunction(fourier_series_func, t_range = t_range)
        broken_path = CurvesAsSubmobjects(vector_sum_path)
        broken_path.stroke_width = 0
        broken_path.start_width = self.interpolate_config[0]
        broken_path.end_width = self.interpolate_config[1]
        return broken_path

    def update_path(self, broken_path):
        alpha = self.vector_clock.get_value()
        n_curves = len(broken_path)
        alpha_range = np.linspace(0, 1, n_curves)
        for a, subpath in zip(alpha_range, broken_path):
            b = (alpha - a)
            if b < 0:
                width = 0
            else:
                width = self.drawn_path_stroke_width * interpolate(broken_path.start_width, broken_path.end_width, (1 - (b % 1)))   # % is b modulo 1, returns the value of b wrapped around 1, so that path width resets after one cycle
            subpath.set_stroke(width=width)

# FOURIER ANIMATION TEST SCENE
class FourierAnimation(FourierScene):
    def __init__(self):
        super().__init__()
        self.fourier_symbol_config = {
            "stroke_width": 1,
            "fill_opacity": 1,
            "height": 4,
        }
        self.vector_config = {
            "buff": 0,
            "max_tip_length_to_length_ratio": 0.25,
            "tip_length": 0.15,
            "max_stroke_width_to_length_ratio": 10,
            "stroke_width": 1.4
        }
        self.circle_config = {
            "stroke_width": 1,
            "stroke_opacity": 0.3,
            "color": WHITE
        }
        self.cycle_time = 5                 
        self.drawn_path_stroke_width = 3
    def construct(self):

        # Symbols to draw
        symbol1 = Tex("m", **self.fourier_symbol_config).set_color(RED)
        symbol2 = Tex("e", **self.fourier_symbol_config).set_color(BLUE)
        group = VGroup(symbol1, symbol2).arrange(RIGHT)

        # Get paths
        path1 = symbol1.family_members_with_points()[0]     # IDEA to only input symbol, put this part in superclass 
        path2 = symbol2.family_members_with_points()[0]

        # Fourier series for symbol1
        vectors1 = self.get_fourier_vectors(path1)
        circles1 = self.get_circles(vectors1)
        drawn_path1 = self.get_drawn_path(vectors1).set_color(RED)

        # Fourier series for symbol2
        vectors2 = self.get_fourier_vectors(path2)
        circles2 = self.get_circles(vectors2)
        drawn_path2 = self.get_drawn_path(vectors2).set_color(BLUE)

        # Text definition
        text = Tex("hire", fill_opacity = 1, height = 3)
        text.next_to(group, LEFT*1.4)

        all_mobs = VGroup(group, text)

        # Camera updater
        last_vector = vectors1[-1]

        def follow_end_vector(camera): 
            camera.move_to(last_vector.get_end())

        # Scene start
        self.wait(1)
        self.play(
            *[
                GrowArrow(arrow)
                for vector_group in [vectors1, vectors2]
                for arrow in vector_group
            ],
            *[
                Create(circle)
                for circle_group in [circles1, circles2]
                for circle in circle_group
            ],
            run_time=2.5,
        )
        # Not sure why but need to add circles and vectors here or updater will not work
        self.add( 
            vectors1,
            circles1,
            drawn_path1.set_stroke(width = 0),
            vectors2,
            circles2,
            drawn_path2.set_stroke(width = 0),
        )

        # Camera move
        self.play(self.camera.frame.animate.scale(0.3).move_to(last_vector.get_end()), run_time = 2)

        # Add updaters and start vector clock
        self.camera.frame.add_updater(follow_end_vector)
        vectors1.add_updater(self.update_vectors)
        circles1.add_updater(self.update_circles)
        vectors2.add_updater(self.update_vectors)
        circles2.add_updater(self.update_circles)
        drawn_path1.add_updater(self.update_path)
        drawn_path2.add_updater(self.update_path)
        self.start_vector_clock()

        self.play(self.slow_factor_tracker.animate.set_value(1), run_time = 0.5*self.cycle_time)
        self.wait(1 * self.cycle_time)

        # Move camera then write text
        self.camera.frame.remove_updater(follow_end_vector)
        self.play(
            self.camera.frame.animate.set_width(all_mobs.width*1.5).move_to(all_mobs.get_center()),
            Write(text),
            run_time = 1 * self.cycle_time,
        )
        self.wait(0.8*self.cycle_time)
        self.play(self.slow_factor_tracker.animate.set_value(0), run_time = 0.5*self.cycle_time)
        
        # Remove all updaters so can animate
        self.stop_vector_clock()
        drawn_path1.clear_updaters()
        drawn_path2.clear_updaters()
        vectors1.clear_updaters()
        vectors2.clear_updaters()
        circles1.clear_updaters()
        circles2.clear_updaters()

        self.play(
            *[
                Uncreate(vmobject)
                for vgroup in [vectors1, vectors2, circles1, circles2]
                for vmobject in vgroup
            ],
            FadeOut(drawn_path1, drawn_path2),
            FadeIn(symbol1, symbol2),
            run_time=2.5,
        )

        self.wait(3)