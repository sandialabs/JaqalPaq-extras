import unittest, pytest

import jaqalpaq

qiskit = pytest.importorskip("qiskit")

from jaqalpaq.transpilers.qiskit import qiskit_circuit_from_jaqal_circuit
from jaqalpaq.core import CircuitBuilder
from jaqalpaq.generator import generate_jaqal_program
from qiskit.circuit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.transpiler import PassManager
from math import pi
from qiskit.converters.circuit_to_dag import circuit_to_dag
from qscout.v1.std import jaqal_gates


class PytketReverseTranspilerTester(unittest.TestCase):
    def test_prepare_bell_pairs(self):
        jcirc = CircuitBuilder(jaqal_gates.ALL_GATES)
        reg1 = jcirc.register("q", 2)
        block = jcirc.block()
        block.gate("prepare_all")
        block.gate("MS", reg1[0], reg1[1], pi / 4, pi / 2)
        block.gate("measure_all")
        built = jcirc.build()
        transpiled = qiskit_circuit_from_jaqal_circuit(built)

        qr = QuantumRegister(2, "q")
        qkc = QuantumCircuit(qr)
        qkc.reset(range(2))
        qkc.jaqalms(pi / 4, pi / 2, qr[0], qr[1])
        qkc.measure_all()

        self.assertEqual(str(qkc.draw()), str(transpiled.draw()))
        # We compare the circuit diagrams because comparing the QASM means that we miss circuits that have the same gates re-ordered in a commuting way.
