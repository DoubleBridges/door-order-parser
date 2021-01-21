from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer
from icecream import ic


class JobDetails:
    def __init__(self, pdf) -> None:
        self.pages = 0
        self.name = ""
        self.order_date = ""
        self.door_styles = {}
        self.doors = []
        self.drawers = []
        self._text_lines = []
        self._get_text_lines(pdf)
        self._reformat_ypos()
        self._split_lines_into_sections(self._text_lines)
        self._get_style_sizes_and_totals()

    def __repr__(self) -> str:
        return f"Job name: {self.name} Order date: {self.order_date}"

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
        Since the parser does not neccessarily read the text objects in the order
        they're on the page, we need to sort the list.
        Add an offset to y cooridinate to account for multiple pages
        using the page numbers.
        """
        for i in range(len(self._text_lines)):
            tup = self._text_lines[i]
            obj = tup[1]
            page_no = tup[0]
            y = obj.y0
            ypos = list(str(y))
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

    def _split_lines_into_sections(self, lines: list) -> None:
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

            if "Job" in text:
                self.name = self._get_name_in_brackets(text)

            elif "Date" in text:
                self.order_date = text.split(":")[-1].strip()

            elif height == title_section_height or "Created" in text:
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

    def _get_door_details(self, style: str) -> None:
        """
        Take the list of lines in each door style object and extract the qtys and sizes by correlated y position.
        Store them in a list of tuples on the door type.
        """
        for d_type in self.door_styles[style]["types"]:
            ys = []
            qtys = {}
            sizes = {}
            start = self.door_styles[style]["types"][d_type]["section_start"]
            end = self.door_styles[style]["types"][d_type]["section_end"]
            lines = [
                line
                for line in self.door_styles[style]["lines"]
                if line.y0 in range(end, start)
            ]

            for line in lines:
                qty_xpos_range = range(70, 90)
                text = line.get_text().replace("\n", "")
                ypos = line.y0
                xpos = int(line.x0)

                if "x" in text and "Width" not in text:
                    if ypos not in ys:
                        ys.append(ypos)
                    sizes[ypos] = text
                if text.isdigit() and xpos in qty_xpos_range:
                    if ypos not in ys:
                        ys.append(ypos)
                    qtys[ypos] = text

            self.door_styles[style]["types"][d_type]["sizes"] = [
                (qtys[ypos], sizes[ypos]) for ypos in ys
            ]

    def _get_size_and_quantity(self, style: str) -> None:
        """
        Take the list of size tuples and seperate them into lists of
        doors and drawers by their listed type
        """
        doors = []
        drawers = []

        for d_type in self.door_styles[style]["types"]:
            size_list = self.door_styles[style]["types"][d_type]["sizes"]

            doors += [
                item
                for item in size_list
                if d_type != "Drawer Fronts" and d_type != "False Fronts"
            ]

            drawers += [
                item
                for item in size_list
                if d_type == "Drawer Fronts" or d_type == "False Fronts"
            ]

        self.door_styles[style]["doors"], self.door_styles[style]["drawers"] = (
            doors,
            drawers,
        )

    def _get_style_sizes_and_totals(self) -> None:
        total_doors = 0
        total_drawers = 0

        # Find the ypos range for each section
        for style in self.door_styles:
            start = self.door_styles[style]["section_start"]
            end = self.door_styles[style]["section_end"]
            self.door_styles[style]["lines"] = [
                line for line in self._text_lines if line.y0 in range(end, start)
            ]

            self._get_door_details(style)  # Get the sizes from the text lines
            self._get_size_and_quantity(style)  # Seperate them into doors and drawers
            del self.door_styles[style]["lines"]  # Get rid of the list of objects

            # Calculate the toal doors and drawers fronts for both the door styles
            # and the job.

            style_total_doors = sum(
                [int(qty) for (qty, _) in self.door_styles[style]["doors"]]
            )

            style_total_drawers = sum(
                [int(qty) for (qty, _) in self.door_styles[style]["drawers"]]
            )

            (
                self.door_styles[style]["door_count"],
                self.door_styles[style]["drawer_count"],
            ) = (
                style_total_doors,
                style_total_drawers,
            )

            total_doors += style_total_doors
            total_drawers += style_total_drawers

        self.doors, self.drawers = total_doors, total_drawers
