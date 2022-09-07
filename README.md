# Manim Fourier Project

Code to draw cool things using the math of complex Fourier-series.

Code is written in Python, to use install [ManimCE](https://docs.manim.community/en/stable/tutorials/quickstart.html)

This is an updated version of the code from youtuber Theorem of Beethoven.

Adapted from CairoManim to [ManimCE](https://www.manim.community/)

Inspired by brilliant math youtuber 3Blue1Brown, creator of the Manim Python library.

- **Theorem of Beethoven link**: https://www.youtube.com/watch?v=2tTshwWTEic
- **3Blue1Brown link**: https://www.youtube.com/watch?v=r6sGWTCMz2k
- **Resulting video**: https://www.youtube.com/watch?v=c-MMb71NMvw

## Usage
1: Rendering the animation with current settings takes considerable time because of the large number of submobjects. For faster render set:
- self.n_vectors = 40
- self.parametric_func_step = 0.001
- self.path_n_samples = 1000

2: Command to render animation is `manim fourierseries.py` 

## Screenshot

[![Video screenshot](/Screenshot_2022-02-25.png)](https://www.youtube.com/watch?v=c-MMb71NMvw)
