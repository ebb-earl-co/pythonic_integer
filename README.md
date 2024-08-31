# pythonic_integer

Implement a class that has all\* of the features and characteristics
of the mathematical object "integer", without importing _anything_.

# Installation
First, clone the repository:
```
git clone https://github.com/ebb-earl-co/pythonic_integer.git
```


## Installation of Optional Packages for Testing
This package does not have any dependencies! ...unless you
want to execute the unit tests in the `test/` directory, _then_ you
will need `hypothesis`, `pytest`, and `more-itertools`. So, however
you want to invoke `pip`, everything you need for the **full
experience** is readily available on PyPi.

### For the Enthusiast
Part of the purpose of this package is to use a well-known concept
in order to test and learn _new_ concepts: in this case,
[`uv`](https://github.com/astral-sh/uv?tab=readme-ov-file#highlights):
> An extremely fast Python package and project manager, written in Rust

If, like me, you want to embrace and/or test a new tool, `uv` is
_seriously_ fast, so you won't waste much time doing so!

The [installation instructions for `uv`](https://github.com/astral-sh/uv?tab=readme-ov-file#installation)
for `uv` point out that there is a compiled release for most
platforms, so download that.

Then, go to the directory where this project was cloned, and,
inside that directory, run your variant (i.e., Unix-like or Windows)
of the terminal command:
```shell
uv sync
```

That's it! This project will be developed with the newest stable
version of Python (at the time of writing: 3.12.5), but all
non-deprecated versions of Python 3 will work just fine.

# Testing
To run the test suite, execute the following:
```bash
$ python3 -m pytest -v test/
```
if you're using a Unix-like system, or
```powershell
PS> python.exe -m pytest -v test\
```
if you're using Windows.
## For the Enthusiast
If you're trailblazing with `uv`, it is a tool that very much
wants to be the center of installation, environment, packaging,
and execution actions. So, the following is the command to run
the test suite:
```bash
$ uv run python3 -m pytest -v test/
```
