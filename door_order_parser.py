from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar

lines = []

for page_layout in extract_pages("sample2.pdf"):
    for element in page_layout:
        if isinstance(element, LTTextContainer):
            for text_line in element:
                lines.append(text_line)

page_dir = {}
current_key = ""

for line in lines:
    height = round(line.height, 2)
    if height > 10:
        if line not in page_dir:
            current_key = line.get_text().replace("\n", "")
            page_dir[current_key] = {}
            page_dir[current_key]["data"] = []
            page_dir[current_key]["name"] = current_key
            page_dir[current_key]["line"] = line
    else:
        page_dir[current_key]["data"].append(line)

for section in page_dir:
    print(section)
    for key in page_dir[section]:
        print("key = ", key, page_dir[section][key])
