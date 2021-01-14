from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus.paragraph import Paragraph
from reportlab.platypus.paraparser import ParaFrag
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch
from reportlab.platypus.flowables import Flowable
from reportlab.lib.colors import tan, green

from parser import parse_door_report


job = parse_door_report("sample2.pdf")

c = canvas.Canvas("font-colors.pdf", pagesize=LETTER)


def generate_order(job, d_style, d_type, doors=[], drawers=[]):
    PAGE_HEIGHT = defaultPageSize[1]
    PAGE_WIDTH = defaultPageSize[0]
    LEFT_MARGIN = 30
    LINE_HEIGHT = 18
    BACKGROUND_COLOR = (33 / 255, 80 / 255, 156 / 255)
    CURSOR_HEIGHT = PAGE_HEIGHT - 60
    INPUT_HEIGHT = LINE_HEIGHT - (LINE_HEIGHT * 0.1)
    SPECIES = d_style.split("-")[-1]
    STYLE = d_style.split("-")[0]

    styles = getSampleStyleSheet()

    Title = "ORDER FORM"
    pageinfo = "platypus example"

    def myFirstPage(c, doc):
        cursor = CURSOR_HEIGHT
        c.saveState()
        c.setStrokeColorRGB(
            BACKGROUND_COLOR[0], BACKGROUND_COLOR[1], BACKGROUND_COLOR[2]
        )
        c.setFillColorRGB(BACKGROUND_COLOR[0], BACKGROUND_COLOR[1], BACKGROUND_COLOR[2])
        c.rect(
            LEFT_MARGIN, PAGE_HEIGHT - 40, PAGE_WIDTH - (LEFT_MARGIN * 2), 24, fill=1
        )
        c.setFillColorRGB(1, 1, 1)
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(PAGE_WIDTH / 2.0, PAGE_HEIGHT - 34, Title)
        c.setFont("Helvetica", 12)
        c.setFillColorRGB(0, 0, 0)
        c.drawString(LEFT_MARGIN, cursor, f"Customer : JS Designs Shop, LLC")
        c.drawString(
            (PAGE_WIDTH / 2) + (LEFT_MARGIN / 2),
            cursor,
            f"Order Date : {job.order_date}",
        )
        cursor -= LINE_HEIGHT
        c.drawString(LEFT_MARGIN, cursor, f"PO # : {job.name}")
        c.drawString(
            (PAGE_WIDTH / 2) + (LEFT_MARGIN / 2), cursor, "Delivery Date : ASAP"
        )
        cursor -= LINE_HEIGHT
        c.setFont("Helvetica-Bold", 12)
        c.drawString(LEFT_MARGIN, cursor, f"Door Style : {STYLE}")
        c.setFont("Helvetica", 12)
        c.drawString(
            (PAGE_WIDTH / 2) + (LEFT_MARGIN / 2), cursor, "Phone : 901-835-7648"
        )
        cursor -= LINE_HEIGHT
        c.drawString(LEFT_MARGIN, cursor, f"Panel : ")
        c.acroForm.textfield(
            x=LEFT_MARGIN + 40,
            y=cursor - 4,
            name="Panel",
            value=" N/A ",
            height=INPUT_HEIGHT,
            width=(PAGE_WIDTH / 2) - LEFT_MARGIN - (LEFT_MARGIN / 2) - 60,
            borderWidth=0,
            fillColor=([0.5, 0.5, 0.5]),
            relative=True,
        )
        c.drawString((PAGE_WIDTH / 2) + (LEFT_MARGIN / 2), cursor, "Comments : ")
        cursor -= LINE_HEIGHT
        c.drawString(LEFT_MARGIN, cursor, f"Wood Type : {SPECIES}")
        c.line(
            (PAGE_WIDTH / 2) + (LEFT_MARGIN / 2),
            cursor,
            PAGE_WIDTH - LEFT_MARGIN,
            cursor,
        )
        cursor -= LINE_HEIGHT
        c.drawString(LEFT_MARGIN, cursor, f"Inside Profile : ")
        c.acroForm.textfield(
            x=LEFT_MARGIN + 78,
            y=cursor - 4,
            name="inside_profile",
            value=" N/A ",
            height=INPUT_HEIGHT,
            width=(PAGE_WIDTH / 2) - LEFT_MARGIN - (LEFT_MARGIN / 2) - 98,
            borderWidth=0,
            fillColor=([0.5, 0.5, 0.5]),
            relative=True,
        )
        c.line(
            (PAGE_WIDTH / 2) + (LEFT_MARGIN / 2),
            cursor,
            PAGE_WIDTH - LEFT_MARGIN,
            cursor,
        )
        cursor -= LINE_HEIGHT
        c.drawString(LEFT_MARGIN, cursor, f"Outside Profile : ")
        c.acroForm.textfield(
            x=LEFT_MARGIN + 88,
            y=cursor - 4,
            name="outside_profile",
            value=" N/A ",
            height=INPUT_HEIGHT,
            width=(PAGE_WIDTH / 2) - LEFT_MARGIN - (LEFT_MARGIN / 2) - 108,
            borderWidth=0,
            fillColor=([0.5, 0.5, 0.5]),
            relative=True,
        )
        c.line(
            (PAGE_WIDTH / 2) + (LEFT_MARGIN / 2),
            cursor,
            PAGE_WIDTH - LEFT_MARGIN,
            cursor,
        )
        cursor -= LINE_HEIGHT
        c.drawString(LEFT_MARGIN, cursor, f"Stile/Rails : ")
        c.acroForm.textfield(
            x=LEFT_MARGIN + 62,
            y=cursor - 4,
            name="stiles_rails",
            value=" N/A ",
            height=INPUT_HEIGHT,
            width=(PAGE_WIDTH / 2) - LEFT_MARGIN - (LEFT_MARGIN / 2) - 82,
            borderWidth=0,
            fillColor=([0.5, 0.5, 0.5]),
            relative=True,
        )
        c.setFont("Helvetica-Bold", 12)
        c.drawString((PAGE_WIDTH / 2) + (LEFT_MARGIN / 2), cursor, f"Drawer Fronts : ")
        c.setFont("Helvetica", 12)
        cursor -= LINE_HEIGHT
        c.drawString(LEFT_MARGIN, cursor, f"Boring For Hinges : No")
        c.drawString(
            (PAGE_WIDTH / 2) + (LEFT_MARGIN / 2), cursor, f"Outside Profile : "
        )
        cursor -= LINE_HEIGHT
        c.drawString(LEFT_MARGIN, cursor, f"Add Hinges :  No")
        c.drawString(
            (PAGE_WIDTH / 2) + (LEFT_MARGIN / 2),
            cursor,
            f" 5 PC Front             Slab           ",
        )
        cursor -= 12
        c.setFont("Times-Italic", 10)
        c.drawString(
            LEFT_MARGIN,
            cursor,
            f"Boring not available in arched doors, applied mould doors",
        )
        cursor -= 10
        c.drawString(
            LEFT_MARGIN,
            cursor,
            f"and raised bead profile mitered doors",
        )
        cursor -= 14
        c.setFont("Times-BoldItalic", 12)
        c.drawString(
            LEFT_MARGIN, cursor, f'Cullman will not bore any door with 2" stiles'
        )
        cursor -= 20
        c.setFont("Helvetica-Bold", 14)
        c.setFillColorRGB(BACKGROUND_COLOR[0], BACKGROUND_COLOR[1], BACKGROUND_COLOR[2])
        c.drawCentredString(PAGE_WIDTH / 4, cursor, "Doors")
        c.drawCentredString((PAGE_WIDTH / 4) * 3, cursor, "Drawer Fronts")
        cursor -= 20
        c.setFont("Helvetica", 9)
        c.setFillColorRGB(0, 0, 0)
        c.drawCentredString(
            PAGE_WIDTH / 2,
            20,
            'Reminder : Any doors 46" and over in height will automatically receive a horizontal center rail unless otherwise noted.',
        )
        c.restoreState()

    def myLaterPages(c, doc):
        cursor = PAGE_HEIGHT - 60
        c.saveState()
        c.setFont("Helvetica-Bold", 14)
        c.setFillColorRGB(BACKGROUND_COLOR[0], BACKGROUND_COLOR[1], BACKGROUND_COLOR[2])
        c.drawCentredString(PAGE_WIDTH / 4, cursor, "Doors")
        c.drawCentredString((PAGE_WIDTH / 4) * 3, cursor, "Drawer Fronts")
        c.drawCentredString(
            PAGE_WIDTH / 2,
            20,
            'Reminder : Any doors 46" and over in height will automatically receive a horizontal center rail unless otherwise noted.',
        )
        c.restoreState()

    class OrderEntry(Flowable):
        """Draws table entry for each item in list of door sizes."""

        def __init__(self, xoffset=0, height=20, qty="", size="", index="1"):
            Flowable.__init__(self)
            self.qty = qty
            self.size = size
            self.index = index
            self.height = height
            self.idx_box_x = xoffset
            self.idx_box_width = 40
            self.string_center = xoffset + (self.idx_box_width / 2)
            self.qty_box_x = self.idx_box_width + xoffset
            self.qty_box_width = 60
            self.size_box_x = self.qty_box_width - 10
            self.size_box_width = 170
            self.second_column_offset = 270

        def draw(self):

            self.canv.setStrokeColorRGB(0, 0, 0)
            self.canv.setFillColorRGB(
                BACKGROUND_COLOR[0], BACKGROUND_COLOR[1], BACKGROUND_COLOR[2]
            )
            self.canv.rect(self.idx_box_x, 0, self.idx_box_width, self.height, fill=1)
            self.canv.setFillColorRGB(1, 1, 1)
            self.canv.setFont("Helvetica", 12)
            self.canv.drawCentredString(
                self.string_center, 0.25 * self.height, self.index
            )
            self.canv.setFillColorRGB(0, 0, 0)
            self.canv.rect(self.qty_box_x, 0, self.qty_box_width, self.height)
            self.string_center += (self.idx_box_width / 2) + (self.qty_box_width / 2)
            self.canv.drawCentredString(
                self.string_center, 0.25 * self.height, self.qty
            )
            self.canv.rect(self.size_box_x, 0, self.size_box_width, self.height)
            self.string_center += (self.qty_box_width / 2) + (self.size_box_width / 2)
            self.canv.drawCentredString(
                self.string_center, 0.25 * self.height, self.size
            )
            self.canv.rect(
                self.second_column_offset + self.qty_box_x,
                0,
                self.qty_box_width,
                self.height,
            )
            self.string_center += 155
            print(dir(Paragraph))
            self.canv.drawCentredString(
                self.string_center,
                0.25 * self.height,
                self.qty,
            )
            self.string_center += (self.qty_box_width / 2) + (self.size_box_width / 2)
            self.canv.rect(
                self.second_column_offset + self.size_box_x,
                0,
                self.size_box_width,
                self.height,
            )

    def go(name, size_list):
        doc = SimpleDocTemplate(f"./reports/{name}-{d_style}.pdf")
        Story = [Spacer(1, 3 * inch)]
        for size in size_list:
            p = OrderEntry(xoffset=-50, qty=size["qty"], size=size["size"])
            Story.append(p)
        for size in size_list:
            p = OrderEntry(xoffset=-50, qty="2", size="23 x 24 7/8")
            Story.append(p)
        doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)

    sizes = job.door_styles[d_style]["types"][d_type]["sizes"]
    go(job.name, sizes)


generate_order(job, "Slab-Birch", "Panelized Ends")
