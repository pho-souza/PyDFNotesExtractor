# -*- coding: utf-8 -*-
import PyDFannots.pydfannots as pdf_extract
import PyDFannots.utils as utils
import typing as typ
# from importlib import reload
import json
import re
from itertools import chain
import os
import pathlib
import csv
import sys

import argparse

from . import __doc__, __version__

# reload(pdf_extract)

def file_path(string,dir = False):
    if os.path.isfile(string) and dir == False:
        return string     
    if dir == True and os.path.dirname(string):
        return string       
    else:
        raise FileNotFoundError(string)

def parse_args(args) -> typ.Tuple[argparse.Namespace]:
    import PyDFannots.cfg as cfg
    
    config = cfg.config_file().config
    
    p = argparse.ArgumentParser(prog = 'pypdfannot', description=__doc__)
    
    p.add_argument('--version', '-v', action='version',
                   version='%(prog)s ' + __version__)
    
    p.add_argument("--input","-i", type=pathlib.Path, required=False,
                   help="PDF files to process", nargs='+')
    
    p.add_argument("--output","-o", type=pathlib.Path, required=False,
                   help="Export file", nargs='+')
    
    g = p.add_argument_group('Basic options')
    
    g.add_argument("--adjust-color", "-ac",dest = 'adjust_color', default=True,action="store_true",
                   help = "Extract colors from annotations.")
    
    g.add_argument("--not-adjust-color", "-nac", dest = 'adjust_color',action="store_false",
                   help = "Extract colors from annotations.")
    
    g.add_argument("--adjust-date", "-ad", default=True,action="store_true",
                   help = "Adjust date to the format YYYY-MM-DD HH:mm:SS")
    
    g.add_argument("--no-adjust-date", "-nad",dest = "adjust_date",action="store_false",
                   help = "Adjust date to the format YYYY-MM-DD HH:mm:SS")
    
    g.add_argument("--adjust-text", "-at", dest = "adjust_text",default=True,action="store_true",
                   help = "Adjust text to eliminate hyphens and linebreaks")
    
    g.add_argument("--no-adjust-text", "-nat", dest = "adjust_text",action="store_false",
                   help = "Adjust text to eliminate hyphens and linebreaks")
    
    g.add_argument("--columns", "-c", default=1, type=int,
                   help = "Reorder the annotations using same size columns")
    
    g.add_argument("--tolerance", "-tol", default=config["TOLERANCE"], type=float,
                   help = "Tolerance interval for columns. Default is {}".format(config["TOLERANCE"]))
    
    g.add_argument("--image", "-img", dest = 'image', default=True,action="store_true",
                   help = "Extract rectangle annotations as image")
    
    g.add_argument("--no-image", "-nimg", dest = 'image', action="store_false",
                   help = "Extract rectangle annotations as image")
    
    g.add_argument("--ink-annotation", "-ink", dest = 'ink_annotation',default=True,action="store_true",
                   help = "Extract ink annotations as image")
    
    g.add_argument("--no-ink-annotation", "-nink", dest = 'ink_annotation',action="store_false",
                   help = "Extract ink annotations as image")
    
    g.add_argument("--template", "-temp", default="",
                   help = "Select jinja2 template")
    
    g.add_argument("--reorder-group", "-rg", default=["page"], nargs="+",
                   help = "Select order criteria. Default is page and y position")
    
    g.add_argument("--format","-f",default="",
                   help = "Set the format export. Options are csv or json.")
    
    g.add_argument("--intersection-level","-il",default=config["INTERSECTION_LEVEL"], type=float,
                   help = "Level of intersection between text and highlights. Value between 0 and 1. Default set to 0.1.")
    
    g.add_argument("--import-template","-it", type=pathlib.Path, nargs="+",
                   help = "Add template file to PyDFannots.")
    
    g.add_argument("--delete-template","-dt", type=str, nargs="+",
                   help = "Delete template from template folder. Give just the name.")
    
    g.add_argument("--rename-template","-rt", type=pathlib.Path, nargs=2,
                   metavar=('name','new_name'),
                   help = "Change name.")
    
    g.add_argument("--config","-cfg", default =  "",type=pathlib.Path,
                   help = "Set user config file.")
    
    g.add_argument("--list-templates","-ltemp", default =  False,action="store_true",
                   help = "List all the templates")
    
    g.add_argument("--list-configs","-lconfig", default =  False,action="store_true",
                   help = "List all the templates")
    
    
    args = p.parse_args(args)
    
    return args
    
    

def main(args=None):
    args = parse_args(args)
    # print(args)
    
    extractor = pdf_extract.Note_extractor()
    
    if args.config != pathlib.Path(""):
        path = os.path.abspath(args.config)
        if os.path.exists(path):
            extractor.add_config(path)
    else:
        extractor.add_config()
    # print(args)
    
    if args.list_templates:
        return extractor.templates
    
    if args.list_configs:
        return extractor.config
    
    if args.input != None and args.output != None:
        input_file = args.input[0]
        export_file = args.output[0]
        
        file_path(input_file)
            
        input_file = os.path.abspath(input_file)
        input_file = os.path.abspath(input_file)
        export_file = os.path.abspath(export_file)
        
        
        
        # print(export_folder)
        
        file_title = os.path.basename(input_file)
        file_title = re.sub("[.].*$","",file_title)
        
        if args.template == "":
            extension = re.sub(".*[.](.*)$","\\1",extractor.config["DEFAULT_TEMPLATE"])
        else:
            extension = re.sub(".*[.](.*)$","\\1",args.template)
            
        if args.format == "json":
            extension = "json"
        if args.format == "csv":
            extension = "csv"
        
        
        if os.path.isdir(export_file):
            export_file = export_file + "//" + file_title + "." + extension
            export_file = os.path.abspath(export_file)
            
        export_folder = os.path.dirname(export_file)

        extractor.add_pdf(input_file)

            
        # print(extractor.config)
        
        
        if args.intersection_level != extractor.config["INTERSECTION_LEVEL"]:
            extractor.notes_extract(intersection_level=args.intersection_level)
        else:
            extractor.notes_extract(intersection_level=args.intersection_level)
        
        if args.adjust_color:
            extractor.adjust_color()
        if args.adjust_date:
            extractor.adjust_date()
        if args.adjust_text:
            extractor.adjust_text()

        if args.reorder_group:
            extractor.reorder_custom(criteria=args.reorder_group,ascending=True)
            
        if args.columns > 1 and args.tolerance:
            extractor.reorder_columns(columns=args.columns,tolerance=args.tolerance)
        
        if args.image:
            extractor.extract_image(location=export_folder)
        
        if args.ink_annotation:
            extractor.extract_ink(location=export_folder)

        highlight = extractor.highlights
        
        if args.format == "json":
            highlight = json.dumps(highlight,ensure_ascii=True,indent=4)
            with open(export_file, mode="w",encoding="utf-8") as f:
                f.write(highlight)
                return 0
        elif args.format == "csv":
            names_fields = []
            for annot in highlight:
                names = list(annot.keys())
                names_fields.append(names)
            names_fields = list(chain(*names_fields))
            # print(names_fields)
            names_fields = list(set(names_fields))
            with open(export_file,'w') as csvfile:
                writer = csv.DictWriter(csvfile,fieldnames=names_fields,doublequote=True,lineterminator="\n",quotechar='"')
                writer.writeheader()
                writer.writerows(highlight)
            return 0
        else:
            if args.template == "":
                md_print = utils.md_export(annotations=highlight,title = file_title)
                with open(export_file, "w", encoding="utf-8") as f:
                    f.write(md_print)
                    return 0
            else:
                template_options = extractor.templates
                if args.template in template_options:
                    md_print = utils.md_export(annotations=highlight,title = file_title,template=args.template)
                    with open(export_file, "w", encoding="utf-8") as f:
                        f.write(md_print)
                        return 0
                else:
                    print("Unrecognized template. The options for template are: ",template_options)
    else:
        # print(args)
        if args.import_template:
            arguments = args.import_template
            if isinstance(arguments, pathlib.Path):
                extractor.import_template(arguments)
            elif isinstance(arguments, str):
                extractor.import_template(arguments)
            elif isinstance(arguments, list):
                for imported in arguments:
                    extractor.import_template(imported)
        
        if args.delete_template:
            arguments = args.delete_template
            if isinstance(arguments, str):
                extractor.remove_template(arguments)
            elif isinstance(arguments, list):
                for item in arguments:
                    print(item)
                    extractor.remove_template(item)
                    
        if args.rename_template:
            print(type(args.rename_template))
            if len(args.rename_template) == 2:
                print("AAAAAA")
                original = str(args.rename_template[0])
                new_name = str(args.rename_template[1])
                print(original)
                if any(original for s in extractor.templates):
                    print("BBBBBBB")
                    extractor.rename_template(name = original,new_name = new_name)


if __name__ == '__main__':
    main()