# Code to draw cool things using the math of complex Fourier-series
# This is an updated version of the code from youtuber Theorem of Beethoven as seen here:
# Theorem of Beethoven link:    https://www.youtube.com/watch?v=2tTshwWTEic
# Adapted from CairoManim to ManimCE
# Inspired by brilliant math youtuber 3Blue1Brown, creator of the Manim Python library:
# 3lue1Brown link:              https://www.youtube.com/watch?v=r6sGWTCMz2k


# TODO go through all comments

# QUESTION fråga Johan om jämförelse av hastighet och antal beräkningar
# ANSWER timeit och söka på python performance

# REALIZATION I think more clearly when I write my thoughts down.
# CONCLUSION fft is much faster relatively, but in absolute numbers it makes only a difference of about 0.1 seconds or so. On top of this, the coefficients would need to be resorted and cut off.
# NOTE fft coefficients are not sorted according by lowest frequency first, this must be done by hand

from manim import *
import numpy as np
import timeit

# config.use_opengl_renderer = True

# Abstract scene
class FourierScene(ZoomedScene):
    def __init__(self):
        super().__init__()
        self.n_vectors = 20
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
        self.cycle_time = 3                 
        self.parametric_func_step = 0.01    
        self.drawn_path_stroke_width = 3
        self.interpolate_config = [0, 1]    # Width of drawn path at end and beginning respectively
        self.n_samples = 1000               # This number will be rounded up to closest power of 2, for fft performance
        self.path_n_samples = 2**np.ceil( np.log(self.n_samples) / np.log(2) )
        # self.freqs = list(range(-self.n_vectors // 2, self.n_vectors // 2 + 1, 1))
        # self.freqs.sort(key=abs)                    # NOTE moved freqs to be property of scene, so need only be calculated once, 

    def setup(self):                                # Manim calls setup, unsure why valuetrackers kept here, is it so able to call on from methods within class?
        super().setup()
        self.vector_clock = ValueTracker(0)         # Consider use of this valuetracker
        self.add(self.vector_clock)

    def start_vector_clock(self):                     # ADD_VECTOR_CLOCK: adds updater to vector_clock, note vector_clock seems to not be added here but in setup
        self.vector_clock.add_updater(
            lambda t, dt: t.increment_value(dt / self.cycle_time)
            )

    def get_fourier_coefs(self, path):
        start = time.time()
        dt = 1 / self.path_n_samples
        ts = np.arange(0, 1, dt)

        # Sample points
        points = np.array([
            path.point_from_proportion(t)
            for t in ts
        ])
        complex_points = points[:, 0] + 1j * points[:, 1]
        print(len(complex_points))
        coefficients = np.fft.fft(complex_points, norm = "forward", axis = 1)
        # coefficients = np.fft.fftshift(coefficients_unshifted) # This is not the problem

        # coefficients = [
        #     np.array([
        #         np.exp(-TAU * 1j * freq * t) * cpoint
        #         for t, cpoint in zip(ts, complex_points)
        #     ]).sum() * dt for freq in self.freqs
        # ]
        end = time.time()
        print("---")
        freq = np.fft.fftfreq(complex_points.size)
        print("Frequencies:")
        print(str(round(freq, 4)))
        print("Number of coefficients: " + str(len(coefficients)))
        print("First three coefficients:")
        print([str(round(coefficients[k],4)) for k in range(0,3)])
        print("This run took:" + str(end - start) + "seconds")
        print("---")
       
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
                v.set_angle(v.phase + time * v.freq * TAU)  # NOTE that rotate() did not work here for unknown reason, probably related to how manin handles updaters
              
    def get_circles(self, vectors):         # TODO Add circle config as argument
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
            
    def get_drawn_path(self, vectors):    # set **kwargs to drawn_path_config, located in abstract scene or in actual scene? Also note to find out application of None, is for placeholder?
        # start = time.time()
        def fourier_series_func(t):
            fss = np.array([
                v.coef * np.exp(TAU * 1j * v.freq * t)
                for v in vectors
                ]).sum()
            real_fss = np.array([np.real(fss), np.imag(fss), 0])
            return real_fss
        
        t_range = np.array([0, 1, self.parametric_func_step])
        vector_sum_path = ParametricFunction(fourier_series_func, t_range = t_range)
        broken_path = CurvesAsSubmobjects(vector_sum_path)
        # broken_path.time = 0
        broken_path.stroke_width = 0
        broken_path.start_width = self.interpolate_config[0]
        broken_path.end_width = self.interpolate_config[1]
        # start, end = self.interpolate_config
        return broken_path

    def update_path(self, broken_path):  # This is add_updater argument dt, it tells manim the function will be executed every frame, else executed when mobject has changed
        alpha = self.vector_clock.get_value()
        n_curves = len(broken_path)
        for a, subpath in zip(np.linspace(0, 1, n_curves), broken_path):
            b = (alpha - a)
            if b < 0:
                width = 0
            else:
                width = self.drawn_path_stroke_width * interpolate(broken_path.start_width, broken_path.end_width, (1 - (b % 1)))   # % is b modulo 1, returns the value of b wrapped around 1
            subpath.set_stroke(width=width)
        # broken_path.time += dt

        # broken_path.add_updater(update_path)
        # end = time.time()
        # print("This run took:" + str(end - start) + "seconds")
        

# FOURIER ANIMATION TEST SCENE

class FourierAnimation(FourierScene):
    def __init__(self):
        super().__init__()
        self.fourier_symbol_config = {
            "stroke_width": 1,
            "fill_opacity": 0,
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
        symbol1 = Tex("m", **self.fourier_symbol_config)
        symbol2 = Tex("e", **self.fourier_symbol_config)
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
            drawn_path1,
            vectors2,
            circles2,
            drawn_path2,
        )

        vectors1.add_updater(self.update_vectors)
        circles1.add_updater(self.update_circles)
        vectors2.add_updater(self.update_vectors)
        circles2.add_updater(self.update_circles)
        drawn_path1.add_updater(self.update_path)
        drawn_path2.add_updater(self.update_path)

        self.start_vector_clock()

        self.wait(1 * self.cycle_time)

        # Move camera then write text
        self.play(
            self.camera.frame.animate.set_width(all_mobs.width*1.5).move_to(all_mobs.get_center()),
            run_time = 2
        )
        self.wait()
        self.play(Write(text))
        self.wait(1 * self.cycle_time)