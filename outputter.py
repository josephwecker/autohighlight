class Outputter:
    """An abstract class defining the interface to the outputter
    classes."""
    def appendColorDefinition(self, color):
        raise NotImplemented()

    def appendLiteral(self, color, literal):
        raise NotImplemented()

    def appendMapping(self, color, contexts): # contexts: List<Context>
        raise NotImplemented()

    def getBuffer(self):
        raise NotImplemented()
