"""Python tools for Jaqal (extras)"""

import sys
from setuptools import setup, find_packages

name = "JaqalPaq-extras"
description = "Python tools for Jaqal (extras)"
version = "1.0.0b1"

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
    install_requires=[f"JaqalPaq=={version}"],
    extras_require={
        "tests": ["pytest"],
        "qiskit": ["qiskit>=0.19.0,<0.20.0", "qscout-gatemodels"],
        "pyquil": ["pyquil>=2.21.0,<3.0.0", "qscout-gatemodels"],
        "cirq": ["cirq>=0.8.2,<0.9.0", "qscout-gatemodels"],
        "projectq": ["projectq>=0.5.1,<0.6.0", "qscout-gatemodels"],
        "pytket": ["pytket>=0.5.6,<0.6.0", "qscout-gatemodels"],
    },
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
