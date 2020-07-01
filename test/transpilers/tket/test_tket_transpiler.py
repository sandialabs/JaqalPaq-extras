import unittest, pytest

import jaqalpaq

pytket = pytest.importorskip("pytket")

from jaqalpaq.transpilers.tket import jaqal_circuit_from_tket_circuit
from jaqalpaq.generator import generate_jaqal_program
from numpy import pi
from jaqalpaq.core import CircuitBuilder
from pytket import Circuit


class PytketTranspilerTester(unittest.TestCase):
    def test_transpile_line_circuit(self):
        c = Circuit(1, 1)
        c.Rz(1, 0)
        c.add_barrier([0])
        c.Measure(0, 0)
        qsc = jaqal_circuit_from_tket_circuit(c)
        jcirc = CircuitBuilder()
        reg = jcirc.register("baseregister", 1)
        reg2 = jcirc.map("q", reg, slice(0, 1, 1))
        block = jcirc.block()
        block.gate("prepare_all")
        block.gate("Rz", reg2[0], pi)
        block = jcirc.block()
        block.gate("measure_all")
        self.assertEqual(
            generate_jaqal_program(jcirc.build()), generate_jaqal_program(qsc)
        )
