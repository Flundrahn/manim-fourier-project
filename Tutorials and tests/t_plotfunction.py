from manim import *

class PlotParametricFunction(Scene):
    def func(self, t):
        return np.array((np.sin(2*t), np.sin(3*t), 0))

    def construct(self):
        x_range = [0, TAU]
        y_range = [0, 2]
        func = ParametricFunction(self.func, t_range = np.array(x_range), fill_opacity=0).set_color(RED)
        func.move_to(ORIGIN)
        self.add(func.scale(3))
        ax = Axes(x_range=x_range, y_range=y_range).move_to(RIGHT)
        self.add(ax)