# from reportlab.lib.pagesizes import LETTER
# from reportlab.lib.units import inch
# from reportlab.pdfgen.canvas import Canvas
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
# from reportlab.lib.styles import getSampleStyleSheet
# from reportlab.rl_config import defaultPageSize
# from reportlab.lib.units import inch

# canvas = Canvas("font-colors.pdf", pagesize=LETTER)

# # # Set font to Times New Roman with 12-point size
# # canvas.setFont("Times-Roman", 12)

# # # Draw blue text one inch from the left and ten
# # # inches from the bottom
# # canvas.setFillColor(blue)
# # canvas.drawString(1 * inch, 10 * inch, "Blue text")

# # # Save the PDF file
# # canvas.save()


# PAGE_HEIGHT = defaultPageSize[1]
# print(PAGE_HEIGHT)
# PAGE_WIDTH = defaultPageSize[0]
# styles = getSampleStyleSheet()

# Title = "Hello world"
# pageinfo = "platypus example"


# def myFirstPage(canvas, doc):
#     canvas.saveState()
#     canvas.setFont("Times-Bold", 16)
#     canvas.drawCentredString(PAGE_WIDTH / 2.0, PAGE_HEIGHT - 108, Title)
#     canvas.setFont("Times-Roman", 9)
#     canvas.drawString(inch, 0.75 * inch, "First Page / %s" % pageinfo)
#     canvas.restoreState()


# def myLaterPages(canvas, doc):
#     canvas.saveState()
#     canvas.setFont("Times-Roman", 9)
#     canvas.drawString(inch, 0.75 * inch, "Page %d %s" % (doc.page, pageinfo))
#     canvas.restoreState()


# def go():
#     doc = SimpleDocTemplate("phello.pdf")
#     Story = [Spacer(1, 2 * inch)]
#     style = styles["Heading1"]
#     for i in range(100):
#         bogustext = ("This is Paragraph number %s. " % i) * 20
#         p = Paragraph(bogustext, style)
#         Story.append(p)
#         Story.append(Spacer(1, 0.2 * inch))
#     doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)


# go()

from reportlab.lib.styles import ParagraphStyle as PS
from reportlab.platypus import PageBreak
from reportlab.platypus.paragraph import Paragraph
from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.platypus.frames import Frame
from reportlab.lib.units import cm


class MyDocTemplate(BaseDocTemplate):
    def __init__(self, filename, **kw):
        self.allowSplitting = 0
        BaseDocTemplate.__init__(self, filename, **kw)
        template = PageTemplate(
            "normal", [Frame(2.5 * cm, 2.5 * cm, 15 * cm, 25 * cm, id="F1")]
        )
        self.addPageTemplates(template)

    def afterFlowable(self, flowable):
        "Registers TOC entries."
        if flowable.__class__.__name__ == "Paragraph":
            text = flowable.getPlainText()
            style = flowable.style.name
            if style == "Heading1":
                self.notify("TOCEntry", (0, text, self.page))
            if style == "Heading2":
                self.notify("TOCEntry", (1, text, self.page))


h1 = PS(name="Heading1", fontSize=14, leading=16)
h2 = PS(name="Heading2", fontSize=12, leading=14, leftIndent=0)
# Build story.
story = []
toc = TableOfContents()
# For conciseness we use the same styles for headings and TOC entries
toc.levelStyles = [h1, h2]
story.append(toc)
story.append(PageBreak())
story.append(Paragraph("First heading", h1))
story.append(Paragraph("Text in first heading", PS("body")))
story.append(Paragraph("First sub heading", h2))
story.append(Paragraph("Text in first sub heading", PS("body")))
story.append(PageBreak())
story.append(Paragraph("Second sub heading", h2))
story.append(Paragraph("Text in second sub heading", PS("body")))
story.append(Paragraph("Last heading", h1))
doc = MyDocTemplate("mintoc.pdf")
doc.multiBuild(story)
