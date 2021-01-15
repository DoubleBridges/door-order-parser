from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer


class JobDetails:
    def __init__(self, pdf) -> None:
        self.pages = 0
        self.name = ""
        self.order_date = ""
        self.door_styles = {}
        self.doors = []
        self.drawers = []
        self._text_lines = []
        self._ys = []
        self._sizes = {}
        self._qtys = {}
        self._types = {}
        self._doors = []
        self._drawers = []
        self._get_text_lines(pdf)
        self._reformat_ypos()
        self._split_lines_into_sections()
        # self._load_job_object(self._text_lines)
        # self._get_door_sizes_from_line_objs()

    def __repr__(self) -> str:
        return f"Job name: {self.name} Order date: {self.order_date}"

    def _get_name_in_brackets(self, base_str: str) -> str:
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
        Add an offset to y cooridinate to account for multiple pages
        using the page numbers. just the object to the list
        """
        for i in range(len(self._text_lines)):
            tup = self._text_lines[i]
            offset = self.pages - tup[0] + 1
            obj = tup[1]
            ypos = list(str(int(round(obj.y0, 0))))
            ypos.insert(0, str(offset))
            new_ypos = int("".join(ypos))
            setattr(obj, "y0", new_ypos)
            self._text_lines[i] = obj

    def _split_lines_into_sections(self) -> None:
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

        for line in self._text_lines:
            height = round(line.height, 0)
            text = line.get_text().replace("\n", "")
            ypos = int(line.y0)

            if height == title_section_height or "Created" in text:
                self._text_lines.remove(line)

            elif "Job" in text:
                self.name = self._get_name_in_brackets(text)

            elif "Date" in text:
                self.order_date = text.split(":")[-1].strip()

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
                    "lines": [],
                }

                if prev_style in self.door_styles:
                    self.door_styles[prev_style]["section_end"] = ypos + 25

            elif height == door_type_height:
                prev_type = curr_type
                curr_type = text
                print(curr_style)
                print(prev_type)
                print(curr_type)
                print("----------")

                self.door_styles[curr_style]["types"][curr_type] = {
                    "lines": [],
                    "section_start": int(ypos),
                    "section_end": 0,
                }

                if prev_type in self.door_styles[curr_style]["types"]:
                    self.door_styles[curr_style]["types"][prev_type]["section_end"] = (
                        ypos + 15
                    )

        for d_style in self.door_styles:
            start = self.door_styles[d_style]["section_start"]
            end = self.door_styles[d_style]["section_end"]
            self.door_styles[d_style]["lines"] = [
                line for line in self._text_lines if line.y0 in range(end, start)
            ]

    # def _get_sizes_
    # def _get_door_sizes_from_line_objs(self) -> None:
    #     qty_xpos_range = range(70, 90)
    #     type_xpos_range = range(280, 310)

    #     for style in self.door_styles:
    #         for door_type in self.door_styles[style]["types"]:
    #             print(style, door_type)
    #             ys = []
    #             sizes = {}
    #             qtys = {}
    #             # types = {}
    #             doors = []
    #             drawers = []

    #             if door_type == "Drawer Fronts":
    #                 print("drawer")

    #             for line in self.door_styles[style]["types"][door_type]["lines"]:
    #                 text = line.get_text().replace("\n", "").strip()
    #                 # print(text)
    #                 ypos = round(line.y0, 2)
    #                 ys.append(ypos)

    #                 if text.isdigit() and int(line.x0) in qty_xpos_range:
    #                     qtys[ypos] = text
    #                 if "x" in text and text[0].isdigit():
    #                     sizes[ypos] = text
    #                 # if text.isalpha() and int(line.x0) in type_xpos_range:
    #                 #     types[ypos] = text

    #             ys.sort()
    #             ys.reverse()
    #             print(style)
    #             # print(types)
    #             print(qtys)
    #             print(sizes)

    #             # for pos in ys:
    #             #     print(pos)
    #             #     doors.append(
    #             #         {"qty": qtys[pos], "size": sizes[pos], "d_type": types[pos]}
    #             #     ) if types[pos] != "DF" else drawers.append(
    #             #         {"qty": qtys[pos], "size": sizes[pos], "d_type": types[pos]}
    #             #     )

    #             # print(doors, drawers)

    #             # sizes = self.door_styles[style]["types"][door_type]["sizes"]

    #             # for (pos, size) in size_and_ypos:
    #             #     sizes.append({"qty": qty_ypos[pos], "size": size, "pos": pos})

    #             # sizes = sorted(sizes, key=lambda item: item["pos"])
    #             # sizes.reverse()

    #             # self.door_styles[style]["types"][door_type]["sizes"] = sizes

    #             del self.door_styles[style]["types"][door_type]["lines"]