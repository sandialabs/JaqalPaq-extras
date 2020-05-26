import unittest


class SmokeTester(unittest.TestCase):
    def test_smoketest(self):
        # Simple test to confirm that we can import both the
        # man jaqal-pup packages, and the extras here.
        import jaqalpaq.core
        import jaqalpaq
        import jaqalpaq.transpilers
        import jaqalpaq.parser
