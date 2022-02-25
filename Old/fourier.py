# NOTES
# 1. Deadline set to saturday 12/2
# 2. Lookup value tracker
# 3. Lookup setup

from manim import *
import itertools as it
import numpy as np
import operator as op
from functools import reduce

# Abstract scene, not the construct of the actual scene later
class FourierScene(ZoomedScene):
    def __init__(self):
        super().__init__()
        self.n_vectors = 10
        self.big_radius = 2
        self.colors = [
            BLUE_D,
            BLUE_C,
            BLUE_E,
            GREY_BROWN,
        ]
        self.vector_config = {                      # Unsure whether this will pass arguments correctly
            "buff": 0,
            "max_tip_length_to_length_ratio": 0.25,
            "tip_length": 0.15,
            "max_stroke_width_to_length_ratio": 10,
            "stroke_width": 1.7,
        }
        self.circle_config = {
            "stroke_width": 1,
        }
        self.base_frequency = 1
        self.slow_factor = 0.5
        self.center_point = ORIGIN
        self.parametric_function_step_size = 0.1
        self.drawn_path_color = YELLOW
        self.drawn_path_stroke_width = 2
        self.interpolate_config = [0, 1]            # Opacity of drawn path at end and beginning respectively

    def setup(self):                                # SETUP: Don't know how Scene.setup works, set valuetrackers for slow_factor and vector_clock, then adds vector_clock
        super().setup()
        self.slow_factor_tracker = ValueTracker(self.slow_factor)
        self.vector_clock = ValueTracker(0)
        self.add(self.vector_clock)

    def add_vector_clock(self):                     # ADD_VECTOR_CLOCK: adds updater to vector_clock, note vector_clock seems to not be added here but in setup
        self.vector_clock.add_updater(
            lambda m, dt: m.increment_value(
                self.get_slow_factor() * dt
            )
        )
    
    def get_slow_factor(self):
        return self.slow_factor_tracker.get_value()

    def get_vector_time(self):          # GET_VECTOR_TIME: returns value of vector_clock
        return self.vector_clock.get_value()

    def get_freqs(self):                # May have something to do with sorting output after transform, compare DTF
        n = self.n_vectors
        all_freqs = list(range(n // 2, -n // 2, -1))
        all_freqs.sort(key=abs)
        return all_freqs                            # returns [0, 1, -1, 2, -2, ...-(n-1), n]

    # def get_coefficients(self):         # Unclear why this method is supposed to return complex zeroes, pay attention how used later
    #     return[complex(0) for _ in range(self.n_vectors)]   # note _ is used in for loop when variable is unnecessessary, just want to return something n_vectors times

    def get_color_iterator(self):       # Does this switch color in steps? uses library itertools
        return it.cycle(self.colors)    

    def get_rotating_vectors(self, freqs=None, coefficients=None):  # is freqs necessary argument?
        vectors = VGroup()
        self.center_tracker = VectorizedPoint(self.center_point)
 
        if freqs is None:
            freqs = self.get_freqs()
        # if coefficients is None:
        #     coefficients = self.get_coefficients()      # Only used when there are no coefficients, when would there be none?
 
        last_vector = None
        for freq, coefficient in zip(freqs, coefficients):
            if last_vector:
                center_func = last_vector.get_end
            else:
                center_func = self.center_tracker.get_location
            vector = self.get_rotating_vector(
            coefficient=coefficient,
            freq=freq,
            center_func=center_func,
            )
            vectors.add(vector)
            last_vector = vector
        return vectors

    def get_rotating_vector(self, coefficient, freq, center_func):
        vector = Vector(RIGHT, **self.vector_config)
        vector.scale(abs(coefficient))
        if abs(coefficient) == 0:
            phase = 0
        else:
            phase = np.angle(coefficient)
        vector.rotate(phase, about_point=ORIGIN)
        vector.freq = freq
        vector.coefficient = coefficient
        vector.center_func = center_func
        vector.add_updater(self.update_vector)
        return vector

    def update_vector(self, vector):
        time = self.get_vector_time()
        coef = vector.coefficient
        freq = vector.freq
        phase = np.log(coef).imag
 
        vector.set_length(abs(coef))
        vector.set_angle(phase + time * freq * TAU)
        vector.shift(vector.center_func() - vector.get_start())
        return vector

    def get_circles(self, vectors):
        return VGroup(*[
            self.get_circle(
                vector,
                color=color
            )
            for vector, color in zip(
                vectors,
                self.get_color_iterator()
            )
        ])

    def get_circle(self, vector, color=BLUE):
        circle = Circle(color=color, **self.circle_config)
        circle.center_func = vector.get_start
        circle.radius_func = vector.get_length
        circle.add_updater(self.update_circle)
        return circle

    def update_circle(self, circle):
        circle.set_width(2 * circle.radius_func())  # why would you update circle width every frame tho
        circle.move_to(circle.center_func())
        return circle

    def get_vector_sum_path(self, vectors, color=YELLOW):
        coefs = [v.coefficient for v in vectors]
        freqs = [v.freq for v in vectors]
        center = vectors[0].get_start()
 
        path = ParametricFunction(
            lambda t: center + reduce(op.add, [
                complex_to_R3(
                    coef * np.exp(TAU * 1j * freq * t)
                )
                for coef, freq in zip(coefs, freqs)
            ]),
            t_range = np.array([0, 1, self.parametric_function_step_size])
        )
        return path

    def get_drawn_path_alpha(self):     # Seems unecessary, why not just call get_vector_time right away, possibly to do with updater or readability
        return self.get_vector_time()

    def get_drawn_path(self, vectors, stroke_width=None, **kwargs):
        if stroke_width is None:
            stroke_width = self.drawn_path_stroke_width
        path = self.get_vector_sum_path(vectors, **kwargs)
        broken_path = CurvesAsSubmobjects(path)
        broken_path.curr_time = 0
        start, end = self.interpolate_config
 
        def update_path(path, dt):
            alpha = self.get_drawn_path_alpha()
            n_curves = len(path)
            for a, sp in zip(np.linspace(0, 1, n_curves), path):
                b = (alpha - a)
                if b < 0:
                    width = 0
                else:
                    width = stroke_width * interpolate(start, end, (1 - (b % 1)))
                sp.set_stroke(width=width)
            path.curr_time += dt
            return path
 
        broken_path.set_color(self.drawn_path_color)
        broken_path.add_updater(update_path)
        return broken_path

    def get_coefficients_of_path(self, path, n_samples=1000, freqs=None):
        if freqs is None:
            freqs = self.get_freqs()
            print("frequencies are:")
            print(freqs)
        dt = 1 / n_samples
        ts = np.arange(0, 1, dt)

        # Get sample points from path
        samples = np.array([
            path.point_from_proportion(t)
            for t in ts
        ])
        samples -= self.center_point
        complex_samples = samples[:, 0] + 1j * samples[:, 1]

        # Calculate fourier coefficients
        return [
            np.array([
                np.exp(-2*PI * 1j * freq * t) * cs
                for t, cs in zip(ts, complex_samples)   # zip pairs up t[k] with complex_samples[k]
            ]).sum() * dt for freq in freqs
        ]

class CustomAnimationExample(FourierScene):

    def __init__(self):
        super().__init__()
        self.n_vectors = 10
        self.slow_factor = 0.2
        self.fourier_symbol_config = {
            "stroke_width": 0,
            "fill_opacity": 0,
            "height": 4,
            "fill_color": WHITE
        }
        self.circle_config = {
            "stroke_width": 1,
            "stroke_opacity": 0.3,
        }
        
    def construct(self):
        # super().construct()
        t_symbol = Tex("T", **self.fourier_symbol_config)
        u_symbol = Tex("U", **self.fourier_symbol_config)

        group = VGroup(t_symbol, u_symbol).arrange(RIGHT,buff=0.3)

        # set paths
        path1 = t_symbol.family_members_with_points()[0]
        path2 = u_symbol.family_members_with_points()[0]

        # path 1 config
        coefs1 = self.get_coefficients_of_path(path1)
        vectors1 = self.get_rotating_vectors(coefficients=coefs1)
        circles1 = self.get_circles(vectors1)
        drawn_path1 = self.get_drawn_path(vectors1)

        # path 2 config
        coefs2 = self.get_coefficients_of_path(path2)
        vectors2 = self.get_rotating_vectors(coefficients=coefs2)
        circles2 = self.get_circles(vectors2)
        drawn_path2= self.get_drawn_path(vectors2)

        # text definition
        text = Tex("Thanks for watch!")
        text.scale(1.5)
        text.next_to(group,DOWN)

        # all elements toget
        all_mobs = VGroup(group,text)
        
        # set mobs to remove
        # vectors1_to_fade = vectors1.copy()
        # circles1_to_fade = circles1.copy()
        # vectors1_to_fade.clear_updaters()
        # circles1_to_fade.clear_updaters()
        # vectors2_to_fade = vectors2.copy()
        # circles2_to_fade = circles2.copy()
        # vectors2_to_fade.clear_updaters()
        # circles2_to_fade.clear_updaters()
 
        # self.play(
        #     *[
        #         GrowArrow(arrow)
        #         for vg in [vectors1_to_fade, vectors2_to_fade]
        #         for arrow in vg
        #     ],
        #     *[
        #         Create(circle)
        #         for cg in [circles1_to_fade, circles2_to_fade]
        #         for circle in cg
        #     ],
        #     run_time=2.5,
        # )
        # self.remove(
        #     *vectors1_to_fade,
        #     *circles1_to_fade,
        #     *vectors2_to_fade,
        #     *circles2_to_fade,
        # )
        print("type is:")
        print(type(drawn_path1))
        print("")
        self.add(
            vectors1,
            circles1,
            drawn_path1.set_color(RED),
            vectors2,
            circles2,
            drawn_path2.set_color(BLUE),
        )
        self.add_vector_clock()
 
        # wait one cycle
        self.wait( 1 / self.slow_factor)
        self.bring_to_back(t_symbol,u_symbol)
        self.wait()

        # move camera
        self.play(
            self.camera.frame.animate.set_height(all_mobs.height*1.2).move_to(all_mobs.get_center())
        )
        self.wait(0.5)
        self.play(Write(text))
        # self.wait(10)
