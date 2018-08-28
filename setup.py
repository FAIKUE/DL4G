# HSLU
#
# Created by Thomas Koller on 21.08.18
#
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jass-kit",
    version="0.9.0",
    author="ABIZ HSLU",
    author_email="thomas.koller@hslu.ch",
    description="Package for the game of jass",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(exclude=['test']),
    classifiers=[
        "Programming Language :: Python :: 3",
        # "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3'
)