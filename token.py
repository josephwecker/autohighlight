import re
import pprint
class Token:
    """A token contains a bit of text and the text coordinate where it
    came from."""
    text = ""
    line = 0
    col = 0
    def __init__(self, line, col, text):
        self.col = col
        self.line = line
        self.text = text

    def __str__(self):
        pp = pprint.PrettyPrinter()
        a = self.__dict__.copy()
        a['a-type-tag'] = "Token"
        return pp.pformat(a)
    
    def __repr__(self):
        return str(self)

    def must_be(self, str):
        if self.text != str:
            raise Exception("%d:%d: Expected '%s', got '%s'." % (self.line, self.col, str, self.text))

    def must_match(self, rex, expected):
        if not re.compile(rex).match(self.text):
            raise Exception("%d:%d: Expected a %s, got '%s' instead." % (self.line, self.col, expected, self.text))

    def __eq__(self, other):
        if other.__class__.__name__ == 'Token' and \
           other.col == self.col and \
           other.line == self.line and \
           other.text == self.text: return True
        return False

    def assert_symbol_name (self):
        if self.text[0] == "'": return True
        if not re.compile('^[a-zA-Z0-9_]+$').match(self.text):
            raise Exception("%d:%d: Expected a symbol, got %s." % ( self.line, self.col, self.text))

