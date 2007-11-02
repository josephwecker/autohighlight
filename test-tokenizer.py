import unittest
from cStringIO import StringIO
from tokenize import *
from token import Token

class TokenizerTestCase(unittest.TestCase):
    def tokenList(self, string):
        try:
            tokenizer = Tokenizer(StringIO(string))
            return [ token for token in tokenizer ]
        except TokenizerException, e:
            return e
    
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testTokenizeString(self):
        """Checks for correct basic string tokenization"""
        self.assertEqual([Token(1, 0, "'abcd'")], self.tokenList("'abcd'"))

    def testTokenizeEscapedString(self):
        tl = self.tokenList("'abc\\'de'")
        self.assertEqual([Token(1, 0, "'abc\\'de'")], tl)

    def testTokenizeUnfinishedString(self):
        """Is an error signalled for unfinished strings?"""
        tl = self.tokenList("'abc")
        self.assertEqual("EofInString", tl.__class__.__name__)

    def testFloatsParsedAsTwoIntegers(self):
        """There are no floats, so things that look like floats should
        parse like integers"""
        tl = self.tokenList("5.6")
        self.assertEqual([Token(1,0,"5"), Token(1,1,"."),Token(1,2,"6")], tl)

    def testIntegerFollowedByPeriod(self):
        """5. => "5" ".": This seems to cause trouble"""
        tl = self.tokenList("5.")
        self.assertEqual([Token(1,0,"5"), Token(1,1,".")],tl)

    def testNewlineDelimitedIntegers(self):
        """5\n6 => "5" "6": Another edge case"""
        tl = self.tokenList("5\n6")
        self.assertEqual([Token(1,0,"5"), Token(2,0,"6")],tl)

    def testIntegerFollowedByIdentifier(self):
        """5a => "5" "a": Another state transition edge case"""
        tl = self.tokenList("5a")
        self.assertEqual([Token(1,0,"5"),Token(1,1,"a")],tl)

    def testIdFollowedByInteger(self):
        """a. => "a" ".": Edge case similar to previous"""
        tl = self.tokenList("a.")
        self.assertEqual([Token(1,0,"a"),Token(1,1,".")],tl)

    def testTokenizeMashedIdAndRegex(self):
        """id$foo => "id" "foo" """
        tl = self.tokenList("id$foo")
        self.assertEqual([Token(1,0,"id"),Token(1,2,"$foo")], tl)

    def testTokenizeMashedIdsAndPunct(self):
        """This should return 5 symbols"""
        tl = self.tokenList("id.def.foo")
        want = [Token(1,0,"id"),Token(1,2,"."),\
                Token(1,3,"def"),Token(1,6,"."),\
                Token(1,7,"foo")]
        self.assertEqual(want, tl)

    def testInteger(self):
        tl = self.tokenList("12")
        self.assertEqual([Token(1,0,"12")],tl)

    def testPunctuationAfterWhitespace(self):
        tl = self.tokenList("\n.")[0]
        self.assertEqual(2, tl.line)
        self.assertEqual(0, tl.col)

    def testValidStartTokens(self):
        valid = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        valid += "{}[].:0123456789"
        for inichar in valid:
            self.assertEqual([Token(1, 0, inichar)], self.tokenList(inichar))

    def testInvalidStartTokens(self):
        invalid = "-_`~!@#%^&*()+=\|?<>,"
        for badchar in invalid:
            tl = self.tokenList(badchar)
            self.assertEqual("UnexpectedCharacter", tl.__class__.__name__)

if __name__ == "__main__":
    unittest.main()
