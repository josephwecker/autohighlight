from StringIO import StringIO

class LispFormatStream (StringIO):
    def __init__(self): self.buffer, self.indent = StringIO(), [0]
    def getvalue(self): return self.buffer.getvalue()
    def prin(self, str):
        col = self.indent[-1]
        #self.buffer.write(" "*col)
        for char in str:
            self.buffer.write(char)
            if char == "(":
                self.indent += [col]
            elif char == ")":
                self.indent = self.indent
            col += 1
        self.buffer.write("\n")

if __name__ == "__main__":
    import unittest
    class LispFormatStreamTest(unittest.TestCase):
        def setUp(self):
            self.lfs = LispFormatStream()
        def testEasy(self):
            self.lfs.prin("(plain)")
            self.lfs.prin("(plain)")
            self.assertEqual("(plain)\n(plain)\n", self.lfs.getvalue())
        def testBreakOpen(self):
            self.lfs.prin("(plain")
            self.lfs.prin("(plain))")
            self.assertEqual("(plain\n  (plain)\n", self.lfs.getvalue())
        def testBreakOpenSecond(self):
            self.lfs.prin("(plain second")
            self.lfs.prin("foo)")
            self.assertEqual("(plain second\n       foo)\n", self.lfs.getvalue())
        def testBreakDoubleOpen(self):
            self.lfs.prin("'((foo bar)")
            self.lfs.prin("(foo bar))")
            self.assertEqual("'((foo bar)\n  (foo bar))\n", self.lfs.getvalue())
    unittest.main()
