# -*- coding: utf-8 -*-
import pypdfannot.pypdfannot as pdf_extract
import pypdfannot.utils as utils
import typing as typ
from importlib import reload
import json
import re
import sys
import os
import pathlib
import csv

import argparse

from . import __doc__, __version__

reload(pdf_extract)

def file_path(string,dir = False):
    if os.path.isfile(string) and dir == False:
        return string     
    if dir == True and os.path.dirname(string):
        return string       
    else:
        raise FileNotFoundError(string)

def parse_args() -> typ.Tuple[argparse.Namespace]:
    p = argparse.ArgumentParser(prog = 'pypdfannot', description=__doc__)
    
    p.add_argument('--version', '-v', action='version',
                   version='%(prog)s ' + __version__)
    
    p.add_argument("input", metavar="INFILE", type=pathlib.Path,
                   help="PDF files to process", nargs='+')
    
    p.add_argument("output", metavar="OUTFILE", type=pathlib.Path,
                   help="Export file", nargs='+')
    
    g = p.add_argument_group('Basic options')
    
    g.add_argument("-p", "--progress", default=False, action="store_true",
                   help="Emit progress information to stderr.")
    
    g.add_argument("--adjust-color", "-ac", default=True,action="store_true",
                   help = "Extract colors from annotations.")
    
    g.add_argument("--adjust-date", "-ad", default=True,action="store_true",
                   help = "Adjust date to the format YYYY-MM-DD HH:mm:SS")
    
    g.add_argument("--adjust-text", "-at", default=True,action="store_true",
                   help = "Adjust text to eliminate hyphens and linebreaks")
    
    g.add_argument("--columns", "-c", default=1,action="store_true",
                   help = "Reorder the annotations using same size columns")
    
    g.add_argument("--tolerance", "-tol", default=0.1,action="store_true",
                   help = "Tolerance interval for columns. Default is 0.1")
    
    g.add_argument("--image", "-img", default=True,action="store_true",
                   help = "Extract rectangle annotations as image")
    
    g.add_argument("--ink-annotation", "-ink", default=True,action="store_true",
                   help = "Extract ink annotations as image")
    
    g.add_argument("--template", "-temp", default="",action="store_true",
                   help = "Select jinja2 template")
    
    g.add_argument("--reorder-group", "-rg", default=["page"], nargs="+",
                   help = "Select order criteria. Default is page and y position")
    
    g.add_argument("--format","-f",default="",action="store_true",
                   help = "Set the format export. Options are csv or json.")
    
    args = p.parse_args()
    
    return args
    
    

def main():
    args = parse_args()
    print(args)
    
    input_file = args.input[0]
    export_file = args.output[0]
    
    file_path(input_file)
        
    input_file = os.path.abspath(input_file)
    input_file = os.path.abspath(input_file)
    export_file = os.path.abspath(export_file)
    
    export_folder = os.path.dirname(export_file)
    print(export_folder)
    
    file_title = os.path.basename(input_file)
    
    extension = re.sub(".*[.](.*)$","\\1",file_title)
    
    print(extension)



    extractor = pdf_extract.Note_extractor(input_file)
    
    extractor.notes_extract()
    
    if args.adjust_color:
        extractor.adjust_color()
    if args.adjust_date:
        extractor.adjust_date()
    if args.adjust_text:
        extractor.adjust_text()

    if args.reorder_group and args.reorder_group != ["page","type"]:
        extractor.reorder_custom(criteria=args.reorder_group,ordenation='asc')
        
    if args.columns > 1 and args.tolerance:
        extractor.reorder_columns(columns=args.columns,tolerance=args.tolerance)
    
    if args.image:
        extractor.extract_image(location=export_folder)
    
    if args.ink_annotation:
        extractor.extract_ink(location=export_folder)

    highlight = extractor.highlights
    
    if args.format == "json":
        highlight = json.dumps(highlight)
        with open(export_file, mode="w",encoding="utf-8") as f:
            f.write(highlight)
            return 0
    elif args.format == "csv":
        names_fields = []
        for annot in highlight:
            names =list(annot.keys())
            names_fields.append(names)
        names_fields = list(set(names_fields))
        with open(export_file,'w') as csvfile:
            writer = csv.DictWriter(csvfile,fieldnames=names_fields)
            writer.writeheader()
            writer.writerows(highlight)
        return 0
    else:
        if args.template == "":
            md_print = utils.md_export(annotations=highlight,title = "")
        else:
            md_print = utils.md_export(annotations=highlight,title = "",template=args.template)
        with open(export_file, "w", encoding="utf-8") as f:
            f.write(md_print)
            
            
    


    # md_print = utils.md_export(annotations=highlight,title = "",template="template_html.html")

    # with open(html_export,'w', encoding='utf-8') as f:
    #     f.write(md_print)


# with open(export_file, "w",encoding='utf-8') as outfile:
#     outfile.write(a)
    
