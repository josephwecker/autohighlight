class Production:
    """Represents a rule in the CON section of the input file."""
    def __init__(self,lhs,elements):
        self.lhs = lhs
        self.elements = elements

    def __hash__(self):
        return hash(str(self))

    def __str__(self):
        return "#P<%s: %s>" % (self.lhs.defining_token.text, ' '.join([str(element.defining_token.text) for element in self.elements]))

    def __repr__(self):
        return str(self)

    def __eq__(self,other):
        if self.elements != other.elements:
            return False
        if self.lhs != other.lhs:
            return False
        return True
