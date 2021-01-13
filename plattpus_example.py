from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch

canvas = Canvas("font-colors.pdf", pagesize=LETTER)


PAGE_HEIGHT = defaultPageSize[1]
print(canvas.getAvailableFonts())
PAGE_WIDTH = defaultPageSize[0]
LEFT_MARGIN = 20
styles = getSampleStyleSheet()

Title = "ORDER FORM"
pageinfo = "platypus example"


def myFirstPage(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColorRGB(0.2, 0.5, 0.5)
    canvas.setFillColorRGB(0, 0, 0.8)
    canvas.rect(
        LEFT_MARGIN, PAGE_HEIGHT - 60, PAGE_WIDTH - (LEFT_MARGIN * 2), 24, fill=1
    )
    canvas.setFillColorRGB(1, 1, 1)
    canvas.setFont("Helvetica-Bold", 16)
    canvas.drawCentredString(PAGE_WIDTH / 2.0, PAGE_HEIGHT - 54, Title)
    canvas.setFont("Helvetica", 9)
    canvas.drawString(inch, 0.75 * inch, "First Page / %s" % pageinfo)
    canvas.restoreState()


def myLaterPages(canvas, doc):
    canvas.saveState()
    canvas.setFont("Times-Roman", 9)
    canvas.drawString(inch, 0.75 * inch, "Page %d %s" % (doc.page, pageinfo))
    canvas.restoreState()


def go():
    doc = SimpleDocTemplate("./reports/phello.pdf")
    Story = [Spacer(1, 2 * inch)]
    style = styles["Heading1"]
    for i in range(100):
        bogustext = ("This is Paragraph number %s. " % i) * 20
        p = Paragraph(bogustext, style)
        Story.append(p)
        Story.append(Spacer(1, 0.2 * inch))
    doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)


go()
