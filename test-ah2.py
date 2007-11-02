from ah import Autohighlight
from cStringIO import StringIO
import unittest

test1file = \
"""
{
} {
  document : document statement ';' .
  document : .
  statement : 'foo' .
} {
}
"""
class AhTestContexts(unittest.TestCase):
    ourTests = [ [ "statement", ['\\;|', '\\;'] ], \
                 [ "'foo'",     ['\\;|', '\\;'] ] \
               ]

    def setUp(self):
        global test1file
        self.ah = Autohighlight(StringIO(test1file))
        self.ah.parse()

    def checkContext(self,number):
        sym = self.ourTests[number][0]
        res = self.ourTests[number][1:]
        context = self.ah.GlobalSymbolDict[sym].get_context(self.ah.GlobalSymbolDict)
        self.assertEqual(res, context, "Contexts for %s are not as expected:\n%s\n%s" % (sym,res,context))

    def test0(self):
        self.checkContext(0)
    def test1(self):
        self.checkContext(1)

if __name__ == "__main__":
    unittest.main()

