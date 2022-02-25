from manim import *
class ValueTrackerExample(Scene):
    def construct(self):
        number_line = NumberLine(include_numbers=True)
        pointer = Vector(DOWN)
        label = MathTex("x").add_updater(lambda m: m.next_to(pointer, UP))  # creates a label then adds updater to position it UP = above pointer

        tracker = ValueTracker()
    
        # adds updater to pointer to position at value of tracker on number_line
        pointer.add_updater(
            lambda m: m.next_to(
                number_line.n2p(tracker.get_value()),
                UP
            )
        )

        self.add(number_line, pointer, label)
        self.wait(2)

        atext = Text("set angle").next_to(label, UP)
        self.add(atext).play(pointer.animate.set_angle(PI*3/4), run_time=2)

        self.wait()

        btext = Text("rotate").move_to(atext)
        self.play(Transform(atext,btext))
        self.play(pointer.animate.rotate(-PI/4), run_time=2)

        # tracker += 1.5
        # self.wait(1)
        # tracker -= 4
        # self.wait(1)
        # self.play(tracker.animate.set_value(5))
        # self.wait(1)
        # self.play(tracker.animate.set_value(3))
        # self.play(tracker.animate.increment_value(-2))
        # self.wait(1)

        v1 = Vector([1, 2, 0])
        v2 = Vector([0, 1, 0])

        vectors = VGroup(v2,v2)

        v3 = vectors[-1]
        print(v3.get_end())