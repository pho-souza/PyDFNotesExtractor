# -*- coding: utf-8 -*-
from pdfannot.pypdfannot import Note_extractor
import pdfannot.utils as utils
import json
import re

# if __name__ == '__main__':
#     import pdfannot.cli
#     pdfannot.cli.main()

def main() -> None:
    file = "D:/Meu Drive/Pesquisas/Outros/Concursos/PPGG-DF/Economia/Micro_Concurso//03 - Elasticidades.pdf"
    export_folder = "C:/Users/pedro/Desktop/cgu/end/"
    export_file = export_folder+"arquivo.json"
    file_title = re.sub(".*/","",file)
    file_title = re.sub("[.].pdf","",file_title)

    html_export = export_folder + "/" + file_title + ".html"



    extractor = Note_extractor(file)


    # pdf = extractor.pdf[3]

    # for annot in pdf.annots():
    #     print(annot.vertices)

    extractor.notes_extract()
    extractor.adjust_color()
    extractor.adjust_date()
    extractor.adjust_text()

    extractor.reorder_custom(criteria=["page"],ordenation='asc')
    extractor.reorder_columns()
    extractor.extract_image(location=export_folder)
    extractor.extract_ink(location=export_folder)

    highlight = extractor.highlights
    a = json.dumps(highlight,indent=4,ensure_ascii=False)


    md_print = utils.md_export(annotations=highlight,title = "",template="template_html.html")

    with open(html_export,'w', encoding='utf-8') as f:
        f.write(md_print)


    with open(export_file, "w",encoding='utf-8') as outfile:
        outfile.write(a)