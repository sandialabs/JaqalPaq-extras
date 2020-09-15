import unittest, pytest

import jaqalpaq

qiskit = pytest.importorskip("qiskit")

from jaqalpaq.transpilers.qiskit import (
    MSGate,
    SXGate,
    SXDGate,
    SYGate,
    SYDGate,
    RGate,
    IonUnroller,
)
from qiskit.circuit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.transpiler import PassManager
from math import pi


class QiskitUnrollerTester(unittest.TestCase):
    def test_stable_gates(self):
        qr = QuantumRegister(2)
        cr = ClassicalRegister(2)
        circ = QuantumCircuit(qr, cr)
        circ.ms2(pi / 4, pi / 4, qr[0], qr[1])
        circ.r(pi / 2, pi / 4, qr[0])
        circ.x(qr[1])
        circ.y(qr[0])
        circ.sx(qr[0])
        circ.sxd(qr[0])
        circ.sy(qr[1])
        circ.syd(qr[1])
        circ.measure(qr, cr)
        unrolled = pass_manager = PassManager([IonUnroller()]).run(
            circ, output_name=circ.name + " unrolled"
        )
        self.assertEqual(str(circ.draw()), str(unrolled.draw()))
        # We compare the circuit diagrams because comparing the QASM means that we miss circuits that have the same gates re-ordered in a commuting way.

    def test_decompose_h(self):
        qr = QuantumRegister(1)
        circ = QuantumCircuit(qr)
        circ.h(qr[0])
        unrolled = pass_manager = PassManager([IonUnroller()]).run(
            circ, output_name=circ.name + " unrolled"
        )
        c2 = QuantumCircuit(qr)
        c2.rz(pi, qr[0])
        c2.sy(qr[0])
        self.assertEqual(str(c2.draw()), str(unrolled.draw()))

    def test_decompose_rx(self):
        qr = QuantumRegister(1)
        circ = QuantumCircuit(qr)
        circ.rx(pi, qr[0])
        circ.rx(pi / 2, qr[0])
        circ.rx(pi / 4, qr[0])
        unrolled = pass_manager = PassManager([IonUnroller()]).run(
            circ, output_name=circ.name + " unrolled"
        )
        c2 = QuantumCircuit(qr)
        c2.x(qr[0])
        c2.sx(qr[0])
        c2.r(0, pi / 4, qr[0])
        self.assertEqual(str(c2.draw()), str(unrolled.draw()))

    def test_decompose_ry(self):
        qr = QuantumRegister(1)
        circ = QuantumCircuit(qr)
        circ.ry(pi, qr[0])
        circ.ry(pi / 2, qr[0])
        circ.ry(pi / 4, qr[0])
        unrolled = pass_manager = PassManager([IonUnroller()]).run(
            circ, output_name=circ.name + " unrolled"
        )
        c2 = QuantumCircuit(qr)
        c2.y(qr[0])
        c2.sy(qr[0])
        c2.r(pi / 2, pi / 4, qr[0])
        self.assertEqual(str(c2.draw()), str(unrolled.draw()))

    def test_decompose_u1(self):
        qr = QuantumRegister(1)
        circ = QuantumCircuit(qr)
        circ.u1(pi, qr[0])
        unrolled = pass_manager = PassManager([IonUnroller()]).run(
            circ, output_name=circ.name + " unrolled"
        )
        c2 = QuantumCircuit(qr)
        c2.rz(pi, qr[0])
        self.assertEqual(str(c2.draw()), str(unrolled.draw()))

    def test_decompose_u2(self):
        qr = QuantumRegister(1)
        circ = QuantumCircuit(qr)
        circ.u2(pi, pi / 2, qr[0])
        unrolled = pass_manager = PassManager([IonUnroller()]).run(
            circ, output_name=circ.name + " unrolled"
        )
        c2 = QuantumCircuit(qr)
        c2.rz(pi / 2, qr[0])
        c2.sy(qr[0])
        c2.rz(pi, qr[0])
        self.assertEqual(str(c2.draw()), str(unrolled.draw()))

    def test_decompose_u3(self):
        qr = QuantumRegister(1)
        circ = QuantumCircuit(qr)
        circ.u3(pi, pi / 2, pi / 4, qr[0])
        unrolled = pass_manager = PassManager([IonUnroller()]).run(
            circ, output_name=circ.name + " unrolled"
        )
        c2 = QuantumCircuit(qr)
        c2.rz(pi / 4, qr[0])
        c2.y(qr[0])
        c2.rz(pi / 2, qr[0])
        self.assertEqual(str(c2.draw()), str(unrolled.draw()))

    def test_decompose_cx(self):
        qr = QuantumRegister(2)
        circ = QuantumCircuit(qr)
        circ.cx(qr[0], qr[1])
        unrolled = pass_manager = PassManager([IonUnroller()]).run(
            circ, output_name=circ.name + " unrolled"
        )
        c2 = QuantumCircuit(qr)
        c2.sy(qr[0])
        c2.ms2(0, pi / 2, qr[0], qr[1])
        c2.sxd(qr[0])
        c2.sxd(qr[1])
        c2.syd(qr[0])
        self.maxDiff = 2000
        self.assertEqual(str(c2.draw()), str(unrolled.draw()))
