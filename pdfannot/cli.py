# -*- coding: utf-8 -*-
import pypdfannot as pdf_extract
from importlib import reload
import utils
import json
import re

reload(pdf_extract)

file = "D:/Meu Drive/Pesquisas/Outros/Concursos/PPGG-DF/Economia/Micro_Concurso//02 - oferta e demanda.pdf"
export_folder = "C:/Users/pedro/Desktop/cgu/end/"
export_file = export_folder+"arquivo.json"
file_title = re.sub(".*/","",file)
file_title = re.sub("[.].pdf","",file_title)

html_export = export_folder + "/" + file_title + ".html"



extractor = pdf_extract.Note_extractor(file)


# pdf = extractor.pdf[3]

# for annot in pdf.annots():
#     print(annot.vertices)

extractor.notes_extract()
extractor.adjust_color()
extractor.adjust_date()
extractor.adjust_text()

extractor.reorder_custom(criteria=["page","type"],ordenation='asc')
extractor.extract_image(location=export_folder)
extractor.extract_ink(location=export_folder)

highlight = extractor.highlights
a = json.dumps(highlight,indent=4,ensure_ascii=False)


md_print = utils.md_export(annotations=highlight,title = "",template="template_html.html")

with open(html_export,'w', encoding='utf-8') as f:
    f.write(md_print)


with open(export_file, "w",encoding='utf-8') as outfile:
    outfile.write(a)
    
