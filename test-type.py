from utils import Set
from autohighlight import Autohighlight
from cStringIO import StringIO
from context import Context
import unittest
import pprint

test1file = \
      """
{ } {
    idn: 'idn' .
    Type: 'OF' Type .
    Type: idn .
    Procedure: ':' Type '=' .
} { }
"""

class AhTestContexts(unittest.TestCase):
    def setUp(self):
        global test1file
        self.ah = Autohighlight(StringIO(test1file))
        self.ah.parse()

    def testGetContextsForIdn(self):
        gsd = self.ah.GlobalSymbolDict
        expected = [Context(Set([gsd["'OF'"]]),gsd['idn'],Set([gsd["'='"]])), \
                Context(Set([gsd["':'"]]),gsd['idn'],Set([gsd["'='"]])) ]
        symbol = gsd['idn']
        contexts = symbol.get_contexts()
        self.assertEqual(contexts, expected, "Contexts for %s are not as expected:\n%s\n%s" % ('t',contexts,expected))

if __name__ == "__main__":
    unittest.main()

