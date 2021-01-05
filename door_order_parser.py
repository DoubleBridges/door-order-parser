# from pdfminer.high_level import extract_text

# text = extract_text("sample.pdf")
# print(text)


# from io import StringIO

# from pdfminer.converter import TextConverter
# from pdfminer.layout import LAParams
# from pdfminer.pdfdocument import PDFDocument
# from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
# from pdfminer.pdfpage import PDFPage
# from pdfminer.pdfparser import PDFParser

# output_string = StringIO()
# with open("sample.pdf", "rb") as in_file:
#     parser = PDFParser(in_file)
#     doc = PDFDocument(parser)
#     rsrcmgr = PDFResourceManager()
#     device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
#     interpreter = PDFPageInterpreter(rsrcmgr, device)
#     for page in PDFPage.create_pages(doc):
#         interpreter.process_page(page)

# print(output_string.getvalue())

# from pdfminer.high_level import extract_pages
# from pdfminer.layout import LTTextContainer

# for page_layout in extract_pages("sample.pdf"):
#     for element in page_layout:
#         if isinstance(element, LTTextContainer):
#             print(element.get_text())

# from pdfminer.high_level import extract_pages
# from pdfminer.layout import LTTextContainer, LTChar

# for page_layout in extract_pages("sample.pdf"):
#     for element in page_layout:
#         if isinstance(element, LTTextContainer):
#             for text_line in element:
#                 for character in text_line:
#                     if isinstance(character, LTChar):
#                         print(character.fontname)
#                         print(character.size)

from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar

for page_layout in extract_pages("sample.pdf"):
    for element in page_layout:
        if isinstance(element, LTTextContainer):
            for text_line in element:
                for character in text_line:
                    if not isinstance(character, LTChar):
                        print(type(character))