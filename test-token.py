import unittest
from token import Token

class TokenTestCase(unittest.TestCase):
    def testTokenEquality(self):
        """This checks the __eq__ operator for Token objects"""
        truth = Token(1, 0, "foo") == Token(1, 0, "foo")
        self.assertEqual(truth, True)

if __name__ == "__main__":
    unittest.main()
