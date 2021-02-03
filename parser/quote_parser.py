from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer
from icecream import ic


class QuoteDetails:
    def __init__(self, pdf) -> None:
        self.text_lines = []
        self.pages = 0
        self.elev_range = None
        self.room_range = None
        self.desc_range = None
        self.note_range = None
        self.table_range = None
        self.table_data_ypos = []
        self.table_data = {}
        self._get_text_lines(pdf)
        self._get_elev_range()
        self._get_room_range()
        self._get_note_range()
        self._get_desc_range()
        self._get_table_range()
        self._get_data_ypos()
        self._load_data_map()
        self.format_table_data()

    def _get_text_lines(self, pdf) -> None:
        for page_layout in extract_pages(pdf):
            for element in page_layout:
                if isinstance(element, LTTextContainer):
                    for text_line in element:
                        self.text_lines.append(text_line)

    def _get_text_xpos(self, text: str) -> int:
        return [
            (text_cont.x0, text_cont.x1)
            for text_cont in self.text_lines
            if text in text_cont.get_text()
        ][0]

    def _get_text_ypos(self, text: str) -> int:
        return [
            (text_cont.y0, text_cont.y1)
            for text_cont in self.text_lines
            if text in text_cont.get_text()
        ][0]

    def _get_x_range_between_text(
        self, left_text: str, left_x: int, right_text: str, right_x: int
    ) -> range:
        start_x = int(round(self._get_text_xpos(left_text)[left_x], 0))
        end_x = int(round(self._get_text_xpos(right_text)[right_x], 0))
        return range(start_x, end_x)

    def _get_y_range_between_text(
        self, top_text: str, top_y: int, bottom_text: str, bottom_y: int
    ) -> range:
        start_y = int(round(self._get_text_ypos(top_text)[top_y], 0)) - 5
        end_y = int(round(self._get_text_ypos(bottom_text)[bottom_y], 0)) + 5
        return range(end_y, start_y)

    def _get_x_range_for_text(self, text: str) -> range:
        start_x = int(round(self._get_text_xpos(text)[0], 0))
        end_x = int(round(self._get_text_xpos(text)[1], 0))
        return range(start_x, end_x)

    def _get_elev_range(self) -> None:
        self.elev_range = self._get_x_range_for_text("Elevation")

    def _get_room_range(self) -> None:
        self.room_range = self._get_x_range_between_text("Elevation", 1, "Note", 0)

    def _get_note_range(self) -> None:
        self.note_range = self._get_x_range_for_text("Note")

    def _get_desc_range(self) -> None:
        self.desc_range = self._get_x_range_between_text("Note", 1, "Materials", 0)

    def _get_table_range(self) -> None:
        self.table_range = self._get_y_range_between_text(
            "Room", 0, "Upholstered seating", 1
        )

    def _get_data_ypos(self) -> None:
        ypos_list = [
            int(round(text_cont.y0, 0))
            for text_cont in self.text_lines
            if int(text_cont.x0) in self.room_range
            and int(text_cont.y0) in self.table_range
        ]
        ypos_list.sort()
        ypos_list.reverse()
        self.table_data_ypos = ypos_list

    def _load_data_map(self) -> None:
        for pos in self.table_data_ypos:
            self.table_data[pos] = [
                (int(round(text_cont.x0, 0)), text_cont.get_text())
                for text_cont in self.text_lines
                if int(round(text_cont.y0, 0)) in range(pos - 5, pos + 5)
            ]

    def format_table_data(self) -> None:
        for ypos in self.table_data:
            line_item = {
                "elevation": None,
                "room": None,
                "note": None,
                "description": None,
            }
            data_list = self.table_data[ypos]
            elevation = [text for (xpos, text) in data_list if xpos in self.elev_range]
            room = [text for (xpos, text) in data_list if xpos in self.room_range]
            note = [text for (xpos, text) in data_list if xpos in self.note_range]
            description = [
                text for (xpos, text) in data_list if xpos in self.desc_range
            ]

            line_item["elevation"] = None if len(elevation) == 0 else elevation[0]
            line_item["room"] = None if len(room) == 0 else room[0]
            line_item["note"] = None if len(note) == 0 else note[0]
            line_item["description"] = None if len(description) == 0 else description[0]

            self.table_data[ypos] = line_item


quote = QuoteDetails("../sample_input.pdf")
ic(quote.table_data)