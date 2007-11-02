from utils import Set
import pprint
import re
from color import Color
from tokenize import Tokenizer
from token import Token
from symbol import Symbol
from mapping import Mapping
from production import Production

pp = pprint.PrettyPrinter()

class Autohighlight:
    """The autohighlight class encapsulates all the state of the
    highlighter at any given moment"""
    def __init__(self, file):
        self.GlobalSymbolDict = {} # Symbol table
        self.ColorDefinitions = self.getPredefinedColors() # Color definition table - maps color names(as strings) to Color objects
        self.OrderedColorMappings = [] # A list of color Mapping objects in textual order (contents of thir section of input)
        self.tokenizer = None # The token generator
        if type(file).__name__ == 'str': self.tokenizer = Tokenizer(open(file)) # behave nicely when given a filename instead of a stream
        else: self.tokenizer = Tokenizer(file)

    def getPredefinedColors(self):
        """Produce hash of Color objects representing the predefined colors"""
        colorNames = [ 'Comment', \
                       'Constant', \
                       'String', \
                       'VariableName', \
                       'FunctionName', \
                       'Keyword', \
                       'Type', \
                       'None', \
                       'Error' \
                     ]
        colors = {}
        for colorName in colorNames:
            colors[colorName]=Color(Token(None,None,colorName),True)
        return colors

    def promote_productions(self):
        """Convert all the elements of products from tokens into
        symbols, meanwhile checking that all of the elements are
        existing symbols. This is name analysis in action: because
        symbol names have Algol scoping inside the concrete grammar
        portion of the input file, we wait until the whose shebang is
        parsed before attempting to promote tokens into symbols."""
        for sym in self.GlobalSymbolDict.values():
            for production in sym.productions:
                elements = production.elements
                if len(elements) > 0: # An empty production has no tokens to promote
                    firstToken = elements[0]
                    for i in range(0, len(elements)):
                        if re.compile("^'").match(elements[i].text): # If the element is a literal, no name analysis needs to be done
                            elements[i] = Symbol(elements[i])
                            elements[i].is_lit = True
                            elements[i].regex = Set(re.escape(elements[i].defining_token.text[1:-1]))
                            self.GlobalSymbolDict[elements[i].defining_token.text]=elements[i]
                        else: # Do name analysis: check if the symbol is used without being defined.
                            try:
                                elements[i] = self.GlobalSymbolDict[elements[i].text]
                            except KeyError, e:
                                raise Exception("Production for %s beginning at %d,%d: %s is not a symbol." % \
                                                (sym.defining_token.text, firstToken.line, firstToken.col, elements[i].text))

    def parse_lexical_symbols(self):
        """Given that the token generator is at the beginning of the
        lexical symbol specifications, read a series of lexical symbol
        specifications, doing name and basic type analysis on the fly."""
        stack = []
        self.tokenizer.next().must_be('{')
        for token in self.tokenizer:
            stack += [ token ]
            if token.text == ".":
                stack[0].assert_symbol_name()
                stack[1].must_be(':')
                stack[2].must_match('^\\$', "regular expression")
                ## Name analysis
                if stack[0].text in self.GlobalSymbolDict:
                    originalDef = self.GlobalSymbolDict[stack[0].text].defining_token
                    raise Exception("Symbol %s redefined at %d,%d. Originally at %d,%d" % (stack[0].text, stack[0].line, stack[0].col, \
                                                                                           originalDef.line, originalDef.col))
                s = Symbol(stack[0])
                s.is_gla = True
                s.regex = Set(stack[2].text[1:])
                self.GlobalSymbolDict[stack[0].text] = s
                stack = []
            elif token.text == "{":
                raise Exception("Unexpected %s" % token)
            elif token.text == "}":
                if len(stack) > 1: raise Exception("Unfinished lexical specification beginning with %s" % stack[0])
                return
            else: pass

    def parse_cst(self):
        """Given that the token generator is positioned at the start
        of the concrete grammar, read rules. After this routine
        completes, each symbol in the GlobalSymbolDict has a set of
        productions that contain Tokens, not symbols. Conversion from
        tokens to symbols happens in promote_productions."""
        stack = []
        self.tokenizer.next().must_be('{')
        for token in self.tokenizer:
            stack += [ token ] # Build a stack to process
            if token.text == ".":
                # We've got a rule to process. Start by determining correct syntax.
                stack[1].must_be(':')
                ## Name analysis
                stack[0].assert_symbol_name()
                production_elements = stack[2:-1]
                for element in production_elements:
                    element.assert_symbol_name()
                if stack[0].text in self.GlobalSymbolDict: # Redefined lexical sym or add a new production?
                    existingSymbol = self.GlobalSymbolDict[stack[0].text]
                    if existingSymbol.is_gla:
                        raise Exception("Lexical Symbol %s redefined at %d,%d. Originally at %d,%d" % \
                                (stack[0].text, stack[0].line, stack[0].col, \
                                 existingSymbol.defining_token.line, existingSymbol.defining_token.col))
                    existingSymbol.productions += [Production(existingSymbol,production_elements)]
                else: # Brand new symbol occurrence
                    s = Symbol(stack[0])
                    s.is_gla = False
                    s.productions = [Production(s,production_elements)]
                    self.GlobalSymbolDict[stack[0].text] = s
                stack = []
            elif token.text == "{":
                raise Exception("Unexpected %s" % token)
            elif token.text == "}":
                if len(stack) > 1: raise Exception("Unfinished lexical specification beginning with %s" % stack[0])
                #pp = pprint.PrettyPrinter()
                #pp.pprint(self.GlobalSymbolDict)
                return
            else: pass

    def mkColor(self, name):
        """Control is transferred here in order to read a color
        specification from the token generator. Does basic name
        analysis to determine if valid font attributes are used."""
        known_attrs = [ 'font-family', 'font-style', 'font-weight', 'font-size', 'text-decoration', 'color', 'background-color' ]
        stack = []
        color = Color(name)
        for token in self.tokenizer:
            if token.text == ";":
                stack[0].assert_symbol_name
                if stack[0].text not in known_attrs: raise Exception("%d:%d: Unknown color attribute %s" % (stack[0].line, stack[0].col, stack[0].text))
                stack[1].must_be(":")
                stack[2].must_match("^\w", "%d:%d: Expected a color attribute value instead of %s" % (stack[2].line, stack[2].col, stack[2].text))
                color.attrs[stack[0].text] = stack[2].text
                stack = []
            elif token.text == "}":
                return color
            else:
                stack += [token]
        raise Exception("%d:%d: End-of-file reached while scanning color %s defined here." % (name.line, name.col, name.text))

    def parse_color(self):
        """Given that the token generator is at the beginning of the
        coloring section, read color definitions and coloring requests"""
        begin = self.tokenizer.next()
        begin.must_be('{')
        for name in self.tokenizer:
            if name.text == '}': return
            name.must_match("^[A-Za-z]", "%d:%d: Expected a color name, got %s instead." % (name.line, name.col, name.text))
            midpunct = self.tokenizer.next()
            if midpunct.text == "{":
                color = self.mkColor(name)
                if color in self.ColorDefinitions:
                    raise Exception("%d:%d: Color %s has already been defined." % (name.line, name.col, name.text))
                self.ColorDefinitions[name.text] = color
            elif midpunct.text == ':':
                stack = []
                for token in self.tokenizer:
                    if token.text == ".":
                        self.OrderedColorMappings += [Mapping(name,stack)]
                        break
                    elif token.text == "}": raise Exception("%d:%d: Color section ended while defining mapping for color %s" % (name.line, name.col, name.text))
                    try:
                        stack += [ self.GlobalSymbolDict[token.text] ]
                    except:
                        raise Exception("%d:%d: Literal %s does not occur in the grammar" % (token.line, token.col, token.text))
                        
            elif midpunct.text == '}': raise Exception("%d:%d: Coloring section ended unexpectedly here." % (token.line, token.col))
            else: raise Exception("%d:%d: Expected : or {, not %s" % (midpunct.line, midpunct.col, midpunct.text))
        raise Exception("%d:%d: Unexpected end-of-file while scanning color definition section beginning here." % (begin.line, begin.col))
    
    def check_color_scoping(self):
        """Since color names have algol scoping, name analysis must be
        done after all the color definitions have been read."""
        for mapping in self.OrderedColorMappings:
            if mapping.token.text not in self.ColorDefinitions:
                raise Exception("%d:%d Color %s is never defined" % (mapping.token.line, mapping.token.col, mapping.token.text))

    def check_for_multiple_roots(self):
        """Determine whether the cst has multiple roots."""
        roots = self.get_roots()
        if len(roots)!=1:
            raise Exception("Found multiple roots: %s"%roots)

    def get_roots(self):
        """Get the roots of the grammar as a list"""
        roots = []
        for symbol in self.GlobalSymbolDict.values():
            if symbol.isRoot():
                roots += [symbol]
        return roots

    def parse(self):
        """Do all the parsing and basic name/type analysis, reserving
        the hard colorability stuff for output routines."""
        self.parse_lexical_symbols()
        self.parse_cst()
        self.promote_productions()
        self.parse_color()
        self.check_color_scoping()
        for sym in self.GlobalSymbolDict.values():
            sym.GlobalSymbolDict = self.GlobalSymbolDict
        self.create_root_symbols()
        self.check_for_multiple_roots()

    def create_root_symbols(self):
        """Insert magical symbols above the root of the grammar in
        order to match the beginning and end of the sample."""
        RootSymbol = Symbol(Token(None,None,'R00t.Symbol'))
        RootSymbol.GlobalSymbolDict=self.GlobalSymbolDict
        StartDocSymbol = Symbol(Token(None,None,'%^'))
        StartDocSymbol.regex = Set('%^')
        StartDocSymbol.is_lit = True
        StartDocSymbol.GlobalSymbolDict=self.GlobalSymbolDict
        EndDocSymbol = Symbol(Token(None,None,'%$'))
        EndDocSymbol.regex = Set('%$')
        EndDocSymbol.is_lit = True
        EndDocSymbol.GlobalSymbolDict=self.GlobalSymbolDict
        RootSymbol.productions = [Production(RootSymbol,[StartDocSymbol]+self.get_roots()+[EndDocSymbol])]
        self.GlobalSymbolDict['R00t.Symbol'] = RootSymbol #XXX this is a nasty hack
        self.GlobalSymbolDict['%^']=StartDocSymbol
        self.GlobalSymbolDict['%$']=EndDocSymbol
    
    def output(self,outputter):
        """This function takes an outputter object and feeds it the
        user's coloring requests."""
        for colorName,color in self.ColorDefinitions.iteritems():
            if color.predefined: continue
            outputter.appendColorDefinition(color)

        for mapping in self.OrderedColorMappings:
            colorName = mapping.token.text
            for symbol in mapping.mappings:
                if symbol.get_terminal_equivalent_regexes() == None:
                    raise Exception("Symbol %s is not colorable because it is not terminal equivalent" % \
                                            symbol.defining_token.text)
                print "Generating rules to color %s as %s" % (symbol.defining_token.text, colorName)
                color = self.ColorDefinitions[colorName]
                if(symbol.is_lit):
                    #outputter.appendLiteral(color, symbol.defining_token.text[1:-1] )
                    outputter.appendMapping(color, symbol.get_contexts())
                else:
                    outputter.appendMapping(color, symbol.get_contexts())
        return outputter.getBuffer()
