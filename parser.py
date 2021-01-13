from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar
import pprint


def get_text_lines(pdf) -> list:
    """
    Extract lines of text from generated door report
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


def load_job_object(text_line_objs: list) -> JobDetails:
    job = JobDetails()
    curr_style = ""
    curr_type = ""

    for line in text_line_objs:
        height = round(line.height, 0)
        text = line.get_text().replace("\n", "")
        if height == title_section_height or "Created" in text:
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
            job.door_styles[curr_style]["types"][text] = {
                "lines": [],
                "total": 0,
                "sizes": [],
            }
        else:
            if curr_type != "" and curr_style != "":
                job.door_styles[curr_style]["types"][curr_type]["lines"].append(line)

    return job


def get_door_sizes_from_line_objs(job_obj: JobDetails) -> None:
    qty_xpos_range = range(73, 93)

    for style in job_obj.door_styles:
        for door_type in job_obj.door_styles[style]["types"]:
            qty_ypos = {}
            size_and_ypos = []

            for line in job_obj.door_styles[style]["types"][door_type]["lines"]:
                text = line.get_text().replace("\n", "").strip()
                ypos = round(line.y0, 2)

                if text.isdigit() and int(line.x0) in qty_xpos_range:
                    qty_ypos[ypos] = text
                if "x" in text and text[0].isdigit():
                    size_and_ypos.append((ypos, text))

            sizes = job_obj.door_styles[style]["types"][door_type]["sizes"]

            for (pos, size) in size_and_ypos:
                sizes.append({"qty": qty_ypos[pos], "size": size, "pos": pos})

            sizes = sorted(sizes, key=lambda item: item["pos"])
            sizes.reverse()

            job_obj.door_styles[style]["types"][door_type]["sizes"] = sizes

            del job_obj.door_styles[style]["types"][door_type]["lines"]


lines: list = get_text_lines("sample.pdf")
job: JobDetails = load_job_object(lines)
get_door_sizes_from_line_objs(job)

pp = pprint.PrettyPrinter(indent=2)

# pp.pprint(job.name)
# pp.pprint(job.order_date)
# pp.pprint(job.door_styles)

from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch

canvas = Canvas("font-colors.pdf", pagesize=LETTER)


PAGE_HEIGHT = defaultPageSize[1]
PAGE_WIDTH = defaultPageSize[0]
LEFT_MARGIN = 30
LINE_HEIGHT = 18
BACKGROUND_COLOR = (33 / 255, 80 / 255, 156 / 255)
CURSOR_HEIGHT = PAGE_HEIGHT - 60

styles = getSampleStyleSheet()

Title = "ORDER FORM"
pageinfo = "platypus example"


def myFirstPage(canvas, doc):
    cursor = CURSOR_HEIGHT
    canvas.saveState()
    canvas.setStrokeColorRGB(
        BACKGROUND_COLOR[0], BACKGROUND_COLOR[1], BACKGROUND_COLOR[2]
    )
    canvas.setFillColorRGB(
        BACKGROUND_COLOR[0], BACKGROUND_COLOR[1], BACKGROUND_COLOR[2]
    )
    canvas.rect(
        LEFT_MARGIN, PAGE_HEIGHT - 40, PAGE_WIDTH - (LEFT_MARGIN * 2), 24, fill=1
    )
    canvas.setFillColorRGB(1, 1, 1)
    canvas.setFont("Helvetica-Bold", 16)
    canvas.drawCentredString(PAGE_WIDTH / 2.0, PAGE_HEIGHT - 34, Title)
    canvas.setFont("Helvetica", 12)
    canvas.setFillColorRGB(0, 0, 0)
    canvas.drawString(LEFT_MARGIN, cursor, f"Customer : JS Designs Shop, LLC")
    canvas.drawString(
        (PAGE_WIDTH / 2) + (LEFT_MARGIN / 2), cursor, f"Order Date : {job.order_date}"
    )
    cursor -= LINE_HEIGHT
    canvas.drawString(LEFT_MARGIN, cursor, f"PO # : {job.name}")
    canvas.drawString(
        (PAGE_WIDTH / 2) + (LEFT_MARGIN / 2), cursor, "Delivery Date : ASAP"
    )
    cursor -= LINE_HEIGHT
    canvas.setFont("Helvetica-Bold", 12)
    canvas.drawString(LEFT_MARGIN, cursor, f"Door Style : ")
    canvas.setFont("Helvetica", 12)
    canvas.drawString(
        (PAGE_WIDTH / 2) + (LEFT_MARGIN / 2), cursor, "Phone : 901-835-7648"
    )
    cursor -= LINE_HEIGHT
    canvas.drawString(LEFT_MARGIN, cursor, f"Panel : ")
    canvas.drawString((PAGE_WIDTH / 2) + (LEFT_MARGIN / 2), cursor, "Comments : ")
    cursor -= LINE_HEIGHT
    canvas.drawString(LEFT_MARGIN, cursor, f"Wood Type : ")
    canvas.line(
        (PAGE_WIDTH / 2) + (LEFT_MARGIN / 2), cursor, PAGE_WIDTH - LEFT_MARGIN, cursor
    )
    cursor -= LINE_HEIGHT
    canvas.drawString(LEFT_MARGIN, cursor, f"Inside Profile : ")
    canvas.line(
        (PAGE_WIDTH / 2) + (LEFT_MARGIN / 2), cursor, PAGE_WIDTH - LEFT_MARGIN, cursor
    )
    cursor -= LINE_HEIGHT
    canvas.drawString(LEFT_MARGIN, cursor, f"Outside Profile : ")
    canvas.line(
        (PAGE_WIDTH / 2) + (LEFT_MARGIN / 2), cursor, PAGE_WIDTH - LEFT_MARGIN, cursor
    )
    cursor -= LINE_HEIGHT
    canvas.drawString(LEFT_MARGIN, cursor, f"Stile/Rails : ")
    canvas.setFont("Helvetica-Bold", 12)
    canvas.drawString((PAGE_WIDTH / 2) + (LEFT_MARGIN / 2), cursor, f"Drawer Fronts : ")
    canvas.setFont("Helvetica", 12)
    cursor -= LINE_HEIGHT
    canvas.drawString(LEFT_MARGIN, cursor, f"Boring For Hinges : No")
    canvas.drawString(
        (PAGE_WIDTH / 2) + (LEFT_MARGIN / 2), cursor, f"Outside Profile : "
    )
    cursor -= LINE_HEIGHT
    canvas.drawString(LEFT_MARGIN, cursor, f"Add Hinges :  No")
    canvas.drawString(
        (PAGE_WIDTH / 2) + (LEFT_MARGIN / 2),
        cursor,
        f" 5 PC Front             Slab           ",
    )
    cursor -= 12
    canvas.setFont("Times-Italic", 10)
    canvas.drawString(
        LEFT_MARGIN,
        cursor,
        f"Boring not availabel in arched doors, applied mould doors and",
    )
    cursor -= 10
    canvas.drawString(
        LEFT_MARGIN,
        cursor,
        f"raised bead profile mitered doors",
    )
    cursor -= 14
    canvas.setFont("Times-BoldItalic", 12)
    canvas.drawString(
        LEFT_MARGIN, cursor, f'Cullman will not bore any door with 2" styles'
    )
    cursor -= 20
    canvas.setFont("Helvetica-Bold", 14)
    canvas.setFillColorRGB(
        BACKGROUND_COLOR[0], BACKGROUND_COLOR[1], BACKGROUND_COLOR[2]
    )
    canvas.drawCentredString(PAGE_WIDTH / 4, cursor, "Doors")
    canvas.drawCentredString((PAGE_WIDTH / 4) * 3, cursor, "Drawer Fronts")
    cursor -= 20
    canvas.setFont("Helvetica", 9)
    canvas.setFillColorRGB(0, 0, 0)
    canvas.drawCentredString(
        PAGE_WIDTH / 2,
        20,
        'Reminder : Any doors 46" and over in height will automatically receive a horizontal center rail unless otherwise noted.',
    )
    canvas.restoreState()


def myLaterPages(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 9)
    canvas.drawCentredString(
        PAGE_WIDTH / 2,
        20,
        'Reminder : Any doors 46" and over in height will automatically receive a horizontal center rail unless otherwise noted.',
    )
    canvas.restoreState()


def go():
    doc = SimpleDocTemplate(f"./reports/{job.name}.pdf")
    Story = [Spacer(1, 3 * inch)]
    style = styles["Normal"]
    for i in range(100):
        bogustext = ("This is Paragraph number %s. " % i) * 20
        p = Paragraph(bogustext, style)
        Story.append(p)
        # Story.append(Spacer(1, 0.2 * inch))
    doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)


go()