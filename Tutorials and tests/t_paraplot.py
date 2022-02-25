from manim import *
from matplotlib.animation import FuncAnimation
from sympy import false

class PlotParametricFunction(Scene):
            def construct(self):
                t = ValueTracker(0)
                t_range = [0, 2*TAU]

                def pfunc(t):
                        return np.array((np.sin(2 * t), np.sin(3 * t), 0))

                parafunc = ParametricFunction(pfunc, t_range=np.array([0, 0, 0.1])).set_color(RED)

                def update_parafunc(old_parafunc):
                    new_parafunc = ParametricFunction(pfunc, t_range = np.array([0, t.get_value(), 0.1]), use_smoothing = false).set_color(RED)
                    old_parafunc.become(new_parafunc)

                self.add(parafunc)
                parafunc.add_updater(update_parafunc)
                self.play(t.animate.set_value(2*TAU), run_time=2, rate_func=linear)
                # parafunc.remove_updater()
                # self.play(Write(parafunc))

                curve = FuncAnimation