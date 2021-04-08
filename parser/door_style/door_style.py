from ..utils.parsing_utils import sanitize_text


class DoorStyle:
    def __init__(
        self, style_name: str, species: str, y_range: range, text_lines: list
    ) -> None:
        self.name = style_name
        self.species = species
        self.ypos_range = y_range
        self.text_lines = text_lines
        self.doors = []
        self.drawers = []
        self.inside_profile = ""
        self.outside_profile = ""
        self._door_type_defs = ("BE", "WE", "S", "P")
        self._drawer_type_defs = ("FF", "DF")
        self._door_ypos = []
        self._drawer_ypos = []
        self._door_text_lines = set()
        self._drawer_text_lines = set()
        self._get_door_drawer_ypos()
        self._get_door_drawer_text_lines()
        self._group_data_into_dicts_by_ypos()
        self._get_outside_profile()
        self._get_inside_profile()

    def _get_door_drawer_ypos(self) -> None:
        self._door_ypos = set(
            [
                line.y0
                for line in self.text_lines
                if line.get_text().replace("\n", "") in self._door_type_defs
            ]
        )

        self._drawer_ypos = set(
            [
                line.y0
                for line in self.text_lines
                if line.get_text().replace("\n", "") in self._drawer_type_defs
            ]
        )

    def _get_door_drawer_text_lines(self) -> None:
        self._door_text_lines = [
            line for line in self.text_lines if line.y0 in self._door_ypos
        ]

        self._drawer_text_lines = [
            line for line in self.text_lines if line.y0 in self._drawer_ypos
        ]

    def _group_data_into_dicts_by_ypos(self) -> None:
        door_dict = {}
        drawer_dict = {}

        for line in self._door_text_lines:
            if line.y0 not in door_dict:
                door_dict[line.y0] = [line]
            else:
                door_dict[line.y0].append(line)

        for line in self._drawer_text_lines:
            if line.y0 not in drawer_dict:
                drawer_dict[line.y0] = [line]
            else:
                drawer_dict[line.y0].append(line)

        for ypos in door_dict:
            door = {"size": "", "qty": ""}
            for line in door_dict[ypos]:
                text = sanitize_text(line)
                if line.x0 > 280:
                    continue
                if "x" in text:
                    door["size"] = text
                else:
                    door["qty"] = text

            door_dict[ypos] = door

        for ypos in drawer_dict:
            drawer = {"size": "", "qty": ""}
            for line in drawer_dict[ypos]:
                text = sanitize_text(line)
                if line.x0 > 280:
                    continue
                if "x" in text:
                    drawer["size"] = text
                else:
                    drawer["qty"] = text

            drawer_dict[ypos] = drawer

        self.doors = list(door_dict.values())
        self.drawers = list(drawer_dict.values())

    def _get_outside_profile(self) -> None:
        for line in self.text_lines:
            if "Outside Edge Profile" in line.get_text():
                self.outside_profile = (
                    line.get_text().replace("\n", "").split(":")[1].strip()
                )

    def _get_inside_profile(self) -> None:
        for line in self.text_lines:
            if "Inside Edge Profile" in line.get_text():
                self.inside_profile = (
                    line.get_text().replace("\n", "").split(":")[1].strip()
                )
