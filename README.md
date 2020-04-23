# Jaqal Programming Utilities Project (Jaqal-pup) Extras
This repository contains extensions to the Jaqal-pup that may be useful for 
users.  Support is provided on a "best effort" basis, and quality cannot be 
guaranteed.  The primary content is compatibility with other Quantum 
programming toolsets, including transpiling.  In particular, we include
* The ability to automatically schedule gates in an efficient (but not 
  necessarily optimal) manner given an unscheduled program.
* The ability to decompose arbitrary unitary operations into native ion-trap 
  gates.
* The ability to convert the data structures used by many other quantum 
  software toolchains to our internal representation. Ideally this will 
  include:
    * IBM's Qiskit/OpenQASM
    * Rigetti's Quil/pyquil/quilc
    * Google's Cirq
    * Microsoft's Q#
    * ETH Zurich's ProjectQ
    * CQC's t|ket>
* Extensions to some or all of the above toolchains to properly support 
  ion-based quantum computation, as needed.
