"""
class JobDetails(
    job_name: str,
    date: str,
    door_style: {
        name: str,
        species: str,
        outside_prifle: str,
        inside_profile: str,
        panel_profile: str,
        panel_shape: str,
        total: int,
        applied_and_finished_ends: [
            {
                qty: int,
                width: int,
                height: int,
            },
            ...
        ],
        doors: [
            {
                qty: int,
                width: int,
                height: int,
            },
            ...
        ],
        drawers: [
            {
                qty: int,
                width: int,
                height: int,
            },
            ...
        ],
    }
)
"""
# from reportlab.lib.styles import ParagraphStyle as PS
# from reportlab.platypus import PageBreak
# from reportlab.platypus.paragraph import Paragraph
# from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate
# from reportlab.platypus.tableofcontents import TableOfContents
# from reportlab.platypus.frames import Frame
# from reportlab.lib.units import cm


# class MyDocTemplate(BaseDocTemplate):
#     def __init__(self, filename, **kw):
#         self.allowSplitting = 0
#         BaseDocTemplate.__init__(self, filename, **kw)
#         template = PageTemplate(
#             "normal", [Frame(2.5 * cm, 2.5 * cm, 15 * cm, 25 * cm, id="F1")]
#         )
#         self.addPageTemplates(template)

#     def afterFlowable(self, flowable):
#         "Registers TOC entries."
#         if flowable.__class__.__name__ == "Paragraph":
#             text = flowable.getPlainText()
#             style = flowable.style.name
#             if style == "Heading1":
#                 self.notify("TOCEntry", (0, text, self.page))
#             if style == "Heading2":
#                 self.notify("TOCEntry", (1, text, self.page))


# h1 = PS(name="Heading1", fontSize=14, leading=16)
# h2 = PS(name="Heading2", fontSize=12, leading=14, leftIndent=0)
# # Build story.
# story = []
# toc = TableOfContents()
# # For conciseness we use the same styles for headings and TOC entries
# toc.levelStyles = [h1, h2]
# story.append(toc)
# story.append(PageBreak())
# story.append(Paragraph("First heading", h1))
# story.append(Paragraph("Text in first heading", PS("body")))
# story.append(Paragraph("First sub heading", h2))
# story.append(Paragraph("Text in first sub heading", PS("body")))
# story.append(PageBreak())
# story.append(Paragraph("Second sub heading", h2))
# story.append(Paragraph("Text in second sub heading", PS("body")))
# story.append(Paragraph("Last heading", h1))
# doc = MyDocTemplate("mintoc.pdf")
# doc.multiBuild(story)

# from reportlab.pdfgen.canvas import Canvas
# from reportlab.lib.styles import getSampleStyleSheet
# from reportlab.lib.units import inch
# from reportlab.platypus import Paragraph, Frame

# styles = getSampleStyleSheet()
# styleN = styles["Normal"]
# styleH = styles["Heading1"]
# story = []
# # add some flowables
# story.append(Paragraph("This is a Heading", styleH))
# story.append(Paragraph("This is a paragraph in <i>Normal</i> style.", styleN))
# c = Canvas("mydoc.pdf")
# f = Frame(inch, inch, 6 * inch, 9 * inch, showBoundary=1)
# f.addFromList(story, c)
# c.save()


# from reportlab.lib.units import inch
# from reportlab.pdfgen.canvas import Canvas

# c = Canvas("rect.pdf")
# # move the origin up and to the left
# c.translate(inch, inch)
# # define a large font
# c.setFont("Helvetica", 14)
# # choose some colors
# c.setStrokeColorRGB(0.2, 0.5, 0.3)
# c.setFillColorRGB(1, 0, 1)
# # draw some lines
# c.line(0, 0, 0, 1.7 * inch)
# c.line(0, 0, 1 * inch, 0)
# # draw a rectangle
# c.rect(0.2 * inch, 0.2 * inch, 2 * inch, 3 * inch, fill=1)
# # make text go straight up
# c.rotate(90)
# # change color
# c.setFillColorRGB(0, 0, 0.77)
# # say hello (note after rotate the y coord needs to be negative!)
# c.drawString(0.3 * inch, -inch, "Hello World")
# c.save()
