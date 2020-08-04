"""Python tools for Jaqal (extras)"""

import sys
from setuptools import setup, find_packages

name = "JaqalPaq-extras"
description = "Python tools for Jaqal (extras)"
version = "1.0.0b0"

setup(
    name=name,
    description=description,
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    version=version,
    author="Benjamin C. A. Morrison, Jay Wesley Van Der Wall, Daniel Lobser, Antonio Russo, Kenneth Rudinger, Peter Maunz",
    author_email="qscout@sandia.gov",
    packages=find_packages(
        include=[
            "jaqalpaq.scheduler",
            "jaqalpaq.transpilers",
            "jaqalpaq.transpilers.*",
        ]
    ),
    package_dir={"": "."},
    install_requires=["JaqalPaq"],
    extras_requires={"tests": ["pytest"],},
    python_requires=">=3.6.5",
    platforms=["any"],
    url="https://qscout.sandia.gov",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Physics",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Unix",
    ],
)
