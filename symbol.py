import pprint
from trace import funtrace
from trace import trprint
from trace import trenter
from trace import trleave
from context import Context
from production import Production
from utils import Set
from memoize import memoize

class Symbol:
    """This is the monster class. It does a lot of the
    theoretically-heavy lifting. A lot of its member functions were
    designed to be memoizable to provide speedups without having to
    worry about keeping member variables in sync."""
    def __init__(self, token):
        self.defining_token = token
        self.is_gla, self.is_lit, self.regex, self.productions = False, False, None, []
        self.GlobalSymbolDict = None

    def __str__(self):
        #rt = "#<Symbol %s gla: %s lit: %s regex: %s productions: " % \
        #     (self.defining_token, self.is_lit, self.is_gla, self.regex)
        #rt += "["
        #for product in self.productions:
        #    rt += "["
        #    for element in product:
        #        if element.__class__.__name__ != "Symbol": return str(element)
        #        else: rt += " S:" + element.defining_token.text
        #    rt += "]"
        #rt += "]"
        #return rt + ">"
        return "#S:%s" % self.defining_token.text
    
    def __repr__(self):
        return str(self)

    def __eq__(self,other):
        if other.__class__.__name__ != 'Symbol':
            return False
        return self.defining_token.text == other.defining_token.text

    def __hash__(self):
        return hash(self.defining_token.text)

    def isRoot(self):
        """Determine if there are other rules in the grammar
        containing this symbol as an element of a production"""
        for symbol in self.GlobalSymbolDict.values():
            if(symbol == self):
                continue
            for production in symbol.productions:
                if self in production.elements:
                    return False
        return True

    def get_terminal_equivalent_regexes(self):
        """If this symbol produces one or zero literals in all its
        productions, and all the expansions of the symbols in its
        productions, it's terminally equivalent. For terminally
        equivalent symbols, return a set of regular expressions so
        that every terminal this symbol can produce matches at least
        one of them."""
        if self.is_gla or self.is_lit:
            return self.regex
        regexes = Set()
        for production in self.productions:
            elements = production.elements
            if len(elements) > 1:
                return None
            elif len(elements) == 0:
                # XXX: Is this the right thing to do with an empty production???
                regexes.update([''])
            else:
                regex = elements[0].get_terminal_equivalent_regexes()
                if regex == None:
                    return None # We've determined this symbol is not terminal equivalent
                regexes.update(regex)
        return regexes

    def get_contexts(self,alreadySeen=()):
        """Returns a complete list of all the contexts for this symbol."""
        contexts = []
        for lhs_symbol in self.GlobalSymbolDict.values():
            for production in lhs_symbol.productions:
                # You HAVE to pair the self with the production
                # because you may have seen this production, but have
                # been looking for a different symbol in it.
                if (self,production) in alreadySeen:
                    # Avoid recursion
                    continue
                if self in production.elements:
                    new_contexts = self.get_contexts_for_production(production,alreadySeen)
                    # check for duplicate contexts resulting from similar contexts in different productions (ie BEGIN and END in mystery)
                    for new_context in new_contexts:
                        if new_context not in contexts:
                            contexts += [new_context]
        # TODO Try and unify contexts that share a left context or a right context to produce fewer coloring rules?
        return contexts

    def get_contexts_for_production(self,production,alreadySeen=()):
        """Gets all of the contexts for this symbol within this
        production. Will look up at the context of the lhs of the
        production if necessary (in the case that there is no symbol
        to the left or right of this symbol in the production.)"""
        contexts=[]
        alreadySeen = alreadySeen + ((self,production),)
        elements = production.elements
        for i in range(0,len(elements)):
            if self == elements[i]:
                if(len(elements) == 1): # the current production is a chain rule. Our context is our parent's context.
                    parentContexts = production.lhs.get_contexts(alreadySeen)
                    contexts += [Context(context.leftSymbols,self,context.rightSymbols) for context in parentContexts]
                elif i == 0: # we're at the beginning of the production. The left context is our parent's left context
                    parentContexts = production.lhs.get_contexts(alreadySeen)
                    parentLeftSymbols = Set()
                    for context in parentContexts:
                        parentLeftSymbols.update(context.leftSymbols)
                    contexts += [Context(parentLeftSymbols,self,Set([elements[i+1]]))]
                elif i == (len(elements)-1): # we're at the end of the production. The right context is our parent's right context
                    parentContexts = production.lhs.get_contexts(alreadySeen)
                    parentRightSymbols = Set()
                    for context in parentContexts:
                        parentRightSymbols.update(context.rightSymbols)
                    contexts += [Context(Set([elements[i-1]]),self,parentRightSymbols)]
                else: # we have symbols on either side of us
                    contexts += [Context( Set([elements[i-1]]), self, Set([elements[i+1]]) ) ]
        return contexts

    def getRightRegexes(self):
        """Get a set of regexes matching the right-most symbol in the
        complete expansion of this symbol."""
        return self.get_xmost_expansion_regexes(-1)

    def getLeftRegexes(self):
        """Get a set of regexes matching the left-most symbol in the
        complete expansion of this symbol."""
        return self.get_xmost_expansion_regexes(0)

    def get_xmost_expansion_regexes(self,direction,alreadySeen=()):
        """This does the real work of the two functions above. """
        xmost_regexes = Set()
        if self.get_terminal_equivalent_regexes() != None:
            return self.get_terminal_equivalent_regexes()
        for production in self.productions:
            elements = production.elements
            if len(elements) == 0:
                # XXX: It seems that when we find an empty production,
                # the expansion regexes come from the context of the
                # LHS symbol in the production.
                parent_regexes = Set()
                for context in production.lhs.get_contexts():
                    for symbol in context.leftSymbols:
                        parent_regexes.update(symbol.get_xmost_expansion_regexes(direction, alreadySeen + (self,)))
                # if there is no parent regexes, then we're at the start or end of the document
                if len(parent_regexes) == 0:
                    raise Exception("We're in deep shit: got a root of the document when we shouldn't have")
                xmost_regexes.update(parent_regexes)
            elif elements[direction] in alreadySeen:
                # XXX: Avoid recursion
                continue
            elif elements[direction].get_terminal_equivalent_regexes() == None:
                xmost_regexes.update(elements[direction].get_xmost_expansion_regexes(direction, alreadySeen + (self,) ))
            else:
                xmost_regexes.update(elements[direction].get_terminal_equivalent_regexes())
        return xmost_regexes


#funtrace(Symbol.get_contexts, [0,2])
#funtrace(Symbol.get_contexts_for_production, 4)
#funtrace(Symbol.merge_left_right_regexes, 3)
#funtrace(Symbol.getLeftRegexes, 1)
#memoize(Symbol.get_xmost_expansion_regexes)
#memoize(Symbol.get_contexts_for_production)
#funtrace(Symbol.get_terminal_equivalent_regexes, 1)
#funtrace(Symbol.get_xmost_expansion_regexes, 3)
#funtrace(Symbol.get_leftmost_expansion_regex, 1)
#funtrace(Symbol.get_rightmost_expansion_regex, 1)

if __name__ == "__main__":
    from token import Token
    from cStringIO import StringIO
    print "You're running the wrong file."
