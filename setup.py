"""Python tools for Jaqal (extras)"""

import sys
from setuptools import setup

try:
    from sphinx.setup_command import BuildDoc
except ImportError:
    print("Warning: document cannot be built without sphinx")
    BuildDoc = None

name = "Jaqal-pup-extra"
description = "Python tools for Jaqal (extras)"
version = "1.0"

setup(
    name=name,
    description=description,
    version=version,
    author="Benjamin C. A. Morrison, Jay Wesley Van Der Wall, Lobser, Daniel, Antonio Russo, Kenneth Rudinger, Peter Maunz",
    author_email="qscout@sandia.gov",
    packages=[
        "jaqal.scheduler",
        "jaqal.transpilers",
        "jaqal.transpilers.cirq",
        "jaqal.transpilers.projectq",
        "jaqal.transpilers.qiskit",
        "jaqal.transpilers.quil",
        "jaqal.transpilers.tket",
    ],
    package_dir={"": "."},
    install_requires=["Jaqal-pup"],
    extras_requires={"tests": ["pytest"], "docs": ["sphinx"],},
    python_requires=">=3.7",
    platforms=["any"],
    url="https://qscout.sandia.gov",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering :: Physics",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Unix",
    ],
    cmdclass={"build_sphinx": BuildDoc},
)
