from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar
import pprint


def get_text_lines(pdf) -> list:
    """
    Extract lines of text ffrom generated door report
    """

    lines = []

    for page_layout in extract_pages(pdf):
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                for text_line in element:
                    lines.append(text_line)

    return lines


def get_name_in_brackets(base_str: str) -> str:
    opening = base_str.index("(")
    closing = base_str.index(")")
    return base_str[opening + 1 : closing]


title_section_height = 24.0
door_style_height = 18.0
door_type_height = 14.0
base_height = 10


class JobDetails:
    def __init__(self, name="", date="", styles={}) -> None:
        self.name = name
        self.order_date = date
        self.door_styles = styles

    # def __str__(self)


def load_job_object(text_line_objs: list) -> JobDetails:
    job = JobDetails()
    curr_style = ""
    curr_type = ""

    for line in text_line_objs:
        height = round(line.height, 0)
        text = line.get_text().replace("\n", "")
        if height == title_section_height:
            continue
        elif "Job" in text:
            job.name = get_name_in_brackets(text)
        elif "Date" in text:
            job.order_date = text.split(":")[-1].strip()
        elif height == door_style_height:
            name = text.split("(")[0].strip()
            species = text.split("(")[1].strip().replace(")", "")
            curr_style = f"{name}-{species}"
            job.door_styles[curr_style] = {"profiles": [], "types": {}}
        elif "Profile" in text or "Detail" in text or "Pattern" in text:
            job.door_styles[curr_style]["profiles"].append(text)
        elif height == door_type_height:
            curr_type = text
            job.door_styles[curr_style]["types"][text] = []
        else:
            if curr_type != "" and curr_style != "" and "Created" not in text:
                job.door_styles[curr_style]["types"][curr_type].append((line, line.x0))

    return job


lines = get_text_lines("sample2.pdf")
job = load_job_object(lines)
pp = pprint.PrettyPrinter(indent=2)
pp.pprint(job.door_styles)
pp.pprint(job)
