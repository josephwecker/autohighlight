class Mapping:
    """A mapping represents a coloring request given by the user in
    the Ah section of the input file."""
    def __init__(self, token, mappings):
        self.token = token # Token giving the color name
        self.mappings = mappings # a list of the items to color with this color
