class DoorStyle:
    def __init__(self, style_name: str, species: str, y_range: tuple) -> None:
        self.name = style_name
        self.species = species
        self.ypos_range = y_range
        self.line_objs = []
        self.doors = []
        self.drawers = []
        self.inside_profile = ""
        self.outside_profile = ""
        self._door_types_defs = ("BE", "WE", "S", "P")
        self._drawer_type_defs = ("FF", "DF")
        self._door_ypos = []
        self.drawer_ypos = []