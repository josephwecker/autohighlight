from ah import Autohighlight
from cStringIO import StringIO
import unittest
from utils import Set
from context import Context

test1file = \
      """
{
  int: $[0-9]+ .
  id: $[A-Za-z][-A-Za-z0-9_]* .
} {
  document : document statement ';' .
  document : .
  statement: assignment .
  statement: declaration .
  statement: output .
  assignment: idUse '=' expr .
  expr: idUse .
  expr: int .
  declaration: 'var' idDef ':' typeUse .
  idUse : id .
  idDef : id .
  typeUse : id.
  output: 'Print' expr .
} {
  TypeColor {
    color: blue;
  }
  TypeColor: typeUse .
  IdDefColor: idDef .
  IdDefColor {
    color: red;
  }
  keyword_face {
    color: green;
  }
  keyword_face: 'var' 'Print' .
}
"""

class AhTestContexts(unittest.TestCase):
    ourTests = [ [ "idUse", ['\\;|%^', '\\='], ['\\=', '\\;'], ['Print', '\\;'] ],\
                 [ "':'", ['[A-Za-z][-A-Za-z0-9_]*', '[A-Za-z][-A-Za-z0-9_]*'] ],\
                 [ "int", ['\\=', '\\;'], ['Print', '\\;'] ],\
                 [ "idDef", ['var', '\\:'] ],\
                 [ "typeUse", ['\\:', '\\;'] ],\
                 [ "expr", ['\\=', '\\;'], ['Print', '\\;'] ],\
                 [ "';'", ['[A-Za-z][-A-Za-z0-9_]*|[0-9]+|[A-Za-z][-A-Za-z0-9_]*|[A-Za-z][-A-Za-z0-9_]*|[0-9]+', '[A-Za-z][-A-Za-z0-9_]*|var|Print|%$'] ],\
                 [ "'Print'", ['\\;|%^', '[A-Za-z][-A-Za-z0-9_]*|[0-9]+'] ],\
                 [ "'='", ['[A-Za-z][-A-Za-z0-9_]*', '[A-Za-z][-A-Za-z0-9_]*|[0-9]+'] ],\
                 [ "id", ['\\;|%^', '\\='], ['\\=', '\\;'], ['Print', '\\;'], ['var', '\\:'], ['\\:', '\\;'] ],\
                 [ "'var'", ['\\;|%^', '[A-Za-z][-A-Za-z0-9_]*'] ] ]

    def setUp(self):
        global test1file
        self.ah = Autohighlight(StringIO(test1file))
        self.ah.parse()
        self.gsd=self.ah.GlobalSymbolDict

    def checkContext(self,number):
        sym = self.ourTests[number][0]
        expected = []
        for context in self.ourTests[number][1:]:
            setted_context = []
            for regex in context:
                setted_context += [ Set(regex.split("|")) ]
            expected += [setted_context]
        contexts = self.ah.GlobalSymbolDict[sym].get_contexts(self.ah.GlobalSymbolDict)
        res = [ [context.getLeftRegexes(), context.getRightRegexes()] for context in contexts ]
        self.assertEqual(res, expected, "Contexts for %s are not as expected:\n%s\n%s" % (sym,res,expected))

    def test0(self):
        self.checkContext(0)
    def test1(self):
        self.checkContext(1)
    def test2(self):
        self.checkContext(2)
    def test3(self):
        self.checkContext(3)
    def test4(self):
        self.checkContext(4)
    def test5(self):
        self.checkContext(5)
    def test6(self):
        self.checkContext(6)
    def test7(self):
        self.checkContext(7)
    def test8(self):
        self.checkContext(8)
    def test9(self):
        self.checkContext(9)
    def test10(self):
        self.checkContext(10)

    def testContextOfSemicolon(self):
        sym = self.gsd["';'"]
        res = sym.get_contexts(self.ah.GlobalSymbolDict)
        expected = [Context(Set(self.gsd["statement"]), sym, Set(self.gsd["statement"],self.gsd['%$']) )]
        self.assertEqual(res, expected, "Contexts for %s are not as expected:\n%s\n%s" % (sym,res,expected))

    def testIsRoot(self):
        roots = []
        for symbol in self.gsd.values():
            if symbol.isRoot():
                roots += [symbol]
        self.assertEqual(len(roots),1,"Multiple roots found: %s"%roots)


#    def testStatementLeftRightInDocument(self):
#        gsd = self.ah.GlobalSymbolDict
#        regexes = gsd['statement'].get_left_right_regexes( gsd['document'], gsd['document'].productions[0], 1, [])
#        self.assertEqual(regexes,[['\\;|'], ['\\;']])
#
#    def testDocumentXMostExpansionRegex(self):
#        gsd = self.ah.GlobalSymbolDict
#        regexes = gsd['document'].get_xmost_expansion_regex(-1,{})
#        self.assertEqual(regexes,'\\;|')

if __name__ == "__main__":
    unittest.main()

