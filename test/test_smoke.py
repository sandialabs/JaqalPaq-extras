import unittest


class SmokeTester(unittest.TestCase):
    def test_smoketest(self):
        # Simple test to confirm that we can import both the
        # man jaqal-pup packages, and the extras here.
        import jaqal.core
        import jaqal
        import jaqal.transpilers
        import jaqal.parser
