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
3. In an elevated PowerShell terminal, run `choco install manimce`
4. In an elevated PowerShell terminal, run `choco install manim-latex` for ability to render LaTeX

## Usage

A parent class `FourierSceneAbstract` contains the logic and default configurations, the concrete parts of the animation are constructed in the child class `FourierScene`.

Two things to know:

1. Rendering the animation takes time because of the large number of submobjects, therefore default values have been set for a lower fidelity fourier series. To get a path of higher fidelity that more closely resembles the original symbol, set the number of generated vectors to `self.n_vectors = 100`. Optionally one can also play around with decreasing `self.parametric_func_step` and increasing `self.path_n_samples`.

2. Command to render animation is `manim fourierseries.py FourierScene`, optionally add flag
   - `-ql` to render animation in low quality for speeding up the process, highly recommended while testing
   - `-qh` to render animation in high quality
   - `-p` to immediately play animation when finished rendering

## Screenshot

[![Video screenshot](/Screenshot_2022-02-25.png)](https://www.youtube.com/watch?v=c-MMb71NMvw)
