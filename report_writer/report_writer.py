from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Spacer
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch
from reportlab.platypus.flowables import Flowable


def generate_order(job, path, d_style, species, doors=[], drawers=[]):
    PAGE_HEIGHT = defaultPageSize[1]
    PAGE_WIDTH = defaultPageSize[0]
    LEFT_MARGIN = 30
    LINE_HEIGHT = 18
    BACKGROUND_COLOR = (33 / 255, 80 / 255, 156 / 255)
    CURSOR_HEIGHT = PAGE_HEIGHT - 60
    INPUT_HEIGHT = LINE_HEIGHT - (LINE_HEIGHT * 0.1)
    SPECIES = species
    STYLE = d_style
    TOTAL_DRS = len(doors)
    TOTAL_DWRS = len(drawers)

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
        c.drawCentredString(PAGE_WIDTH / 2.0, PAGE_HEIGHT - 34, "DOOR ORDER FORM")
        c.setFont("Helvetica", 12)
        c.setFillColorRGB(0, 0, 0)
        c.drawString(LEFT_MARGIN, cursor, f"Customer : JS Designs Shop, LLC")
        c.drawString(
            (PAGE_WIDTH / 2) + (LEFT_MARGIN / 2),
            cursor,
            f"Order Date : {job.order_date}",
        )
        cursor -= LINE_HEIGHT
        c.drawString(LEFT_MARGIN, cursor, f"PO # : {job.name}-{STYLE}-{SPECIES}")
        c.drawString(
            (PAGE_WIDTH / 2) + (LEFT_MARGIN / 2), cursor, "Delivery Date : ASAP"
        )
        cursor -= LINE_HEIGHT
        c.setFont("Helvetica-Bold", 12)
        c.drawString(LEFT_MARGIN, cursor, f"Door Style : {STYLE}")
        c.setFont("Helvetica", 12)
        c.drawString(
            (PAGE_WIDTH / 2) + (LEFT_MARGIN / 2), cursor, "Phone : 901-853-7568"
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
            # fillColor=([1, 1, 1]),
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
            # fillColor=([1, 1, 1]),
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
            # fillColor=([1, 1, 1]),
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
            # fillColor=([1, 1, 1]),
            relative=True,
        )
        c.setFont("Helvetica-Bold", 12)
        c.drawString((PAGE_WIDTH / 2) + (LEFT_MARGIN / 2), cursor, f"Drawer Fronts : ")
        c.acroForm.textfield(
            x=LEFT_MARGIN + 375,
            y=cursor - 4,
            name="drawer_fronts",
            value=" N/A ",
            height=INPUT_HEIGHT,
            width=(PAGE_WIDTH / 2) - LEFT_MARGIN - (LEFT_MARGIN / 2) - 92,
            borderWidth=0,
            # fillColor=([1, 1, 1]),
            relative=True,
        )
        c.setFont("Helvetica", 12)
        cursor -= LINE_HEIGHT
        c.drawString(LEFT_MARGIN, cursor, f"Boring For Hinges : No")
        c.drawString(
            (PAGE_WIDTH / 2) + (LEFT_MARGIN / 2), cursor, f"Outside Profile : "
        )
        c.acroForm.textfield(
            x=LEFT_MARGIN + 370,
            y=cursor - 4,
            name="out_profile",
            value=" N/A ",
            height=INPUT_HEIGHT,
            width=(PAGE_WIDTH / 2) - LEFT_MARGIN - (LEFT_MARGIN / 2) - 87,
            borderWidth=0,
            # fillColor=([1, 1, 1]),
            relative=True,
        )
        cursor -= LINE_HEIGHT
        c.drawString(LEFT_MARGIN, cursor, f"Add Hinges :  No")
        c.drawString(
            (PAGE_WIDTH / 2) + (LEFT_MARGIN / 2),
            cursor,
            f" 5 PC Front:                Slab:",
        )
        c.acroForm.textfield(
            x=LEFT_MARGIN + 350,
            y=cursor - 4,
            name="5_pc_front",
            value=" N/A ",
            height=INPUT_HEIGHT,
            width=30,
            borderWidth=0,
            # fillColor=([1, 1, 1]),
            relative=True,
        )
        c.acroForm.textfield(
            x=LEFT_MARGIN + 430,
            y=cursor - 4,
            name="slab_front",
            value=" N/A ",
            height=INPUT_HEIGHT,
            width=30,
            borderWidth=0,
            # fillColor=([1, 1, 1]),
            relative=True,
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
        c.drawCentredString((PAGE_WIDTH / 4) + 30, cursor, f"Total Doors: {TOTAL_DRS}")
        c.drawCentredString(
            ((PAGE_WIDTH / 4) * 3) + 10, cursor, f"Total Drawer Fronts: {TOTAL_DWRS}"
        )
        cursor -= 24
        c.setStrokeColorRGB(0, 0, 0)
        c.setFillColorRGB(BACKGROUND_COLOR[0], BACKGROUND_COLOR[1], BACKGROUND_COLOR[2])
        c.rect(LEFT_MARGIN + 38, cursor, 60, 20, fill=1)
        c.rect(LEFT_MARGIN + 98, cursor, 170, 20, fill=1)
        c.rect(LEFT_MARGIN + 308, cursor, 60, 20, fill=1)
        c.rect(LEFT_MARGIN + 368, cursor, 170, 20, fill=1)
        c.setFont("Helvetica-Bold", 12)
        c.setFillColorRGB(1, 1, 1)
        string_center = LEFT_MARGIN + 68
        c.drawCentredString(string_center, cursor + 5, "Qty")
        string_center += 115
        c.drawCentredString(string_center, cursor + 5, "Width X Height")
        string_center += 155
        c.drawCentredString(string_center, cursor + 5, "Qty")
        string_center += 115
        c.drawCentredString(string_center, cursor + 5, "Width X Height")
        c.setFont("Helvetica", 9)
        c.setFillColorRGB(0, 0, 0)
        c.drawCentredString(
            PAGE_WIDTH / 2, 40, f"Page 1 of {job.name}-{STYLE}-{SPECIES}"
        )
        c.drawCentredString(
            PAGE_WIDTH / 2,
            20,
            'Reminder : Any doors 46" and over in height will automatically receive a horizontal center rail unless otherwise noted.',
        )
        c.restoreState()

    def myLaterPages(c, doc):
        cursor = PAGE_HEIGHT - 54
        c.saveState()
        c.setFont("Helvetica-Bold", 14)
        c.setFillColorRGB(BACKGROUND_COLOR[0], BACKGROUND_COLOR[1], BACKGROUND_COLOR[2])
        c.drawCentredString((PAGE_WIDTH / 4) + 30, cursor, "Doors")
        c.drawCentredString(((PAGE_WIDTH / 4) * 3) + 10, cursor, "Drawer Fronts")
        cursor -= 24
        c.setStrokeColorRGB(0, 0, 0)
        c.setFillColorRGB(BACKGROUND_COLOR[0], BACKGROUND_COLOR[1], BACKGROUND_COLOR[2])
        c.rect(LEFT_MARGIN + 38, cursor, 60, 20, fill=1)
        c.rect(LEFT_MARGIN + 98, cursor, 170, 20, fill=1)
        c.rect(LEFT_MARGIN + 308, cursor, 60, 20, fill=1)
        c.rect(LEFT_MARGIN + 368, cursor, 170, 20, fill=1)
        c.setFont("Helvetica-Bold", 12)
        c.setFillColorRGB(1, 1, 1)
        string_center = LEFT_MARGIN + 68
        c.drawCentredString(string_center, cursor + 5, "Qty")
        string_center += 115
        c.drawCentredString(string_center, cursor + 5, "Width X Height")
        string_center += 155
        c.drawCentredString(string_center, cursor + 5, "Qty")
        string_center += 115
        c.drawCentredString(string_center, cursor + 5, "Width X Height")
        c.setFont("Helvetica", 9)
        c.setFillColorRGB(0, 0, 0)
        c.drawCentredString(
            PAGE_WIDTH / 2, 40, f"Page {doc.page} of {job.name}-{STYLE}-{SPECIES}"
        )
        c.drawCentredString(
            PAGE_WIDTH / 2,
            20,
            'Reminder : Any doors 46" and over in height will automatically receive a horizontal center rail unless otherwise noted.',
        )
        c.restoreState()

    class OrderEntry(Flowable):
        """Draws table entry for each item in list of door sizes."""

        def __init__(
            self,
            xoffset=0,
            height=20,
            dr_qty="",
            dr_size="",
            dwr_qty="",
            dwr_size="",
            index=0,
        ):
            Flowable.__init__(self)
            self.dr_qty = dr_qty
            self.dr_size = dr_size
            self.dwr_qty = dwr_qty
            self.dwr_size = dwr_size
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
            # Door
            self.canv.setStrokeColorRGB(0, 0, 0)
            self.canv.setFillColorRGB(
                BACKGROUND_COLOR[0], BACKGROUND_COLOR[1], BACKGROUND_COLOR[2]
            )
            self.canv.rect(self.idx_box_x, 0, self.idx_box_width, self.height, fill=1)
            self.canv.setFillColorRGB(1, 1, 1)
            self.canv.setFont("Helvetica", 12)
            self.canv.drawCentredString(
                self.string_center, 0.25 * self.height, str(self.index)
            )
            self.canv.setFillColorRGB(0, 0, 0)
            self.canv.rect(self.qty_box_x, 0, self.qty_box_width, self.height)
            self.string_center += (self.idx_box_width / 2) + (self.qty_box_width / 2)
            self.canv.drawCentredString(
                self.string_center, 0.25 * self.height, self.dr_qty
            )
            self.canv.rect(self.size_box_x, 0, self.size_box_width, self.height)
            self.string_center += (self.qty_box_width / 2) + (self.size_box_width / 2)
            self.canv.drawCentredString(
                self.string_center, 0.25 * self.height, self.dr_size
            )
            # Drawer
            if self.dwr_qty != "" and self.dwr_size != "":
                self.canv.rect(
                    self.second_column_offset + self.qty_box_x,
                    0,
                    self.qty_box_width,
                    self.height,
                )
                self.string_center += 155
                self.canv.drawCentredString(
                    self.string_center,
                    0.25 * self.height,
                    self.dwr_qty,
                )
                self.canv.rect(
                    self.second_column_offset + self.size_box_x,
                    0,
                    self.size_box_width,
                    self.height,
                )
                self.string_center += (self.qty_box_width / 2) + (
                    self.size_box_width / 2
                )
                self.canv.drawCentredString(
                    self.string_center, 0.25 * self.height, self.dr_size
                )

    def build_pdf(path, name, door_list, drawer_list):
        doc = SimpleDocTemplate(f"{path}/{name}-{d_style}.pdf")
        Story = [Spacer(1, 3.11 * inch)]
        num_of_doors = len(door_list)
        num_of_drawers = len(drawer_list)
        num_of_entries = max(num_of_doors, num_of_drawers)

        for i in range(0, num_of_entries):
            try:
                door_qty, door_size = door_list[i]["qty"], door_list[i]["size"]
            except IndexError:
                door_qty, door_size = "", ""

            try:
                drawer_qty, drawer_size = drawer_list[i]["qty"], drawer_list[i]["size"]
            except IndexError:
                drawer_qty, drawer_size = "", ""

            p = OrderEntry(
                xoffset=-50,
                dr_qty=door_qty,
                dr_size=door_size,
                dwr_qty=drawer_qty,
                dwr_size=drawer_size,
                index=i + 1,
            )
            Story.append(p)

        doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)

    build_pdf(path, job.name, doors, drawers)
