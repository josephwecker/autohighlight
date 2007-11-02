from __future__ import generators
import re
from token import Token

class TokenizerException (Exception):
    text = "Token error on '%s'."
    def __init__(self, line, col, char): self.line, self.col, self.char = line, col, char
    def __str__(self):
        return ("%d:%d: " % (self.line, self.col)) + (self.text % self.char)
    def __repr__(self):
        return "#<%s Exception at %s>" % (self.__class__.__name__, str(self))

class EofInString (TokenizerException):
    def __init__(self, line, col): self.line, self.col = line, col
    def __str__(self): return "%d:%d: End-of-file occurred while reading string beginning here." % (self.line, self.col)

class UnexpectedCharacter (TokenizerException):
    text = "Unexpected character: '%s'."

class Tokenizer:
    """This class is a generator, meaning it has a next() method that
    gets called when an object of this class is used as the sequence
    in for loop. Tokenizer objects track the text coordinates and
    build Tokens using a finite state machine."""
    def __init__(self, stream):
        self.stream = stream
        self.line = 1 # Tracks the current line number
        self.col = 0 # Tracks the current column number
        self.state = 0 # Tokenizer finite-state-machine's current state

    def __iter__(self): return self

    def setCursor(self, line, col):
        """Sets the text coordinates. This doesn't seem like it should
        need its own function, but experience proves it's a nice place
        to hook into while debugging."""
        self.line, self.col = line, col

    def transition(self):
        """Examine self.char to determine the next transition to take.
        Once this transition is identified, interpret the list of
        actions to take along the transition. Each action produces a
        return value. The last action's return value is returned from
        this function."""
        statedef = self.transitions[self.state]
        for path in statedef:
            pat, dest = path[:2]
            retval = None
            if type(pat).__name__ == "str" and pat == self.char or \
               type(pat).__name__ == "SRE_Pattern" and pat.match(self.char): # Regexp objects match like regexps
                for action in path[2:]:
                    retval = action(self) # Keep the return value to return from ourselves
                self.state = dest
                return retval
        raise Exception("No matching path for char %s from state %d." % (self.char, self.state))

        
    def c(e): return re.compile(e, re.M | re.S)
    ### What comes next is the list of actions it's possible to take
    ### on transition from one state to another. When an action
    ### returns a Token, then next() returns also. Kind of kludgy, but
    ### with python's poor coroutining support, it's the best we can
    ### do.
    def add(self):
        """Add the character to the token being built up"""
        self.token += self.char
        return None
    def tok(self):
        """Create a token and return it"""
        return Token(self.sline, self.scol, self.token)
    def push(self):
        """Push the character back onto the input buffer, consider it
        again later. Updates the text coordinates"""
        #print "PUSHING!!!!!!!"
        if self.char == '': return
        self.setCursor(self.line, self.col - 1)
        if self.col < 0 or self.char == '\n': self.setCursor(self.line - 1, 0)
        #print "DONE PUSHING!!!!!!"
        self.stream.seek(-1, 1)
    def stop(self):
        """This happens when we reach EOF"""
        raise StopIteration()
    def noop(self):
        """Do nothing"""
        return None
    def reset(self):
        """Reset the start-line and start-col to the current text
        position. This happens when transitioning from whitespace to
        something that will end up being a token. These start-*
        coordinates are passed to Token to get the text coordinates of
        the first character of the token's definition"""
        self.sline, self.scol = self.line, self.col
        #print "RESET Token must begin at (%d,%d)" % (self.line, self.col)
        return None
    def strangechar(self):
        """Raise an error if a character is found that doesn't match
        the token being read"""
        raise UnexpectedCharacter(self.line, self.col, self.char)
    def endinstr(self):
        """Bail out when EOF in a string is found."""
        raise EofInString(self.sline, self.scol)

    # Here's the state "table". It's not really a table, its a
    # decision list. Each element <i> of transitions is a list of
    # transitions out of state <i>. Each transition a tuple consisting
    # of a test, the next state, and any number of actions to take
    # before transitioning to the new state. The <c> function produces
    # a regular expression object from its argument.
    transitions = [ \
      # state 0: initial state \
      [ (c("[A-Za-z]"), 1, reset, add), ('', 0, stop), (c('[0-9]'), 5, reset, add), ('$', 2, reset, add), ("'", 3, reset, add), (c('[][{}:;.]'), 0, reset, add, tok), (c('\s'), 0, noop), (c('.'), 0, strangechar) ], \
      # state 1: accumulating identifiers \
      [ ( c("[-A-Za-z0-9_]"), 1, add), ('', 0, tok), (c('.'), 0, push, tok) ], \
      # state 2: accumulating regexes \
      [ ('', 0, push, tok), (c('\s'), 0, tok), (c('.'), 2, add) ], \
      # state 3: accumulating strings \
      [ ('\\', 4, add), ("'", 0, add, tok), ('', 0, endinstr), (c('.'), 3, add) ], \
      # state 4: escaping strings \
      [ ('', 0, endinstr), (c('.'), 3, add) ], \
      # state 5: integers \
      [ (c("[0-9]"), 5, add), ('', 0, tok), (c('.'), 0, push, tok) ] \
      ]


    def next(self):
        """When the generator is used in a for loop, this method is
        called repeatedly to get values. Iteration stops when somebody
        raises a StopIteration exception"""
        self.token = ""
        self.sline = self.line # The line the currently-being-built token starts on
        self.scol = self.col # The column the currently-being-built token starts on
        self.char = '' # The character under consideration

        while True:
            self.char = self.stream.read(1)
            # Do a state-machine transition
            retval = self.transition()
            # Text coordinate upkeep: detect pushes.
            if self.char == '\n':
                self.setCursor(self.line + 1, 0)
            else: self.setCursor(self.line, self.col + 1)
            if retval: return retval # Keep considering new characters until a token is built.
            if self.char == '': raise StopIteration()
        # end next()

if __name__ == "__main__":
    from cStringIO import StringIO
    import unittest
    class LocalTokenTest(unittest.TestCase):
        def testParse(self):
            t = Tokenizer(StringIO("5.6"))
            self.assertEqual([Token(1, 0, "5"), Token(1, 1, "."), Token(1, 2, "6")], [ token for token in t ])
        
        def testNewlineDelimitedIntegers(self):
            """5\n6 => "5" "6": Another edge case"""
            t = Tokenizer(StringIO("5\n6"))
            self.assertEqual([Token(1, 0, "5"), Token(2, 0, "6") ], [ token for token in t ])

        def testTokenizeMashedIdAndRegex(self):
            """id$foo => "id" "foo" """
            tl = [ token for token in Tokenizer(StringIO("id$foo")) ]
            self.assertEqual([Token(1,0,"id"),Token(1,2,"$foo")], tl)

    unittest.main()
