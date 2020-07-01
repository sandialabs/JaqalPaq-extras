from jaqalpaq import JaqalError
import networkx as nx
from pyquil.device import NxDevice
from pyquil.api import QuantumComputer
from pyquil.quilbase import Gate
from pyquil.quilatom import unpack_qubit
from .ioncompiler import IonCompiler
from .qscoutam import QSCOUTAM
import numpy as np
import pyquil


def get_ion_device(num_qubits):
    return NxDevice(nx.complete_graph(num_qubits))


def get_ion_qam():
    return QSCOUTAM()


def get_ion_qc(num_qubits):
    """Constructs a quantum computer object that represents the QSCOUT hardware.
    Unlike the builtin Quil counterparts, it can't run quantum programs, but it can still
    be used as a compilation target and thus used to generate Jaqal code (which can then
    be submitted to be run on the actual QSCOUT device).

    :param int num_qubits: How many qubits in the trap will be used.
    :returns: The quantum computer object for compilation.
    :rtype: pyquil.api.QuantumComputer
    """
    device = get_ion_device(num_qubits)
    return QuantumComputer(
        name="QSCOUT-%d" % num_qubits,
        qam=get_ion_qam(),
        device=device,
        compiler=IonCompiler(device),
    )


def quil_gates(native_gates=None):
    """Generates quil versions of a gate set (the QSCOUT native gates, by default).

    :returns: A mapping of gate names to functions that take classical parameters and
        qubit indices and build pyquil gates.
    :rtype: dict

    .. warning::
        PyQuil simulators will give an error if QSCOUT native gates are passed to them!
    """
    dkt = {}
    if native_gates is None:
        from qscout.v1.std import NATIVE_GATES

        native_gates = NATIVE_GATES

    gates = {}

    for gate in native_gates:
        if gate.ideal_unitary is None:
            continue
        # pyquil expects non-parametrized gates to be matrices and
        # parametrized ones to be functions that return matrices.
        quil_name = gate.name.upper()
        classical_count = len(gate.classical_parameters)
        if classical_count == 0:
            gates[quil_name] = lambda *args: Gate(
                name=quil_name,
                params=args[:classical_count],
                qubits=[unpack_qubit(q) for q in args[classical_count:]],
            )
        else:
            gates[quil_name] = lambda *args: Gate(
                name=quil_name, params=[], qubits=[unpack_qubit(q) for q in args]
            )
    return gates


# NOTE: pyquil has changed the way they implement their simulators, so this kind of
# monkeypatching technique will no longer work. Thus, trapped-ion circuits cannot be
# simulated using pyquil's simulators, and instead must be transpiled and emulated
# in jaqalpaq.
# def patch_simulator():
#     """Modifies pyquil's simulator to support trapped-ion gates. Run before attempting to
#     simulate any circuit that includes the QSCOUT native gates.
#
#     :returns: A mapping of gate names to functions that take classical parameters and
#         qubit indices and build pyquil gates.
#     :rtype: dict

#     .. warning::
#         The simulator will give an error if QSCOUT native gates are passed to it before calling this function!
#     """
#     dkt = {}
#     from qscout.v1.std import NATIVE_GATES

#     gates = {}

#     for gate in NATIVE_GATES:
#         if gate.ideal_unitary is None:
#             continue
#         # pyquil expects non-parametrized gates to be matrices and
#         # parametrized ones to be functions that return matrices.
#         classical_count = len(gate.classical_parameters)
#         if classical_count == 0:
#             dkt[gate.name.upper()] = gate.ideal_unitary()
#             def build_gate(*args):
#                 return Gate(name=gate.name.upper(), params=args[:classical_count], qubits=[unpack_qubit(q) for q in args[classical_count:]])
#             gates[gate.name.upper()] = build_gate
#         else:
#             dkt[gate.name.upper()] = gate.ideal_unitary
#             def build_gate(*args):
#                 return Gate(name=gate.name.upper(), params=[], qubits=[unpack_qubit(q) for q in args])
#             gates[gate.name.upper()] = build_gate
#     QUANTUM_GATES.update(dkt)
#     return gates
