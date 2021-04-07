from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer
from icecream import ic

from .utils.parsing_utils import (
    get_formatted_text_from_line_obj,
    get_start_and_end_ypos,
)
from .door_style.door_style import DoorStyle


class JobSummary:
    def __init__(self, pdf, name) -> None:
        self.pages = 0
        self.name = name
        self.order_date = ""
        self.door_styles = []
        self.doors = []
        self.drawers = []
        self._door_ypos = []
        self._drawer_ypos = []
        self._text_lines = []
        self._get_text_lines(pdf)
        self._reformat_ypos()
        self._get_job_date()
        self._get_doorstyle_ypos()
        self.get_doorstyle_objs_from_tuples()
        # self._split_lines_into_sections(self._text_lines)
        # self._get_style_sizes_and_totals()

    # def __repr__(self) -> str:
    #     return f"Job name: {self.name} Order date: {self.order_date}\n"

    def _get_name_in_brackets(self, base_str: str) -> str:
        """
        Gets the job name from the parens in the text object
        """
        opening = base_str.index("(")
        closing = base_str.index(")")
        return base_str[opening + 1 : closing]

    def _get_text_lines(self, pdf) -> None:
        """
        Extract lines of text from generated door report.
        Store the text objs in a list of tuples with tup[0] being the page number
        and tup[1] being the object
        """
        for page_layout in extract_pages(pdf):
            self.pages += 1
            for element in page_layout:
                if isinstance(element, LTTextContainer):
                    for text_line in element:
                        self._text_lines.append((self.pages, text_line))

    def _reformat_ypos(self) -> None:
        """
        Since the parser does not neccessarily read the text objects in the
        order they're on the page, we need to sort the list.
        Add an offset to y cooridinate to account for multiple pages
        using the page numbers.
        """
        for i in range(len(self._text_lines)):
            tup = self._text_lines[i]
            obj = tup[1]
            page_no = tup[0]
            y = round(obj.y0, 0)
            ypos = list(str(y))[:-2]
            offset = (
                self.pages - page_no + 1
                if len(ypos) > 2
                else (self.pages - page_no + 1) * 10
            )
            ypos.insert(0, str(offset))
            new_ypos = int("".join(ypos))
            setattr(obj, "y0", new_ypos)
            self._text_lines[i] = obj

        self._text_lines.sort(key=lambda line: line.y0, reverse=True)

    def _get_job_date(self) -> None:
        date = [
            get_formatted_text_from_line_obj(line)
            for line in self._text_lines
            if "Date" in line.get_text()
        ][0]
        self.date = date

    def _split_lines_into_doorstyles(self, lines: list) -> None:
        """
        Seperate lines into their appropriate sections accroding to their
        y cooridnates
        """
        title_section_height = 24.0
        door_style_height = 18.0
        door_type_height = 14.0
        curr_style = ""
        curr_type = ""
        prev_type = ""

        for line in lines:
            height = round(line.height, 0)
            ypos = int(line.y0)
            text = line.get_text().replace("\n", "")

            if height == title_section_height or "Created" in text:
                continue

            elif height == door_style_height:
                name = text.split("(")[0].strip()
                species = text.split("(")[1].strip().replace(")", "")
                prev_style = curr_style
                curr_style = f"{name}-{species}"

                self.door_styles[curr_style] = {
                    "species": species,
                    "section_start": ypos,
                    "section_end": 0,
                    "profiles": [],
                    "types": {},
                    "doors": [],
                    "drawers": [],
                }

                if prev_style in self.door_styles:
                    self.door_styles[prev_style]["section_end"] = ypos + 25

            elif height == door_type_height:
                prev_type = curr_type
                curr_type = text

                self.door_styles[curr_style]["types"][curr_type] = {
                    "section_start": int(ypos),
                    "section_end": 0,
                }

                if prev_type in self.door_styles[curr_style]["types"]:
                    self.door_styles[curr_style]["types"][prev_type][
                        "section_end"
                    ] = ypos

    def _get_doorstyle_ypos(self) -> None:

        doorstyles = [
            (get_formatted_text_from_line_obj(line), line.y0)
            for line in self._text_lines
            if round(line.height, 0) == 18
        ]

        self.door_styles = get_start_and_end_ypos(doorstyles)

    def get_doorstyle_objs_from_tuples(self) -> None:
        self.door_styles = [
            DoorStyle(item["name"], item[1][0], item[1][1]) for item in self.door_styles
        ]
        ic(self.door_styles)