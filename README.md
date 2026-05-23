# manim-fourier-project

Written in Python to draw cool things using the math of complex Fourier-series. This is an updated version of the code from youtuber Theorem of Beethoven, adapted from CairoManim to Manim Community Edition [ManimCE](https://www.manim.community/)

Inspired by brilliant math youtuber 3Blue1Brown, creator of the original Manim Python library.

- **Theorem of Beethoven link**: https://www.youtube.com/watch?v=2tTshwWTEic
- **3Blue1Brown link**: https://www.youtube.com/watch?v=r6sGWTCMz2k
- **Resulting video**: https://www.youtube.com/watch?v=c-MMb71NMvw

## Get Started

### Prerequisites
- Python 3.10 or higher

### Setup 

First setup the Python virtual environment.

If using Powershell (Windows):
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt # This may take a while
```

Or if using POSIX (macOS / Linux):
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt # This may take a while
```

Then to render:
```
manim fourierseries.py FourierScene -ql -p
```

Alternative flags for this command are:
- `-ql` to render animation in low quality, highly recommended while testing to speed up
- `-qh` to render animation in high quality
- `-p` to immediately play animation when finished rendering

## Code and discussion

A parent class `FourierSceneAbstract` contains the logic and default configurations, the concrete parts of the animation are constructed in the child class `FourierScene`.

Rendering the animation takes time because of the large number of submobjects, therefore default values have been set for a lower fidelity fourier series. To get a path of higher fidelity that more closely resembles the original symbol, set the number of generated vectors to `self.n_vectors = 100`. Optionally one can also play around with decreasing `self.parametric_func_step` and increasing `self.path_n_samples`.

### Attempts to use OpenGL rendering

I attempted to use the ManimCE [OpenGL rendering](https://docs.manim.community/en/stable/faq/opengl.html) but ran into a while host of issues, if someone knows how to convert this script to be compatible with the OpenGL renderer

## Screenshot

[![Video screenshot](/Screenshot_2022-02-25.png)](https://www.youtube.com/watch?v=c-MMb71NMvw)

## Tested Environment

Tested with Python 3.13 and Manim v0.20.1.
