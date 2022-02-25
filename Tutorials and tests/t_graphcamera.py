from manim import *

class FollowingGraphCamera(MovingCameraScene):
    def construct(self):
        self.camera.frame.save_state()
        
        # create axes and curve

        ax = Axes(x_range=[-1, 10], y_range=[-1, 10])
        graph = ax.plot(lambda x: np.sin(x), color=BLUE, x_range=[0, 3*PI])

        # create dots based on graph
        moving_dot = Dot(ax.i2gp(graph.t_min, graph), color=ORANGE) # input to graph, graph.t_min is property with value = start of graph x-value?
        dot_1 = Dot(ax.i2gp(graph.t_min, graph))
        dot_2 = Dot(ax.i2gp(graph.t_min, graph))
        print(graph.t_max)
        print(type(graph.t_min))

        self.add(graph, dot_1, dot_2, moving_dot)
        self.play(self.camera.frame.animate.scale(0.5).move_to(moving_dot)) # no updater needed?

        def update_curve(mob):
            mob.move_to(moving_dot.get_center())    # so simple!

        self.camera.frame.add_updater(update_curve) # no parenthesis when input function into method
        self.play(MoveAlongPath(moving_dot, graph, rate_func=linear))   # moves dot along the path of another mobject = the graph
        self.camera.frame.remove_updater(update_curve)  # to stop frame updater, in order to restore saved frame

        self.play(Restore(self.camera.frame))