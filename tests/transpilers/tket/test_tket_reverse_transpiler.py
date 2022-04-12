import unittest, pytest

import jaqalpaq

pytket = pytest.importorskip("pytket")

from jaqalpaq.core import CircuitBuilder
from jaqalpaq.transpilers.tket import JaqalBackend, tket_circuit_from_jaqal_circuit
from pytket import Circuit
from math import pi
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
        tkc = tket_circuit_from_jaqal_circuit(built)
        jb = JaqalBackend("emulator")
        compiled = jb.get_compiled_circuit(tkc)
        handle = jb.process_circuit(compiled, n_shots=16)
        for shot in jb.get_result(handle).get_shots():
            self.assertEqual(shot[0], shot[1])
