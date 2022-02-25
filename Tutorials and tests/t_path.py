from manim import *
class PathScene(Scene):
    def construct(self):
        symbol1 = Tex("m", height = 4)
        symbol2 = Tex("e", height = 4)

        path1 = symbol1.family_members_with_points()[0]
        path2 = symbol2.family_members_with_points()[0]

        ts = np.arange(0, 1, 0.001)
        points1 = np.array([
            path1.point_from_proportion(t)
            for t in ts
        ])
        points2 = path2.points
        group = VGroup(path1, path2).arrange(RIGHT, buff=2)
        center1 = path1.get_center()
        center2 = path2.get_center()
        # n = 12
        # dt = 1/n
        # ts = np.arange(0, 1, dt)
        # print(ts)
        print(type(center1))
        print(len(points1))
        print(points1.shape)

        # print('first one')
        # print(center1)
        # print("length:")
        # print(len(center1))
        # print("shape:")
        # print(center1.shape)

        # for p, t in zip(points1,points2):
        #     point = Point(location = p + center1, color=BLUE)
        #     toint = Point(location = t + center2, color=RED)
        #     self.add(point, toint)

        for p in points1:
            point = Point(location = p + center1, color=BLUE)
            self.add(point)

        # Conclusion, the points given from path are not moved when the object is moved

        # print(dim(points1))
        # print(points1)
        self.add(path1, path2)