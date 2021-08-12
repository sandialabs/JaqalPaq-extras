"""Python tools for Jaqal (extras)"""

import sys
from setuptools import setup, find_packages

name = "JaqalPaq-extras"
description = "Python tools for Jaqal (extras)"
version = "1.0.0rc1"

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
        ],
        where="src",
    ),
    package_dir={"": "src"},
    install_requires=[f"JaqalPaq=={version}"],
    extras_require={
        "tests": ["pytest"],
        "qiskit": ["qiskit>=0.27.0,<0.28.0", "qscout-gatemodels"],
        "pyquil": ["pyquil>=2.21.0,<3.0.0", "qscout-gatemodels"],
        "cirq": ["cirq>=0.11.0,<0.12.0", "qscout-gatemodels"],
        "projectq": ["projectq>=0.5.1,<0.7.0", "qscout-gatemodels"],
        "pytket": ["pytket>=0.5.6,<0.13.0", "qscout-gatemodels"],
        "tutorial": ["pytket-qiskit"],
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
