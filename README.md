# JaqalPaq-Extras
JaqalPaq-Extras contains extensions to the
[JaqalPaq](https://gitlab.com/jaqal/jaqalpaq/) python package, which itself is
used to parse, manipulate, emulate, and generate quantum assembly code written
in
[Jaqal](https://qscout.sandia.gov/jaqal) (Just another quantum assembly
language).  The purpose of JaqalPaq-Extras is to facilitate the conversion of
programs written in other quantum assembly languages into Jaqal circuit objects
in JaqalPaq.  JaqalPaq-Extras is supported on a "best effort" basis, and
quality cannot be guaranteed.

Because some other quantum assembly languages do not support explicit
scheduling like Jaqal does, JaqalPaq-Extras also contains some basic quantum
circuit scheduling routines.  Furthermore, to facilitate execution on the
[QSCOUT](https://qscout.sandia.gov/) (Quantum Scientific Computing Open User
Testbed) platform, JaqalPaq-Extras also includes extensions for third-party
quantum software toolchains that support the QSCOUT hardware model (including
its native gate set and scheduling constraints).  In summary, JaqalPaq-Extras
contains the following functionalities:


* Conversion of quantum assembly data structures into JaqalPaq circuit objects
  from:
    * IBM's [Qiskit](https://github.com/Qiskit)
    * Rigetti's [pyquil](https://github.com/rigetti/pyquil)
    * Google's [Cirq](https://github.com/quantumlib/Cirq)
    * ETH Zurich's [ProjectQ](https://github.com/ProjectQ-Framework/ProjectQ)
    * CQC's [pytket](https://github.com/CQCL/pytket)
* Basic routines for scheduling unscheduled quantum assembly programs.
* Extensions to these packages above, as needed, to support to the QSCOUT
  hardware model.

## Installation

JaqalPaq-Extras is available on
[GitLab](https://gitlab.com/jaqal/jaqalpaq-extras).  It requires JaqalPaq to be
installed first, which is also  available on
[GitLab](https://gitlab.com/jaqal/jaqalpaq).  JaqalPaq-Extras requires JaqalPaq
itself be installed first.
Both JaqalPaq and its extensions can be installed with
[pip](https://pip.pypa.io/en/stable/):

```bash
pip install jaqalpaq
pip install jaqalpaq-extras
```

If only the scheduler will be used, there are no other dependencies.
However, to make use of the transpiler subpackages, one or more other software
toolchains
must be installed. As of this writing, all five supported toolchains can be
installed via
pip as follows, with the supported versions of these packages indicated:

```bash
pip install qiskit>=0.27.0,<0.28.0
pip install pyquil>=2.21.0,<3.0.0
pip install cirq>=0.11.0,<0.12.0
pip install projectq>=0.5.1,<0.7.0
pip install pytket>=0.5.6,<0.13.0
```

Additionally, a gate-set specification is required for all of the transpiler
subpackages.
Currently, we provide the QSCOUT native gate models, which is also available on
[GitLab](https://gitlab.com/jaqal/qscout-gatemodels/) and can be installed via
[pip](https://pip.pypa.io/en/stable/):

```bash
pip install qscout-gatemodels
```

## Documentation

Online documentation is hosted on [Read the
Docs](https://jaqalpaq.readthedocs.io).


## License
[Apache 2.0](https://choosealicense.com/licenses/apache-2.0/)

## Questions?

For help and support, please contact
[qscout@sandia.gov](mailto:qscout@sandia.gov).
