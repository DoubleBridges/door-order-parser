from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer

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
        self._text_lines = []
        self._get_text_lines(pdf)
        self._reformat_ypos()
        self._get_job_date()
        self._get_doorstyle_ypos()
        self._instantiate_doorstyle_objs()

    def __repr__(self) -> str:
        return f"Job name: {self.name} Order date: {self.order_date}\n"

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

    def _get_doorstyle_ypos(self) -> None:

        doorstyles = [
            (get_formatted_text_from_line_obj(line), line.y0)
            for line in self._text_lines
            if round(line.height, 0) == 18
        ]

        self.door_styles = get_start_and_end_ypos(doorstyles)

    def _instantiate_doorstyle_objs(self) -> None:
        doorstyle_list = []

        for doorstyle in self.door_styles:
            name = doorstyle["name"]
            species = doorstyle["species"]
            y_range = range(doorstyle["end_y"], doorstyle["start_y"])
            lines = [
                text_line for text_line in self._text_lines if text_line.y0 in y_range
            ]
            doorstyle_list.append(DoorStyle(name, species, y_range, lines))

        self.door_styles = doorstyle_list
