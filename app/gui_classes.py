# import tkinter as tk
# import tkinter.ttk as ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import StringVar, BooleanVar, IntVar, DoubleVar, PhotoImage, END, Listbox, Text
from tkinter.ttk import Frame, Button, Combobox, Label, Checkbutton, Spinbox, Style, Notebook, Scrollbar, Entry, Progressbar, Treeview
from tkinterdnd2 import DND_FILES

from app.cfg import Config_file as Config_class
from app.utils import path_normalizer,  is_dir
from threading import *

import os
import app.cli as cli
import re
import json
from random import choices as random_choices
import string


def threading(): 
    # Call work function 
    t1=Thread(target=cli.main) 
    t1.start() 


class gui_interface():
    def __init__(self,  master = None) -> None:
        self.__master = master
        self.ui = Frame(self.__master)


class gui_pdf_load(gui_interface):
    def __init__(self,  master = None) -> None:
        self.__master = master
        self.ui = Frame(self.__master)

        self.set_size()
        self.assets_import()
        self.set_initial_vars()
        self.basic_ui()
        self.basic_ui_draw()
        self.basic_ui_commmands()

    def set_initial_vars(self):
        self.values_format = ["Template", "csv", "json"]

        self.vars = {}
        self.vars["format"] = StringVar()
        self.vars["format"].set(self.values_format[0])

        self.vars["il"] = DoubleVar()
        self.vars["il"].set(0.1)
        self.vars["col"] = IntVar()
        self.vars["col"].set(1)
        self.vars["tol"] = DoubleVar()
        self.vars["tol"].set(0.1)
        self.vars["template"] = StringVar()
        self.vars["ink"] = BooleanVar()
        self.vars["ink"].set(True)
        self.vars["img"] = BooleanVar()
        self.vars["img"].set(True)

        self.vars["status_text"] = StringVar()
        self.vars["status_text"].set("PyDF Annot opened!")

        self.vars["progress_status"] = DoubleVar()
        self.vars["progress_status"].set(0.0)

        self.vars["parameters"] = StringVar()
        self.vars["parameters"].set("")

    def assets_import(self):
        self.icon_delete = PhotoImage(file = os.path.abspath("app/gui_assets/delete.png"))
        self.icon_trash = PhotoImage(file = os.path.abspath("app/gui_assets/trash.png"))

    def set_status(self, text = ""):
        self.vars["status_text"].set(text)

    def basic_ui(self):
        self.row_1 = Frame(self.ui)
        self.row_2 = Frame(self.ui)
        self.row_3 = Frame(self.ui)
        self.pdf_list = Treeview(self.row_1)



        self.btn_file_selector = Button(self.row_1, text="Select files")
        self.btn_pdf_export = Button(self.row_1,  text = "Export PDF highlights")

        # Grid com atalhos para remover item selecionado ou todos
        self.column_btns = Frame(self.row_1)
        self.btn_remove_item = Button(self.column_btns, image=self.icon_delete)
        self.btn_remove_all_files = Button(self.column_btns, image=self.icon_trash)

        self.parameters_tab = Frame(self.row_2)
        self.parameters_label = Label(self.parameters_tab, text = "Add parameters")
        self.parameters_template_label = Label(self.parameters_tab, text="Select a template")
        self.parameters_template = Combobox(self.parameters_tab, textvariable=self.vars["template"],  state = 'readonly',  )
        self.parameters_il_label = Label(self.parameters_tab, text="Select a intersection level between text and highlights.")
        self.parameters_il = Spinbox(self.parameters_tab, from_=0, to=1,  increment=0.05,  state = 'readonly',  textvariable=self.vars["il"])
        self.parameters_entry = Label(self.parameters_tab, textvariable=self.vars["parameters"])
        self.parameters_col = Spinbox(self.parameters_tab, from_=1, to=15,  increment=1,  state = 'readonly',  textvariable=self.vars["col"])
        self.parameters_col_label = Label(self.parameters_tab, text="Select number of columns in PDF.")
        self.parameters_tol_label = Label(self.parameters_tab, text="Select tolerance interval for columns")
        self.parameters_tol = Spinbox(self.parameters_tab, from_=0, to=1,  increment=0.05,  state = 'readonly',  textvariable=self.vars["tol"])
        self.parameters_img_label = Label(self.parameters_tab, text="Extract images")
        self.parameters_img = Checkbutton(self.parameters_tab,  variable=self.vars["img"])
        self.parameters_ink_label = Label(self.parameters_tab, text="Extract ink annotations")
        self.parameters_ink = Checkbutton(self.parameters_tab,  variable=self.vars["ink"])
        # Default format export set to template
        self.parameters_format_label = Label(self.parameters_tab, text="Select export format.")
        self.parameters_format = Combobox(self.parameters_tab, textvariable=self.vars["format"],  state = 'readonly',  )

        # self.parameters_cfg_label = Label(self.parameters_tab, text="Load saved config.")
        # self.parameters_cfg_load = Button(self.parameters_tab, text="Load", command=self.load_cfg)
        # self.parameters_cfg_save = Button(self.parameters_tab, text="Save", command=self.save_cfg)

        # Status bar
        self.status_bar = Label(self.row_3, textvariable=self.vars["status_text"])
        self.progress_bar = Progressbar(self.row_3, orient='horizontal', length=250, mode = 'determinate')

    def basic_ui_draw(self):
        self.ui.grid(sticky='nwse')
        self.row_1.grid(column = 1,  row = 1, sticky='nwse')
        self.row_2.grid(column = 1,  row = 2, sticky='nwse')
        self.row_3.grid(column = 1,  row = 3, sticky='nwse')
        self.pdf_list.grid(column = 1,  row = 1,  columnspan = 2, sticky = "nwse")

        self.btn_file_selector.grid(column=1, row = 2, sticky = "nwse")
        self.btn_pdf_export.grid(column=2, row = 2, sticky = "nwse")
        self.ui.grid_columnconfigure(1, weight=7)

        self.ui.grid_rowconfigure(1, weight=7)
        self.ui.grid_rowconfigure(2, weight=3)

        self.column_btns.grid(column=4, row=1, rowspan=2)
        self.btn_remove_item.grid()
        self.btn_remove_all_files.grid()

        self.row_1.grid_columnconfigure(1, weight=5)
        self.row_1.grid_columnconfigure(2, weight=5)

        self.row_1.grid_rowconfigure(1, weight=7)

        self.row_2.grid_columnconfigure(1, weight=6)
        self.row_2.grid_columnconfigure(2, weight=3)
        self.row_2.grid_columnconfigure(3, weight=3)

        self.parameters_tab.grid(column = 0,  row = 0, sticky = "nwse")
        self.parameters_label.grid(row = 0,  sticky = "nwse")
        self.parameters_entry.grid(row = 0,  column = 1, sticky = "nwse",  columnspan=2)
        self.parameters_template_label.grid(row = 1,  sticky = "nwse")
        self.parameters_template.grid(row = 1,  column = 1, sticky = "nwse")
        self.parameters_il_label.grid(row = 2,  sticky = "nwse")
        self.parameters_il.grid(row = 2,  column = 1, sticky = "nwse")
        self.parameters_col_label.grid(row = 3,  sticky = "nwse")
        self.parameters_col.grid(row = 3,  column = 1, sticky = "nwse")
        self.parameters_tol_label.grid(row = 4,  sticky = "nwse")
        self.parameters_tol.grid(row = 4,  column = 1, sticky = "nwse")
        self.parameters_img_label.grid(row = 5,  sticky = "nwse")
        self.parameters_img.grid(row = 5,  column = 1, sticky = "nwse")
        self.parameters_ink_label.grid(row = 4,  sticky = "nwse")
        self.parameters_ink.grid(row = 6,  column = 1, sticky = "nwse")
        self.parameters_format_label.grid(row = 7,  sticky = "nwse")
        self.parameters_format.grid(row = 7,  column = 1, sticky = "nwse")
        # self.parameters_cfg_label.grid(row = 8,  sticky = "nwse")
        # self.parameters_cfg_load.grid(row = 9,  sticky = "nwse")
        # self.parameters_cfg_save.grid(sticky = "nwse")

        self.status_bar.grid(sticky="nwse")
        self.progress_bar.grid(sticky='nwse')
        self.set_cfg()

    @property
    def arguments(self):
        parameters = f'-il {self.cfg["INTERSECTION_LEVEL"]} --columns {self.cfg["COLUMNS"]} -tol  {self.cfg["TOLERANCE"]} --template "{self.cfg["TEMPLATE"]}"'
        if not self.cfg["FORMAT"] == "Template":
            parameters = f'{parameters}  --format {self.cfg["FORMAT"]}'
        # # print(parameters)
        self.vars["parameters"].set(parameters)
        return parameters

    def edit_parameters(self):
        parameters = f'-il {self.cfg["INTERSECTION_LEVEL"]} --columns {self.cfg["COLUMNS"]} -tol  {self.cfg["TOLERANCE"]} --template "{self.cfg["TEMPLATE"]}"'
        self.parameters_arguments = list()
        if not self.cfg["FORMAT"] == "Template":
            parameters = f'{parameters}  --format {self.cfg["FORMAT"]}'
            self.parameters_arguments.append(['--format', self.cfg["FORMAT"]])
        self.parameters_arguments.append(['-il', self.cfg["INTERSECTION_LEVEL"]])
        self.parameters_arguments.append(['--columns', self.cfg["COLUMNS"]])
        self.parameters_arguments.append(['-tol', self.cfg["TOLERANCE"]])

        self.vars["parameters"].set(parameters)

    def get_cfg(self,  event = None):
        if os.path.exists("default_cfg.json"):
            file = open("default_cfg.json").read()
            self.configuration_file = json.load(file)
            # self.configuration_file
    
    def get_pdf_info(self, pdf_path = '', event=None):
        status = "Getting data from: " + pdf_path
        self.set_status(status)

        pdf = path_normalizer(pdf_path)

        pdf_path = os.path.abspath(pdf)

        pdf_path = path_normalizer(pdf_path)

        input_file = ['-i', pdf_path]

        argument_count_annots = input_file + ['--count-annotations']
        argument_count_pages = input_file + ['--total-pages']

        number_of_annots = cli.main(argument_count_annots)
        number_of_pages = cli.main(argument_count_pages)
        
        return (pdf_path, number_of_pages, number_of_annots)

    def set_cfg(self, event=None):
        if not hasattr(self, "cfg"):
            self.cfg = {}
        self.cfg["INTERSECTION_LEVEL"] = self.vars["il"].get()
        self.cfg["COLUMNS"] = self.vars["col"].get()
        self.cfg["TOLERANCE"] = self.vars["tol"].get()
        self.cfg["TEMPLATE"] = self.vars["template"].get()
        self.cfg["FORMAT"] = self.vars["format"].get()
        self.cfg["IMAGE"] = self.vars["img"].get()
        self.cfg["INK"] = self.vars["ink"].get()
        # print(self.cfg)
        self.edit_parameters()

    def set_vars(self):
        self.vars["il"].set(self.cfg["INTERSECTION_LEVEL"])
        self.vars["col"].set(self.cfg["COLUMNS"])
        self.vars["tol"].set(self.cfg["TOLERANCE"])
        self.vars["template"].set(self.cfg["TEMPLATE"])
        self.vars["format"].set(self.cfg["FORMAT"])
        self.vars["img"].set(self.cfg["IMAGE"])
        self.vars["ink"].set(self.cfg["INK"])
        self.set_cfg()

    def set_new_cfg(self, cfg:dict):
        if cfg.keys() == self.cfg.keys():
            for entry in cfg:
                self.cfg[entry] = cfg[entry]
            self.set_vars()
            self.set_cfg()
            self.cfg_validate()

    def cfg_validate(self,  event = None):
        self.load_templates()
        if not isinstance(self.cfg["INTERSECTION_LEVEL"], float):
            self.vars["col"].set(self.default_configs["INTERSECTION_LEVEL"])
        if not isinstance(self.cfg["COLUMNS"], int):
            self.vars["col"].set(self.default_configs["TOLERANCE"])
        if not isinstance(self.cfg["TOLERANCE"], float):
            self.vars["tol"].set(self.default_configs["TOLERANCE"])
        if not self.cfg["TEMPLATE"] in self.templates:
            self.vars["template"].set(self.default_configs["DEFAULT_TEMPLATE"])
        if not self.cfg["IMAGE"] in self.templates:
            self.vars["img"].set(self.default_configs["IMAGE"])
        if not self.cfg["INK"] in self.templates:
            self.vars["ink"].set(self.default_configs["INK"])
        self.set_cfg()

    @property
    def templates(self):
        return cli.main(['--list-templates'])

    @property
    def default_configs(self):
        return cli.main(["--list-configs"])

    def load_templates(self,  event = None):
        self.parameters_template["values"] = self.templates

    def load_cfg(self, event = None):
        file_cfg = filedialog.askopenfile(title="Select config file", mode='r', filetypes=(('json file', '*.json'), ))
        cfg = json.load(file_cfg)
        self.set_new_cfg(cfg)
        # print(list(cfg.keys()))
        self.set_status(f'Configs loaded from: {file_cfg.name}')

    def save_cfg(self, event = None):
        self.set_cfg()
        file_cfg = filedialog.asksaveasfilename(title="Save config file", filetypes=(('json file', '*.json'), ), defaultextension="json")
        cfg = json.dumps(self.cfg, ensure_ascii=True, indent=4)
        with open(file_cfg, mode='w', encoding="utf-8") as f:
            f.write(cfg)
        self.set_status(f'Configs saved at: {file_cfg}')

    def basic_ui_commmands(self):
        self.cfg_validate()
        self.btn_file_selector['command'] = self.add_file
        self.btn_remove_all_files["command"] = self.remove_all_files
        self.btn_remove_item["command"] = self.remove_file
        self.btn_pdf_export["command"] = self.export_folder

        self.pdf_list.bind("<Delete>",  self.remove_file)

        # self.vars["il"].set(self.default_configs["INTERSECTION_LEVEL"])
        # self.vars["col"].set(self.default_configs["COLUMNS"])
        # self.vars["tol"].set(self.default_configs["TOLERANCE"])

        self.parameters_il.bind("<ButtonRelease>",  self.cfg_validate)
        self.parameters_tol.bind("<ButtonRelease>",  self.cfg_validate)
        self.parameters_col.bind("<ButtonRelease>",  self.cfg_validate)
        self.parameters_template.bind("<ButtonRelease>",  self.cfg_validate)
        self.parameters_format.bind("<ButtonRelease>",  self.cfg_validate)

        self.parameters_il.bind("<Leave>",  self.cfg_validate)
        self.parameters_tol.bind("<Leave>",  self.cfg_validate)
        self.parameters_col.bind("<Leave>",  self.cfg_validate)
        self.parameters_template.bind("<Leave>",  self.cfg_validate)
        self.parameters_format.bind("<Leave>",  self.cfg_validate)

        self.parameters_il.bind("<Enter>",  self.cfg_validate)
        self.parameters_tol.bind("<Enter>",  self.cfg_validate)
        self.parameters_col.bind("<Enter>",  self.cfg_validate)
        self.parameters_template.bind("<Enter>",  self.cfg_validate)
        self.parameters_format.bind("<Enter>",  self.cfg_validate)

        self.configs = cli.main(['--list-configs'])

        self.parameters_template["values"] = self.templates
        self.parameters_format["values"] = self.values_format
        

        # self.vars["template"].set("template_html.html")

        self.pdf_list.drop_target_register(DND_FILES)
        self.pdf_list.dnd_bind("<<Drop>>",  self.add_file_drag_drop)
        
        self.pdf_list['columns'] = ['Files', 'Number of pages', 'Number of annotations']
        
        self.pdf_list['show'] = 'headings'

        for col in self.pdf_list['columns']:
            if col == 'Files':
                self.pdf_list.column(col, minwidth=int(300))
            self.pdf_list.heading(col, text=col)
            
        
        self.set_cfg()

    def add_file_drag_drop(self, event):
        list_files = event.data
        if bool(re.search("^\\{", list_files)):
            list_files = re.sub('[ ]+\{', "", list_files)
            list_files = re.sub('\{', "", list_files)
            list_files = re.sub('\\\\', "/", list_files)
            list_files = re.sub('\}', ";", list_files)
            list_files = re.sub('^[ ]+', "", list_files)
            lista = list_files.split(";")
        else:
            lista = list_files.split()
        # print(lista)
        
        values = []
        for i in lista:
            if not i == '':
                pdf_inserted = re.sub("^[ ]+", "", i)
                value_pdf = (pdf_inserted, '', '')
                values.append(value_pdf)
        for i in values:
            self.pdf_list.insert('', 'end', values = i)
        self.validate_files()

    def validate_files(self):
        self.files = list()
        for line in self.pdf_list.get_children():
            print(line)
            pdf_file = self.pdf_list.item(line)['values'][0]
            print(pdf_file)
            self.files.append(pdf_file)
        # self.files = list(self.pdf_list.get_children(0, END))
        for file in self.files:
            self.files.remove(file)
            file = path_normalizer(file)
            self.files.append(file)

        for file in self.files:
            file = path_normalizer(file)
            extension = re.sub(".*[.](.*)", "\\1", str.upper(file))
            print(extension)
            if extension != "PDF" or is_dir(file):
                print(file)
                self.files.remove(file)
        self.files = set(self.files)
        self.files = list(self.files)

        self.remove_all_files()

        for i in self.files:
            # value_pdf = self.get_pdf_info(i)
            values = self.get_pdf_info(i)
            self.pdf_list.insert('', 'end',  values=values)
        self.set_status(f'There are {len(self.files)} PDFs files. ')



    def export_folder(self):
        self.files = list()
        # self.files = list(self.pdf_list.get(0, END))
        for i in self.pdf_list.get_children():
            pdf = self.pdf_list.item(i)['values'][0]
            self.files.append(pdf)
        # print(self.files)

        if len(self.files) >= 1:
            self.folder = filedialog.askdirectory(title="Select export folder")
            # self.folder = str(os.path.abspath(self.folder))

            self.cfg_validate()
            self.pdf_export(pdf_location=self.files, export = self.folder)
        else:
            messagebox.showerror(title = "Select at least one PDF file.",
            message = "You have to select at least one PDF file on the <Select files> button.")

    def add_file(self):
        file_open = filedialog.askopenfiles(defaultextension=['pdf'], filetypes=[('PDF', '.pdf')])
        if isinstance(file_open, list):
            for i in file_open:
                file = i.name
                path = os.path.abspath(file)
                if not is_dir(file):
                    values = (file, '', '')
                    self.pdf_list.insert('', 'end', values=values)
        else:
            file = os.path.abspath(file_open)
            if not is_dir(file):
                values = self.get_pdf_info(file)
                self.pdf_list.insert('', 'end', values=values)
        self.validate_files()

    def remove_all_files(self):
        for line in self.pdf_list.get_children():
            self.pdf_list.delete(line)

    def remove_file(self, event= None):
        selected_items = self.pdf_list.curselection()
        for item in selected_items:
            # print(item)
            self.pdf_list.delete(item)

    def set_size(self, width = 500,  height = 500):
        self.width = width
        self.height = height

    def pdf_export(self, pdf_location = [],  export = 'output/', config_file = "default_cfg.json"):
        if os.path.exists(export) is False:
            export = path_normalizer(export)
            self.set_status(f'Export folder "{export}" does not exist!')
            self.set_status(f'Creating new folder')
            os.mkdir(export)

        self.edit_parameters()

        for pdf in pdf_location:
            status = "Extracting annotation for: " + pdf
            self.set_status(status)


            pdf = path_normalizer(pdf)

            pdf_path = os.path.abspath(pdf)

            pdf_path = path_normalizer(pdf_path)

            input_file = ['-i', pdf_path, '-o', export]

            argument_count_annots = input_file + ['--count-annotations']

            print(argument_count_annots)
            
            print(self.vars['format'])
            if self.vars['format'].get() == 'Template':
                argument = input_file + ['-il', f'{self.cfg["INTERSECTION_LEVEL"]}',  '-tol', f'{self.cfg["TOLERANCE"]}', '--columns', f'{self.cfg["COLUMNS"]}', '--template', f'{self.cfg["TEMPLATE"]}']
            elif self.vars['format'].get() == 'json':
                argument = input_file + ['-il', f'{self.cfg["INTERSECTION_LEVEL"]}',  '-tol', f'{self.cfg["TOLERANCE"]}', '--columns', f'{self.cfg["COLUMNS"]}', '--format', 'json']
            elif self.vars['format'].get() == 'csv':
                argument = input_file + ['-il', f'{self.cfg["INTERSECTION_LEVEL"]}',  '-tol', f'{self.cfg["TOLERANCE"]}', '--columns', f'{self.cfg["COLUMNS"]}', '--format', 'csv']
            
            if os.path.exists(config_file):
                argument = argument + ['--config', config_file]

            count_annotation = cli.main(argument_count_annots)

            if count_annotation > 0:
                t1 = Thread(target = cli.main, args = (argument, ))
                t1.start()
                status = f'Annotations for {pdf} extracted!'
                self.set_status(status)
            else:
                messagebox.showerror(title="Error!", message=f"{pdf_path} file don't have annotations.")
        status = f'All annotations extracted!'
        self.set_status(status)


class gui_settings(gui_interface):
    def __init__(self,  master = None) -> None:
        self.__master = master
        self.ui = Frame(self.__master)

        self.configuration_file = {}

        self.basic_ui()
        self.basic_ui_draw()
        self.basic_ui_commmands()
        self.selected_items = []



    def basic_ui(self):
        self.style = Style(self.ui)
        self.style.configure('lefttab.TNotebook',  tabposition='wn')

        self.notebook = Notebook(self.ui,  style='lefttab.TNotebook')

        

        # Config of template tab
        self.template_tab = Frame(self.ui)
        self.col_1 = Frame(self.template_tab)
        self.col_2 = Frame(self.template_tab)
        self.file_list = Listbox(self.col_1)
        self.btn_add_template = Button(self.col_1, text="+")
        self.btn_del_template = Button(self.col_1,  text = "-")
        self.btn_load_template = Button(self.col_1,  text = "Load external template")
        self.vertical_bar = Scrollbar(self.col_2,  orient = 'vertical')
        self.temp_text = Text(self.col_2,  yscrollcommand=self.vertical_bar.set)
        # Grid com atalhos para remover item selecionado ou todos
        self.column_btns = Frame(self.col_1)
        # self.btn_remove_item = Button(self.column_btns, image=self.icon_delete)
        # self.btn_remove_all_files = Button(self.column_btns, image=self.icon_trash)

        self.parameters_tab = Frame(self.col_2)
        self.parameters_label = Label(self.parameters_tab, text = "Adicione parametros")
        self.rename_entry = Entry(self.parameters_tab)
        self.btn_rename_template = Button(self.parameters_tab,  text = "Save")

        #### Configs template
        self.configs_tab = Frame(self.ui)
        self.config_frame = Frame(self.configs_tab)
        self.config_label = Label(self.config_frame, text="Configuration of app")
        self.config_default = Button(self.config_frame,  text = "Default Config")
        self.config_save = Button(self.config_frame, text = "Save Config")
        self.config_items = dict()
        self.config_labels = dict()

    def basic_ui_draw(self):
        self.ui.grid_columnconfigure(0, weight=10)
        self.notebook.grid(sticky="nwse", row=0, column=0)

        self.col_1.grid(column = 1,  row = 1, sticky='nwse',  rowspan=3)
        self.col_2.grid(column = 2,  row = 1, sticky='nwse')
        self.file_list.grid(column = 1,  row = 1,  columnspan = 3, sticky = "nwse")
        self.temp_text.grid(sticky="nwse")
        self.btn_add_template.grid(column=1, row = 2, sticky = "nwse")
        self.btn_del_template.grid(column=2, row = 2, sticky = "nwse")
        self.btn_load_template.grid(column=3,  row = 2,  sticky = "nwse")
        self.temp_text.grid(column = 0, row = 3, sticky="nwse")
        self.vertical_bar.grid(column = 1, row = 3,  sticky='nwse')

        self.template_tab.grid_columnconfigure(1, weight=7)
        self.template_tab.grid_columnconfigure(2, weight=3)

        self.column_btns.grid(column=4, row=1, rowspan=2)

        self.col_1.grid_columnconfigure(1, weight=3)
        self.col_1.grid_columnconfigure(2, weight=3)
        self.col_1.grid_columnconfigure(3, weight=3)


        self.col_2.grid_columnconfigure(0, weight=1)


        self.parameters_tab.grid(column = 0,  row = 0, sticky = "nwse")
        self.parameters_label.grid(sticky = "nwse")
        self.rename_entry.grid(sticky = "nwse",  columnspan=2)
        self.btn_rename_template.grid(row = 1,  column=4, sticky = "nwse")

        ### Config tab
        self.configs_tab.grid(sticky="nwse")
        self.configs_tab.grid_columnconfigure(0,  weight=1)

        


    def basic_ui_commmands(self):
        self.notebook.add(self.template_tab, text = "Templates")
        self.notebook.add(self.configs_tab, text = "Configuration")
        self.btn_add_template['command'] = self.add_template
        self.btn_del_template["command"] = self.del_template
        self.btn_rename_template["command"] = self.rename_template
        self.file_list.bind("<ButtonRelease>", self.load_template)

        self.vertical_bar.config(command = self.temp_text.yview)
        self.update_templates()

        self.configs = cli.main(['--list-configs'])

        for conf in self.configs:
            config = self.configs[conf]
            self.config_items[conf] = dict()
            self.config_items[conf]["frame"] = Frame(self.configs_tab)
            self.config_items[conf]["label"] = Label(self.config_items[conf]["frame"], text=conf,  width=30)

            if isinstance(config,  str) and conf != "DEFAULT_TEMPLATE":
                self.config_items[conf]["vars"] = StringVar()
                self.config_items[conf]["entry"] = Entry(self.config_items[conf]["frame"],  width = 60,  textvariable=self.config_items[conf]["vars"])
            elif isinstance(config,  str) and conf == "DEFAULT_TEMPLATE":
                self.config_items[conf]["vars"] = StringVar()
                self.config_items[conf]["entry"] = Combobox(self.config_items[conf]["frame"],  width = 60,  textvariable=self.config_items[conf]["vars"])
                self.config_items[conf]["entry"]["values"] = self.templates
            elif isinstance(config, list):
                self.config_items[conf]["entry"] = Listbox(self.config_items[conf]["frame"], width = 60)
                self.config_items[conf]["entry"].bind("<Double-1>", self.change_listbox)
                self.config_items[conf]["entry"].bind("<Return>", self.change_listbox)
            elif isinstance(config, bool):
                self.config_items[conf]["vars"] = BooleanVar()
                self.config_items[conf]["entry"] = Checkbutton(self.config_items[conf]["frame"],  variable=self.config_items[conf]["vars"])
            elif isinstance(config, float):
                self.config_items[conf]["vars"] = DoubleVar()
                self.config_items[conf]["entry"] = Spinbox(self.config_items[conf]["frame"],  from_ = 0,  to = 1, increment=0.05,  textvariable=self.config_items[conf]["vars"])
            elif isinstance(config, int):
                self.config_items[conf]["vars"] = IntVar()
                self.config_items[conf]["entry"] = Spinbox(self.config_items[conf]["frame"],  from_ = 1,  to = 10,  textvariable=self.config_items[conf]["vars"])
            else:
                self.config_items[conf]["entry"] = Entry(self.config_items[conf]["frame"],  width = 60)
            self.config_items[conf]["frame"].grid(sticky="nwse")
            self.config_items[conf]["label"].grid(column = 1, row = 1, sticky="WE")
            self.config_items[conf]["entry"].grid(column = 2, row = 1, sticky="WE")
        self.load_config()
        self.set_config()
        self.config_frame.grid(sticky="nwse")
        self.config_label.grid(row = 0, sticky="nwse")
        self.config_default.grid(row = 1,  column=1, sticky="nwse")
        self.config_save.grid(row = 1,  column=2, sticky="nwse")

        self.config_default['command'] = self.restore_config
        self.config_save['command'] = self.save_config

            
    def set_config(self):
        """
        Set the self.config value to all entries in configuration tab
        """
        for conf in self.configs:
            config = self.configs[conf]
            tk_item = self.config_items[conf]["entry"]
            if isinstance(tk_item,  (Entry)):
                self.config_items[conf]["vars"].set(config)
            elif isinstance(tk_item,  Listbox):
                self.config_items[conf]["entry"].delete('0', 'end')
                for i in config:
                    self.config_items[conf]["entry"].insert('end', i)
            elif isinstance(tk_item,  Checkbutton):
                self.config_items[conf]["vars"].set(config)
            else:
                self.config_items[conf]["vars"].set(config)
        self.get_config()

    def change_listbox(self, event = None):
        pass

    def get_config(self):
        """
        Get the self.config values from all entrys in configuration tab
        """
        for conf in self.configs:
            tk_item = self.config_items[conf]["entry"]
            if isinstance(tk_item,  (Entry)):
                self.configs[conf] = self.config_items[conf]["vars"].get()
            elif isinstance(tk_item,  Checkbutton):
                self.configs[conf] = self.config_items[conf]["vars"].get()
            else:
                self.configs[conf] = self.config_items[conf]["entry"].get(0, 'end')
        self.configuration_file["config"] = self.configs

    def load_config(self, from_file = True):
        """
        Load configuration if exist default configuration. If don't,  load from cfg settings
        """
        if os.path.exists("default_cfg.json") and from_file:
            file = open("default_cfg.json", mode='r', encoding='utf-8')
            self.configuration_file = json.load(file)
            self.configs = self.configuration_file["config"]
        else:
            self.configs = cli.main(['--list-configs'])
            self.configuration_file["config"] = self.configs
        # self.set_config()

    def save_config(self):
        self.get_config()
        file = json.dumps(self.configuration_file, ensure_ascii=True, indent=4)
        with open("default_cfg.json",  mode='w',  encoding='utf-8') as f:
            f.write(file)
        print("SAVED")

    def restore_config(self):
        """
        Restore default settings from configuration class
        """
        cfg = Config_class("")
        self.configs = cfg.default
        print(self.configs)
        # self.get_config()
        self.set_config()
        print("LOADED")


        # print(self.configs)
    @property
    def templates(self):
        return cli.main(["--list-templates"])

            
    def update_templates(self):
        self.file_list.delete(0, 'end')
        for i in self.templates:
            self.file_list.insert('end',  i)

    
    def load_template(self,  event=None):
        path = self.configs["TEMPLATE_FOLDER"]
        self.selected_items = self.file_list.curselection()
        file_name = self.file_list.get(self.selected_items)
        template = path + "/" + file_name
        template = os.path.abspath(template)

        file = open(template,  mode='r',  encoding = "utf-8").read()
        # self.loaded_template = file
        self.temp_text.delete("1.0", 'end')
        self.temp_text.insert('end', file)

        self.rename_entry.delete(0, 'end')
        self.rename_entry.insert('end', file_name)

        self.update_templates()


    def export_folder(self):
        self.files = list(self.file_list.get(0, END))
        # print(self.files)

    @property
    def default_template(self):
        file = '''
<!DOCTYPE html>
<html lang="en-US">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width,  initial-scale=1.0">
    <title>{{title}}</title>
</head>
<body>
  {% set anterior = namespace('') %}
  {% set anterior.content = highlights[0].content %}
  </pre>
  <h1>{{title}}</h1>
  <article>
  {%- for annot in highlights %}
    {%- if annot.text -%}
    {%- if  annot.content -%}
    <p style="background-color: {{annot.color_name}};">{{annot.type}} - {{annot.text}}</p>
    <li>{{annot.content}}</li>
    {%- else -%}
    <p style="background-color: {{annot.color_name}};">{{annot.type}} - {{annot.text}}</p>
    {%- endif -%}
    {% else %}
    {%- if  annot.text -%}
    <li>{{annot.type}} - {{annot.content}}</li>
    {%- else -%}
    {%- endif -%}
    {%- endif -%}

  {% endfor -%}


</article>

</body>
</html> 
        '''
        return file

    def add_template(self):
        # if self.selected_items:
        self.selected_items = []
        file = self.default_template
        self.temp_text.delete("1.0", 'end')
        self.temp_text.insert('end', file)
        self.rename_entry.delete(0, 'end')
        self.rename_entry.insert('end', "new_template.html")
        self.update_templates()

    def del_template(self):
        if self.selected_items:
            delete_argument = ["--delete-template", f'{self.file_list.get(self.selected_items)}']
            cli.main(delete_argument)
            self.selected_items = []
        self.update_templates()

    def rename_template(self):
        name = "random_write_" + ''.join(random_choices(string.ascii_letters, k = 7))
        file_name = os.path.abspath(name)
        file = open(file_name, mode = 'w', encoding= 'utf-8')
        template = self.temp_text.get(1.0, 'end')
        # print(template)
        file.write(template)
        file.close()

        if self.selected_items:
            rename_argument_1 = ["--rename-template", f'{self.file_list.get(self.selected_items)}', f'{self.rename_entry.get()}']
            cli.main(rename_argument_1)
        add_argument = ['--import-template', f'{file_name}']
        rename_argument = ["--rename-template", f'{name}', f'{self.rename_entry.get()}']
        cli.main(add_argument)
        cli.main(rename_argument)

        self.selected_items = []

        os.remove(file_name)

            
        self.update_templates()

    def remove_all_files(self):
        self.file_list.delete(0, END)

    def remove_file(self):
        selected_items = self.file_list.curselection()
        for item in selected_items:
            # print(item)
            self.file_list.delete(item)
