# Copyright 2020 National Technology & Engineering Solutions of Sandia, LLC (NTESS).
# Under the terms of Contract DE-NA0003525 with NTESS, the U.S. Government retains
# certain rights in this software.
from pyquil.api._qac import AbstractCompiler
from typing import Optional
from pyquil.quil import Program, Gate
from pyquil.quilbase import Measurement, ResetQubit, Reset, Declare
from jaqalpaq.core import CircuitBuilder, Circuit
from jaqalpaq.core.circuitbuilder import UnscheduledBlockBuilder
from jaqalpaq import JaqalError
import numpy as np

# We automatically map gates that have the same name up to case; for example, any gate
# generated by quil_gates.

QUIL_NAMES = {
    "X": "Px",
    "Y": "Py",
}


class IonCompiler(AbstractCompiler):
    """
    A compiler that converts Quil programs to Jaqal circuits that can be executed on the QSCOUT device.

    :param pyquil.device.AbstractDevice device: The quantum device the compiler should target.
    :param names: A mapping from names of Quil gates to the corresponding native Jaqal gate names.
        If omitted, maps X, Y, RZ, and any gate produced by :func:`qscout.quil.quil_gates`
        to their QSCOUT counterparts. Any gate whose Jaqal native gate name and Quil gate name
        are the same up to case will automatically be mapped to each other unless an alternative
        mapping is specified.
    :type names: dict or None
    :param native_gates: The native gate set to target. If None, target the QSCOUT native gates.
    :type native_gates: dict or None
    """

    def __init__(self, device, names=None, native_gates=None):
        self._device = device
        self.names = names
        if self.names is None:
            self.names = QUIL_NAMES
        self.native_gates = native_gates
        if self.native_gates is None:
            from qscout.v1.std import NATIVE_GATES

            self.native_gates = NATIVE_GATES
        for gate in self.native_gates:
            if gate.name.upper() not in self.names:
                self.names[gate.name.upper()] = gate.name
        print(self.names)

    def quil_to_native_quil(self, program: Program, *, protoquil=None) -> Program:
        """
        Currently does nothing. Eventually, will compile a Quil program down to the native
        gates of the QSCOUT machine.

        :param pyquil.quil.Program program: The program to compile.
        :param bool protoquil: Ignored.
        :returns: The input program.
        :rtype: pyquil.quil.Program
        """
        return program  # TODO: Implement transpiler pass to convert arbitrary circuit.

    def native_quil_to_executable(self, nq_program: Program) -> Optional[Circuit]:
        """
        Compiles a Quil program to a :class:`qscout.core.Circuit`. Because Quil
        does not support any form of schedule control, the entire circuit will be put in a
        single unscheduled block. If the :mod:`qscout.scheduler` is run on the circuit, as
        many as possible of those gates will be parallelized, while maintaining the order
        of gates that act on the same qubits. Otherwise, the circuit will be treated as a
        fully sequential circuit.

        Measurement and reset commands are supported, but only if applied to every qubit in
        the circuit in immediate succession. If so, they will be mapped to a prepare_all or
        measure_all gate. If the circuit does not end with a measurement, then a measure_all
        gate will be appended to it.

        :param pyquil.quil.Program nq_program: The program to compile.
        :returns: The same quantum program, converted to JaqalPaq.
        :rtype: qscout.core.Circuit
        :raises JaqalError: If the program includes a non-gate instruction other than resets or measurements.
        :raises JaqalError: If the user tries to measure or reset only some of the qubits, rather than all of them.
        :raises JaqalError: If the program includes a gate not included in `names`.
        """
        n = max(nq_program.get_qubits()) + 1
        if n > len(self._device.qubits()):
            raise JaqalError(
                "Program uses more qubits (%d) than device supports (%d)."
                % (n, len(self._device.qubits()))
            )
        qsc = CircuitBuilder(native_gates=self.native_gates)
        block = UnscheduledBlockBuilder()
        qsc.expression.append(block.expression)
        # Quil doesn't support barriers, so either the user
        # won't run the the scheduler and everything will happen
        # sequentially, or the user will and everything can be
        # rescheduled as needed.
        qreg = qsc.register("qreg", n)
        block.gate("prepare_all")
        reset_accumulator = set()
        measure_accumulator = set()
        in_preamble = True
        for instr in nq_program:
            if reset_accumulator:
                if isinstance(instr, ResetQubit):
                    reset_accumulator.add(instr.qubit.index)
                    if nq_program.get_qubits() <= reset_accumulator:
                        block.gate("prepare_all")
                        reset_accumulator = set()
                        in_preamble = False
                    continue
                else:
                    raise JaqalError(
                        "Cannot reset only qubits %s and not whole register."
                        % reset_accumulator
                    )
                    # reset_accumulator = set()
            if measure_accumulator:
                if isinstance(instr, Measurement):
                    measure_accumulator.add(instr.qubit.index)
                    if nq_program.get_qubits() <= measure_accumulator:
                        block.gate("measure_all")
                        measure_accumulator = set()
                        in_preamble = False
                    continue
                else:
                    raise JaqalError(
                        "Cannot measure only qubits %s and not whole register."
                        % measure_accumulator
                    )
                    # measure_accumulator = set()
            if isinstance(instr, Gate):
                if instr.name in self.names:
                    block.gate(
                        self.names[instr.name],
                        *[qreg[qubit.index] for qubit in instr.qubits],
                        *[float(p) for p in instr.params]
                    )
                    in_preamble = False
                else:
                    raise JaqalError("Gate %s not in native gate set." % instr.name)
            elif isinstance(instr, Reset):
                if not in_preamble:
                    block.gate("prepare_all")
                    in_preamble = False
            elif isinstance(instr, ResetQubit):
                if not in_preamble:
                    reset_accumulator = {instr.qubit.index}
                    if nq_program.get_qubits() <= reset_accumulator:
                        block.gate("prepare_all")
                        reset_accumulator = set()
            elif isinstance(instr, Measurement):
                measure_accumulator = {instr.qubit.index}
                # We ignore the classical register.
                if nq_program.get_qubits() <= measure_accumulator:
                    block.gate("measure_all")
                    measure_accumulator = set()
                    in_preamble = False
            elif isinstance(instr, Declare):
                pass  # Ignore allocations of classical memory.
            else:
                raise JaqalError("Instruction %s not supported." % instr.out())
        block.gate("measure_all", no_duplicate=True)
        return qsc.build()
