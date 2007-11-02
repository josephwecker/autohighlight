from utils import Set
from autohighlight import Autohighlight
from cStringIO import StringIO
from context import Context
import unittest

test1file = \
      """
{
} {
    a: 'a' .
    c: 'c' .
    d: 'd' .
    e: 'e' .
    q: 'q' .
    t: 't' .
    s: 's' .
    x: a b c .
    y: d b e .
    b: q t .
    b: q s .
} {
}
"""

class AhTestContexts(unittest.TestCase):
    def setUp(self):
        global test1file
        self.ah = Autohighlight(StringIO(test1file))
        self.ah.parse()

    def testGetContextsForQ(self):
        gsd = self.ah.GlobalSymbolDict
        expected = [Context(Set([gsd['a'],gsd['d']]),gsd['q'],Set([gsd['t']])), \
                    Context(Set([gsd['a'],gsd['d']]),gsd['q'],Set([gsd['s']])) ]
        contexts = gsd['q'].get_contexts()
        self.assertEqual(contexts, expected, "Contexts for %s are not as expected:\n%s\n%s" % ('q',contexts,expected))

if __name__ == "__main__":
    unittest.main()

