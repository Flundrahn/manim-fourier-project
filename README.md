# manim-fourier-project

Written in Python to draw cool things using the math of complex Fourier-series. This is an updated version of the code from youtuber Theorem of Beethoven, adapted from CairoManim to [ManimCE](https://www.manim.community/)

Inspired by brilliant math youtuber 3Blue1Brown, creator of the Manim Python library.

- **Theorem of Beethoven link**: https://www.youtube.com/watch?v=2tTshwWTEic
- **3Blue1Brown link**: https://www.youtube.com/watch?v=r6sGWTCMz2k
- **Resulting video**: https://www.youtube.com/watch?v=c-MMb71NMvw

## Installation on Windows

Detailed instructions can be found in the [ManimCE Documentation](https://docs.manim.community/en/stable/installation/windows.html), but in short:

1. Install Python 3.7 or higher
2. Install Chocolatey package manager
3. In an elevated PowerShell window, run `choco install manimce`
4. In an elevated PowerShell window, run `choco install manim-latex` for ability to render LaTeX

## Usage

Two things to know:

1.  Rendering the animation with current settings takes considerable time because of the large number of submobjects. For faster render set:

    - self.n_vectors = 40
    - self.parametric_func_step = 0.001
    - self.path_n_samples = 1000

2.  Command to render animation is `manim fourierseries.py`
    - optionally add flag `-ql` to render animation in low quality in order to speed up the process
    - optionally add flag `-qh` to render animation in high quality
    - optionally add flag `-p` to immediately play animation

## Screenshot

[![Video screenshot](/Screenshot_2022-02-25.png)](https://www.youtube.com/watch?v=c-MMb71NMvw)
