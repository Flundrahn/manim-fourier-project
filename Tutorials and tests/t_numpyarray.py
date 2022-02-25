import numpy as np
from manim import *

# path = ParametricFunction(
#             lambda t: center + reduce(op.add, [
#                 complex_to_R3(
#                     coef * np.exp(TAU * 1j * freq * t)
#                 )
#                 for coef, freq in zip(coefs, freqs)
#             ]),
#             t_range = np.array([0, 1])


dt = 1 / 1000
ts = np.arange(0, TAU, dt)

samples = np.array([np.sin(t) for t in ts])
