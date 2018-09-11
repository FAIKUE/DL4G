# Jass Kit

- This project provides base components for the game of Jass

# Installation instruction
Obtain a local copy of the repository by either checking it out with git (preferred) or by downloading the zip file.

The directory source contains a setup.py file for use with the python installation tools. There are several possibilities to install, but the easiest is to install directly from the source directory. For this you have to navigate first into the source directory

If the option -e is used as in
```
pip3 install -e .
```
then [development mode](https://setuptools.readthedocs.io/en/latest/setuptools.html#development-mode) is selected and the current source directory is used and any updates from the git repository will automatically be used.

Without the option the sources are copied to the python installation directory:
```
pip3 install .
```

Python installations can either use the global repository or a separate environment. A popular tool to separate the environments is [virtualenv](https://pypi.org/project/virtualenv/), which is recommended if you do not want to use the global environment.

Contact thomas.koller@hslu.ch or ruedi.arnold@hslu.ch if you have any questions.