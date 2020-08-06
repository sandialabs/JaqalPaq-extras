# Copyright 2020 National Technology & Engineering Solutions of Sandia, LLC (NTESS).
# Under the terms of Contract DE-NA0003525 with NTESS, the U.S. Government retains
# certain rights in this software.
from jaqalpaq.core import CircuitBuilder, GateStatement
from jaqalpaq.core.circuitbuilder import UnscheduledBlockBuilder

# from qscoutlib import MSGate, QasmGate, IonUnroller
from qiskit.converters import dag_to_circuit
from jaqalpaq import JaqalError

# from sympy.core.evalf import N
import numpy as np

QISKIT_NAMES = {
    "i": "I",
    "r": "R",
    "sx": "Sx",
    "sy": "Sy",
    "x": "Px",
    "y": "Py",
    "rz": "Rz",
    "ms2": "MS",
}


def jaqal_circuit_from_dag_circuit(dag):
    """
    Converts a Qiskit directed-acyclic-graph representation of a circuit to a
    :class:`jaqalpaq.core.Circuit`.
    See :func:`jaqal_circuit_from_qiskit_circuit` for details.

    :param qiskit.dagcircuit.DAGCircuit dag: The directed acyclic graph circuit to convert.
    :returns: The same quantum circuit, converted to JaqalPaq.
    :rtype: jaqalpaq.core.Circuit
    """
    return jaqal_circuit_from_qiskit_circuit(dag_to_circuit(dag))


def jaqal_circuit_from_qiskit_circuit(circuit, names=None, native_gates=None):
    """
    Converts a Qiskit circuit to a :class:`jaqalpaq.core.Circuit`. The circuit
    will be structured into a sequence of unscheduled blocks. All instructions between one
    barrier statement and the next will be put into an unscheduled block together. If the
    :mod:`qscout.scheduler` is run on the circuit, as many as possible of those gates will
    be parallelized within each block, while maintaining the order of the blocks.
    Otherwise, the circuit will be treated as a fully sequential circuit.

    Measurement and reset commands are supported, but only if applied to every qubit in
    the circuit in immediate succession. If so, they will be mapped to a prepare_all or
    measure_all gate. If the circuit does not end with a measurement, then a measure_all
    gate will be appended to it.

    Circuits containing multiple quantum registers will be converted to circuits with a
    single quantum register, containing all the qubits from each register. The parts of
    that larger register that correspond to each of the original registers will be mapped
    with the appropriate names.

    :param qiskit.circuit.QuantumCircuit circuit: The circuit to convert.
    :param names: A mapping from names of Qiskit gates to the corresponding native Jaqal
        gate names. If omitted, maps i, r (:class:`jaqalpaq.transpilers.qiskit.RGate`),
        sx (:class:`jaqalpaq.qiskit.SXGate`), sy (:class:`jaqalpaq.qiskit.SYGate`), x, y,
        rz, and ms2 (:class:`jaqalpaq.qiskit.MSGate`) to their QSCOUT counterparts.
    :type names: dict or None
    :param native_gates: The native gate set to target. If None, target the QSCOUT native
        gates.
    :type native_gates: dict or None
    :returns: The same quantum circuit, converted to JaqalPaq.
    :rtype: jaqalpaq.core.Circuit
    :raises JaqalError: If any instruction acts on a qubit from a register other than the
        circuit's qregs.
    :raises JaqalError: If the circuit includes a snapshot instruction.
    :raises JaqalError: If the user tries to measure or reset only some of the qubits,
        rather than all of them.
    :raises JaqalError: If the circuit includes a gate not included in `names`.
    """
    if native_gates is None:
        from qscout.v1.std import NATIVE_GATES

        native_gates = NATIVE_GATES
    n = sum([qreg.size for qreg in circuit.qregs])
    qsc = CircuitBuilder(native_gates=native_gates)
    if names is None:
        names = QISKIT_NAMES
    baseregister = qsc.register("baseregister", n)
    offset = 0
    registers = {}
    for qreg in circuit.qregs:
        registers[qreg.name] = qsc.map(
            qreg.name, baseregister, slice(offset, offset + qreg.size)
        )
        offset += qreg.size
    # We're going to divide the circuit up into blocks. Each block will contain every gate
    # between one barrier statement and the next. If the circuit is output with no further
    # processing, then the gates in each block will be run in sequence. However, if the
    # circuit is passed to the scheduler, it'll try to parallelize as many of the gates
    # within each block as possible, while keeping the blocks themselves sequential.
    block = UnscheduledBlockBuilder()
    qsc.expression.append(block.expression)
    block.gate("prepare_all")
    measure_accumulator = set()
    reset_accumulator = set()
    in_preamble = True
    for instr in circuit.data:
        if reset_accumulator:
            if instr[0].name == "reset":
                target = instr[1][0]
                if target.register.name in registers:
                    reset_accumulator.add(
                        registers[target.register.name].resolve_qubit(target.index)[1]
                    )
                else:
                    raise JaqalError("Register %s invalid!" % target.register.name)
                if len(reset_accumulator) == n:
                    block.gate("prepare_all")
                    reset_accumulator = {}
                continue
            else:
                raise JaqalError(
                    "Cannot reset only qubits %s and not whole register."
                    % reset_accumulator
                )
                # reset_accumulator = set()
        if measure_accumulator:
            if instr[0].name == "measure":
                target = instr[1][0]
                if target.register.name in registers:
                    measure_accumulator.add(
                        registers[target.register.name].resolve_qubit(target.index)[1]
                    )
                else:
                    raise JaqalError("Register %s invalid!" % target.register.name)
                if len(measure_accumulator) == n:
                    block.gate("measure_all")
                    measure_accumulator = {}
                continue
            else:
                raise JaqalError(
                    "Cannot measure only qubits %s and not whole register."
                    % reset_accumulator
                )
                # measure_accumulator = set()
        if instr[0].name == "measure":
            in_preamble = False
            target = instr[1][0]
            if target.register.name in registers:
                measure_accumulator = {
                    registers[target.register.name].resolve_qubit(target.index)[1]
                }
                if len(measure_accumulator) == n:
                    block.gate("measure_all")
                    measure_accumulator = {}
                continue
            else:
                raise JaqalError("Register %s invalid!" % target.register.name)
        elif instr[0].name == "reset":
            if not in_preamble:
                target = instr[1][0]
                if target.register.name in registers:
                    reset_accumulator = {
                        registers[target.register.name].resolve_qubit(target.index)[1]
                    }
                    if len(reset_accumulator) == n:
                        block.gate("prepare_all")
                        reset_accumulator = {}
                else:
                    raise JaqalError("Register %s invalid!" % target.register.name)
        elif instr[0].name == "barrier":
            block = UnscheduledBlockBuilder()
            qsc.expression.append(block.expression)
            # Use barriers to inform the scheduler, as explained above.
        elif instr[0].name == "snapshot":
            raise JaqalError(
                "Physical hardware does not support snapshot instructions."
            )
        elif instr[0].name in names:
            in_preamble = False
            targets = instr[1]
            for target in targets:
                if target.register.name not in registers:
                    raise JaqalError("Gate register %s invalid!" % target.register.name)
            block.gate(
                names[instr[0].name],
                *[registers[target.register.name][target.index] for target in targets],
                *[float(param) for param in instr[0].params]
            )
        else:
            raise JaqalError(
                "Instruction %s not available on trapped ion hardware; try unrolling first."
                % instr[0].name
            )
    block.gate("measure_all", no_duplicate=True)
    return qsc.build()
