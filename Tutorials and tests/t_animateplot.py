from manim import *
import numpy as np

class AnimatePlot(Scene):

    def func(self, t):
            return np.array((np.sin(2 * t), np.sin(3 * t), 0))

    def construct(self):
        x = ValueTracker()
        x_range = [0, 2*TAU]
        y_range = [-2, 2]
        axes1 = Axes(x_range=x_range, y_range=y_range)

        
        plot1 = axes1.plot(lambda t: np.sin(t), x_range=[x_range[0], x.get_value()])

        def update_plot(plot):
            plot.become(axes1.plot(lambda t: np.sin(t), x_range=[x_range[0], x.get_value()]))

        self.add(plot1)
        self.wait(1)
        plot1.add_updater(update_plot)
        self.play(x.animate.set_value(x_range[1]), run_time=2, rate_func=linear)