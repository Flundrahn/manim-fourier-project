from signal import raise_signal
import numpy as np
import timeit
from manim import *

class FourierScene(ZoomedScene):
    def __init__(self):
        super().__init__()
        self.n_vectors = 8
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
        self.interpolate_config = [0, 1]            # Opacity/width of drawn path at end and beginning respectively
        self.n_samples = 1000                       # This number will be rounded up to closest power of 2, for fft performance
        self.path_n_samples = 2**np.ceil( np.log(self.n_samples) / np.log(2) )
        self.freqs = list(range(-self.n_vectors // 2, self.n_vectors // 2 + 1, 1))
        self.freqs.sort(key=abs)                    # NOTE moved freqs to be property of scene, so need only be calculated once

    def get_fourier_coefs(self, points):
        starttime = time.time()

        # dt = 1 / self.path_n_samples
        # ts = np.arange(0, 1, dt)

        # # Sample points
        # points = np.array([
        #     path.point_from_proportion(t)
        #     for t in ts
        # ])

        complex_points = points[:, 0] + 1j * points[:, 1]
        print(len(complex_points))
        coefficients = np.fft.fft(complex_points, norm = "forward")
        freqs = np.fft.fftfreq(complex_points.size, d = 1/complex_points.size)

        # Sort coefficients by size of frequency
        cf = zip(coefficients, freqs)

        


        # coefficients = np.fft.fftshift(coefficients_unshifted) # This is not the problem

        # coefficients = [
        #     np.array([
        #         np.exp(-TAU * 1j * freq * t) * cpoint
        #         for t, cpoint in zip(ts, complex_points)
        #     ]).sum() * dt for freq in self.freqs
        # ]
        endtime = time.time()

        print("---")
        
        print("Frequencies:")
        
        
        # r_freqs = np.flip(freqs)
        r_freqs = np.append(freqs[0], [(freqs[k], freqs[-k]) for k in range(1,self.n_vectors // 2)])
        print(np.size(r_freqs))
        for f in r_freqs:
            print(f)
        print(type(r_freqs))
        print(str(r_freqs))
        print("Number of coefficients: " + str(len(coefficients)))

        print("First three coefficients:")
        print([str(np.round(coefficients[k],3)) for k in range(0,3)])

        print("This run took: ", endtime - starttime)
        print("---")
       
        return coefficients

    def construct(self):

        # Symbols to draw
        symbol1 = Tex("m", height = 4)

        # Get Points
        dt = 1 / self.path_n_samples    
        ts = np.arange(0, 1, dt)
        
        path = symbol1.family_members_with_points()[0]  
        points = np.array([
            path.point_from_proportion(t)
            for t in ts
        ])

        coefs = self.get_fourier_coefs(points)
        c_signal = np.fft.ifft(coefs, norm = "forward")
        print(c_signal)
        print(type(c_signal))
        print(len(c_signal))
        r_signal=np.array([complex_to_R3(c) for c in c_signal])


        for p,r in zip(points,r_signal):
            self.add(Point(location = p, color=BLUE),
            Point(location = r, color=RED))


        # def sort_coefs(self,coefs):
        #     coefs_pos = coefs[0:len(coefs) // 2]
        #     coefs_neg = coefs[len(coefs) //2 + 1:]

        #     for f,c in zip(freqs, coefs):