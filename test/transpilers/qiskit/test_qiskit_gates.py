import unittest, pytest

import jaqalpaq

qiskit = pytest.importorskip("qiskit")

from jaqalpaq.transpilers.qiskit import MSGate, SXGate, SXDGate, SYGate, SYDGate, RGate
from qiskit.circuit import QuantumCircuit, QuantumRegister
from math import pi


class QiskitGateTester(unittest.TestCase):
    def test_msgate(self):
        qr = QuantumRegister(2)
        circ = QuantumCircuit(qr)
        circ.ms2(pi / 4, pi / 4, qr[0], qr[1])
        gates = [inst[0].name for inst in circ.decompose()]
        self.assertEqual(gates, ["u3", "u3", "rxx", "u3", "u3"])

    def test_rgate(self):
        qr = QuantumRegister(1)
        circ = QuantumCircuit(qr)
        circ.r(pi / 4, pi / 4, qr[0])
        gates = [inst[0].name for inst in circ.decompose()]
        self.assertEqual(gates, ["rz", "rx", "rz"])

    def test_sxgate(self):
        qr = QuantumRegister(1)
        circ = QuantumCircuit(qr)
        circ.sx(qr[0])
        gates = [inst[0].name for inst in circ.decompose()]
        self.assertEqual(gates, ["rx"])

    def test_sxdgate(self):
        qr = QuantumRegister(1)
        circ = QuantumCircuit(qr)
        circ.sxd(qr[0])
        gates = [inst[0].name for inst in circ.decompose()]
        self.assertEqual(gates, ["rx"])

    def test_sygate(self):
        qr = QuantumRegister(1)
        circ = QuantumCircuit(qr)
        circ.sy(qr[0])
        gates = [inst[0].name for inst in circ.decompose()]
        self.assertEqual(gates, ["ry"])

    def test_sydgate(self):
        qr = QuantumRegister(1)
        circ = QuantumCircuit(qr)
        circ.syd(qr[0])
        gates = [inst[0].name for inst in circ.decompose()]
        self.assertEqual(gates, ["ry"])
