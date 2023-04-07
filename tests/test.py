# -*- coding: utf-8 -*-
from PyDFannots.pydfannot import Note_extractor
import PyDFannots.utils as utils
import json
import re

# if __name__ == '__main__':
#     import pdfannot.cli
#     pdfannot.cli.main()

# def main() -> None:
file = "tests/PDF_WIKI.pdf"
export_folder = "tests/output/"
export_file = export_folder+"arquivo.json"
file_title = re.sub(".*/","",file)
file_title = re.sub("[.].pdf","",file_title)

html_export = export_folder + "/" + file_title + ".html"



extractor = Note_extractor(file)

pdf = extractor.pdf[0]

for annot in pdf.annots():
    print(annot)
    print(annot.colors)

extractor.get_metadata()
extractor.metadata
extractor.notes_extract()
extractor.adjust_color()
extractor.adjust_date()
extractor.adjust_text()

extractor.reorder_custom(criteria=["page"],ordenation='asc')
extractor.reorder_columns(columns=1,tolerance=0)
extractor.extract_image(location=export_folder)
extractor.extract_ink(location=export_folder)

highlight = extractor.highlights
a = json.dumps(highlight,indent=4,ensure_ascii=False)


md_print = utils.md_export(annotations=highlight,title = "",template="template_html.html")

with open(html_export,'w', encoding='utf-8') as f:
    f.write(md_print)


with open(export_file, "w",encoding='utf-8') as outfile:
    outfile.write(a)