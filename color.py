class Color:
    """Color is a data class representing a predefined or user-defined
    color."""
    def __init__(self, name, predefined=False):
        self.name, self.attrs, self.predefined = name, {}, predefined

