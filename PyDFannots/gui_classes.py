import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
# import string as str
import pathlib
from time import sleep

import os
import PyDFannots.cli as cli
import PyDFannots.utils as utils
import re
import json
import shutil
from random import choices as random_choices
import string

class gui_interface():
    def __init__(self, master = None) -> None:
        self.__master = master
        self.ui = ttk.Frame(self.__master)
        self.__file_location = os.path.abspath(pathlib.Path(__file__).parent)
        self.__cli = cli
        self.__entry_text = tk.StringVar()

    



class gui_pdf_load(gui_interface):
    def __init__(self, master = None) -> None:
        self.__master = master
        self.ui = tk.Frame(self.__master)
        self.__file_location = os.path.abspath(pathlib.Path(__file__).parent)

        self.set_size()
        self.assets_import()
        self.set_initial_vars()
        self.basic_ui()
        self.basic_ui_draw()
        self.basic_ui_commmands()
        
    def set_initial_vars(self):
        self.values_format = ["Template","csv","json"]
        self.var_format = tk.StringVar()
        self.var_format.set(self.values_format[0])
        
        self.var_il = tk.DoubleVar()
        self.var_il.set(0.1)
        self.var_col = tk.IntVar()
        self.var_col.set(1)
        self.var_tol = tk.DoubleVar()
        self.var_tol.set(0.1)
        self.var_template = tk.StringVar()
        
        self.var_parameters = tk.StringVar()
        self.var_parameters.set("")
        # self.set_properties()
        
        # self.var_il.trace('w', self.set_cfg)
        # self.var_col.trace('w', self.set_cfg)
        # self.var_tol.trace('w', self.set_cfg)
        # self.var_template.trace('w', self.set_cfg)
        # self.var_format.trace('w', self.set_cfg)

    def assets_import(self):
        self.icon_delete = tk.PhotoImage(file = os.path.abspath(self.__file_location + "//gui_assets//delete.png"))
        self.icon_trash = tk.PhotoImage(file = os.path.abspath(self.__file_location + "//gui_assets//trash.png"))
       
    def basic_ui(self):
        self.row_1 = tk.Frame(self.ui,highlightbackground="blue", highlightthickness=2)
        self.row_2 = tk.Frame(self.ui,highlightbackground="green", highlightthickness=2)
        self.row_3 = tk.Frame(self.ui,highlightbackground="cyan", highlightthickness=2)
        self.file_list = tk.Listbox(self.row_1)

        

        self.btn_file_selector = ttk.Button(self.row_1,text="Select files")
        self.btn_pdf_export = ttk.Button(self.row_1, text = "Export PDF highlights")

        # Grid com atalhos para remover item selecionado ou todos
        self.column_btns = ttk.Frame(self.row_1)
        self.btn_remove_item = ttk.Button(self.column_btns,image=self.icon_delete)
        self.btn_remove_all = ttk.Button(self.column_btns,image=self.icon_trash)

        self.parameters_tab = ttk.Frame(self.row_2)
        self.parameters_label = ttk.Label(self.parameters_tab,text = "Add parameters")
        self.parameters_template_label = ttk.Label(self.parameters_tab,text="Select a template")
        self.parameters_template = ttk.Combobox(self.parameters_tab,textvariable=self.var_template, state = 'readonly', )
        self.parameters_il_label = ttk.Label(self.parameters_tab,text="Select a intersection level between text and highlights.")
        self.parameters_il = ttk.Spinbox(self.parameters_tab,from_=0,to=1, increment=0.1, state = 'readonly', textvariable=self.var_il)
        self.parameters_entry = ttk.Label(self.parameters_tab,textvariable=self.var_parameters)
        self.parameters_col = ttk.Spinbox(self.parameters_tab,from_=1,to=15, increment=1, state = 'readonly', textvariable=self.var_col)
        self.parameters_col_label = ttk.Label(self.parameters_tab,text="Select number of columns in PDF.")
        self.parameters_tol_label = ttk.Label(self.parameters_tab,text="Select tolerance interval for columns")
        self.parameters_tol = ttk.Spinbox(self.parameters_tab,from_=0,to=1, increment=0.1, state = 'readonly', textvariable=self.var_tol)
        # Default format export set to template
        self.parameters_format_label = ttk.Label(self.parameters_tab,text="Select export format.")
        self.parameters_format = ttk.Combobox(self.parameters_tab,textvariable=self.var_format, state = 'readonly', )
        
        self.parameters_cfg_label = ttk.Label(self.parameters_tab,text="Load saved config.")
        self.parameters_cfg_load = ttk.Button(self.parameters_tab,text="Load",command=self.load_cfg)
        self.parameters_cfg_save = ttk.Button(self.parameters_tab,text="Save",command=self.save_cfg)
        
        # Status bar
        self.status_bar = ttk.Label(self.row_3)

    def basic_ui_draw(self):
        self.ui.grid(sticky='nwse')
        self.row_1.grid(column = 1, row = 1,sticky='nwse')
        self.row_2.grid(column = 1, row = 2,sticky='nwse')
        self.row_3.grid(column = 1, row = 3,sticky='nwse')
        self.file_list.grid(column = 1, row = 1, columnspan = 3,sticky = "nwse")

        self.btn_file_selector.grid(column=1,row = 2,sticky = "nwse")
        self.btn_pdf_export.grid(column=2,row = 2,sticky = "nwse")
        self.ui.grid_columnconfigure(1,weight=7)
        
        self.ui.grid_rowconfigure(1,weight=7)
        self.ui.grid_rowconfigure(2,weight=3)

        self.column_btns.grid(column=4,row=1,rowspan=2)
        self.btn_remove_item.grid()
        self.btn_remove_all.grid()

        self.row_1.grid_columnconfigure(1,weight=3)
        self.row_1.grid_columnconfigure(2,weight=3)
        self.row_1.grid_columnconfigure(3,weight=6)
        
        self.row_1.grid_rowconfigure(1,weight=7)
        # self.row_1.grid_rowconfigure(2,weight=3)
        # self.row_1.grid_rowconfigure(3,weight=6)

        self.row_2.grid_columnconfigure(1,weight=6)
        self.row_2.grid_columnconfigure(2,weight=3)
        self.row_2.grid_columnconfigure(3,weight=3)

        self.parameters_tab.grid(column = 0, row = 0,sticky = "nwse")
        self.parameters_label.grid(row = 0, sticky = "nwse")
        self.parameters_entry.grid(row = 0, column = 1,sticky = "nwse", columnspan=2)
        self.parameters_template_label.grid(row = 1, sticky = "nwse")
        self.parameters_template.grid(row = 1, column = 1,sticky = "nwse")
        self.parameters_il_label.grid(row = 2, sticky = "nwse")
        self.parameters_il.grid(row = 2, column = 1,sticky = "nwse")
        self.parameters_col_label.grid(row = 3, sticky = "nwse")
        self.parameters_col.grid(row = 3, column = 1,sticky = "nwse")
        self.parameters_tol_label.grid(row = 4, sticky = "nwse")
        self.parameters_tol.grid(row = 4, column = 1,sticky = "nwse")
        self.parameters_format_label.grid(row = 5, sticky = "nwse")
        self.parameters_format.grid(row = 5, column = 1,sticky = "nwse")
        self.parameters_cfg_label.grid(row = 6, sticky = "nwse")
        self.parameters_cfg_load.grid(row = 7, sticky = "nwse")
        self.parameters_cfg_save.grid(sticky = "nwse")
        
        self.status_bar.grid(sticky="nwse")
        self.set_cfg()
    
    @property
    def arguments(self):
        parameters = f'-il {self.cfg["il"]} --columns {self.cfg["col"]} -tol  {self.cfg["tol"]} --template "{self.cfg["template"]}"'
        if not self.cfg["format"] == "Template":
            parameters = f'{parameters}  --format {self.cfg["format"]}'
        # # print(parameters)
        self.var_parameters.set(parameters)
        return parameters
    
    def edit_parameters(self):
        parameters = f'-il {self.cfg["il"]} --columns {self.cfg["col"]} -tol  {self.cfg["tol"]} --template "{self.cfg["template"]}"'
        self.parameters_arguments = list()
        if not self.cfg["format"] == "Template":
            parameters = f'{parameters}  --format {self.cfg["format"]}'
            self.parameters_arguments.append(['--format',self.cfg["format"]])
        self.parameters_arguments.append(['-il',self.cfg["il"]])
        self.parameters_arguments.append(['--columns',self.cfg["col"]])
        self.parameters_arguments.append(['-tol',self.cfg["tol"]])
        
        self.var_parameters.set(parameters)
        # print("Arguments: ",self.arguments)
        
    def set_cfg(self,event=None):
        if not hasattr(self,"cfg"):
            self.cfg = {}
        self.cfg["il"] = self.var_il.get()
        self.cfg["col"] = self.var_col.get()
        self.cfg["tol"] = self.var_tol.get()
        self.cfg["template"] = self.var_template.get()
        self.cfg["format"] = self.var_format.get()
        # print(self.cfg)
        self.edit_parameters()
        
    def set_vars(self):
        self.var_il.set(self.cfg["il"])
        self.var_col.set(self.cfg["col"])
        self.var_tol.set(self.cfg["tol"])
        self.var_template.set(self.cfg["template"])
        self.var_format.set(self.cfg["format"])
        self.set_cfg()
        
    def set_new_cfg(self,cfg:dict):
        if cfg.keys() == self.cfg.keys():
            for entry in cfg:
                self.cfg[entry] = cfg[entry]
            self.set_vars()
            self.set_cfg()
            self.cfg_validate()
        
    def cfg_validate(self, event = None):
        if not isinstance(self.cfg["il"],float):
            self.var_col.set(0.1)
        if not isinstance(self.cfg["col"],int):
            self.var_col.set(1)
        if not isinstance(self.cfg["tol"],float):
            self.var_tol.set(0.1)
        if not self.cfg["template"] in self.templates:
            self.var_template.set("template_html.html")
        self.set_cfg()
        
    def load_cfg(self,event = None):
        file_cfg = filedialog.askopenfile(title="Select config file",mode='r',filetypes=(('json file','*.json'),))
        cfg = json.load(file_cfg)
        self.set_new_cfg(cfg)
        # print(list(cfg.keys()))
        self.status_bar["text"] = f'Configs loaded from: {file_cfg.name}'
    
    def save_cfg(self,event = None):
        self.set_cfg()
        file_cfg = filedialog.asksaveasfilename(title="Save config file",filetypes=(('json file','*.json'),),defaultextension="json")
        cfg = json.dumps(self.cfg,ensure_ascii=True,indent=4)
        with open(file_cfg,mode='w',encoding="utf-8") as f:
            f.write(cfg)
        self.status_bar["text"] = f'Configs saved at: {file_cfg}'

    def basic_ui_commmands(self):
        self.btn_file_selector['command'] = self.add_file
        self.btn_remove_all["command"] = self.remove_all
        self.btn_remove_item["command"] = self.remove_file
        self.btn_pdf_export["command"] = self.export_folder
        
        self.var_il.set(0.1)
        self.var_col.set(1)
        self.var_tol.set(0.1)
        # self.parameters_format.set("Template")
        
        self.parameters_il.bind("<ButtonRelease>", self.cfg_validate)
        self.parameters_tol.bind("<ButtonRelease>", self.cfg_validate)
        self.parameters_col.bind("<ButtonRelease>", self.cfg_validate)
        self.parameters_template.bind("<ButtonRelease>", self.cfg_validate)
        self.parameters_format.bind("<ButtonRelease>", self.cfg_validate)
        
        self.parameters_il.bind("<Leave>", self.cfg_validate)
        self.parameters_tol.bind("<Leave>", self.cfg_validate)
        self.parameters_col.bind("<Leave>", self.cfg_validate)
        self.parameters_template.bind("<Leave>", self.cfg_validate)
        self.parameters_format.bind("<Leave>", self.cfg_validate)
        
        self.parameters_il.bind("<Enter>", self.cfg_validate)
        self.parameters_tol.bind("<Enter>", self.cfg_validate)
        self.parameters_col.bind("<Enter>", self.cfg_validate)
        self.parameters_template.bind("<Enter>", self.cfg_validate)
        self.parameters_format.bind("<Enter>", self.cfg_validate)
        
        self.templates = cli.main(['--list-templates'])
        self.configs = cli.main(['--list-configs'])
        
        self.parameters_template["values"] = self.templates
        self.parameters_format["values"] = self.values_format
        
        self.var_template.set("template_html.html")

        self.file_list.drop_target_register(DND_FILES)

        self.file_list.dnd_bind("<<Drop>>", self.add_file_drag_drop) 
        self.set_cfg()

    def add_file_drag_drop(self,event):
        list_files = event.data
        if bool(re.search("^\\{",list_files)):
            list_files = re.sub('[ ]+\{',"",list_files)
            list_files = re.sub('\{',"",list_files)
            list_files = re.sub('\\\\',"/",list_files)
            list_files = re.sub('\}',";",list_files)
            list_files = re.sub('^[ ]+',"",list_files)
            lista = list_files.split(";")
        else:
            lista = list_files.split()
        # print(lista)
        
        for i in lista:
            if not i == '':
                self.file_list.insert("end",re.sub("^[ ]+","",i))
        self.validate_files()

    def validate_files(self):
        self.files = list(self.file_list.get(0,tk.END))
        for i in range(0,len(self.files)):
            self.files[i] = re.sub("\\\\","/",self.files[i])
            # print(i)
        self.files = set(self.files)
        self.files = list(self.files)

        self.remove_all()

        for i in self.files:
            
            self.file_list.insert("end", i)
        self.status_bar["text"] = f'There are {len(self.files)} PDFs files. '



    def export_folder(self):
        self.files = list(self.file_list.get(0,tk.END))
        # print(self.files)

        if len(self.files) >= 1:
            self.folder = filedialog.askdirectory(title="Select export folder")
            # self.folder = str(os.path.abspath(self.folder))
            
            self.cfg_validate()
            self.pdf_export(pdf_location=self.files,export = self.folder)
        else:
            messagebox.showerror(title = "Select at least one PDF file.",
            message = "You have to select at least one PDF file on the <Select files> button.")

    def add_file(self):
        file_open = filedialog.askopenfiles(defaultextension=['pdf'],filetypes=[('PDF','.pdf')])
        if isinstance(file_open,list):
            for i in file_open:
                file = i.name
                path = os.path.abspath(file)
                self.file_list.insert("end", path)
        else:
            path = os.path.abspath(file_open)
            self.file_list.insert("end", path)
        self.validate_files()

    def remove_all(self):
        self.file_list.delete(0,tk.END)
    
    def remove_file(self):
        selected_items = self.file_list.curselection()
        for item in selected_items:
            # print(item)
            self.file_list.delete(item)

    def set_size(self,width = 500, height = 500):
        self.width = width
        self.height = height

    def pdf_export(self,pdf_location = [], export = 'output/',config_file = ""):
        if os.path.exists(export) == False:
            os.mkdir(export)
            
        self.edit_parameters()
        
        for pdf in pdf_location:
            
            status = "Making PDF file: " + pdf
            # print(status)
            self.status_bar["text"] = status
        

            pdf = re.sub("[\\\\]+","/",pdf)
            
            pdf_path = os.path.abspath(pdf)
            
            pdf_path = re.sub("[\\\\]+","/",pdf_path)

            # print("\n\nPDF location: ",pdf)
            
            input_file = ['-i',pdf_path,'-o',export]#'python pydfannots.py -i "' + pdf_path + '" '
            # output_file = ['-o',export]
            #execution_path = execution_path + ' -o "' + export + '" '
            
            # print("\n\nPDF: ",execution_path)
            
            if os.path.exists(config_file):
                argument = input_file + ['-config',config_file]
                # execution_path = execution_path + ' -config "' + config_file + '" '
            else:
                argument = input_file + ['-il',f'{self.cfg["il"]}', '-tol',f'{self.cfg["tol"]}','--columns',f'{self.cfg["col"]}','--template',f'{self.cfg["template"]}']
                # execution_path = execution_path + self.parameters_entry["text"]
            print(argument)
            # os.popen(execution_path).read()
            cli.main(argument)

        # print("\n\nEnd!")






class gui_settings(gui_interface):
    def __init__(self, master = None) -> None:
        self.__master = master
        self.ui = tk.Frame(self.__master)

        self.basic_ui()
        self.basic_ui_draw()
        self.basic_ui_commmands()
        self.selected_items = []

       
    def basic_ui(self):
        self.style = ttk.Style(self.ui)
        self.style.configure('lefttab.TNotebook', tabposition='wn')
        
        self.notebook = ttk.Notebook(self.ui, style='lefttab.TNotebook')
        
        
        
        # Config of template tab
        self.template_tab = tk.Frame(self.ui,highlightbackground="cyan", highlightthickness=2)
        self.col_1 = tk.Frame(self.template_tab,highlightbackground="blue", highlightthickness=2)
        self.col_2 = tk.Frame(self.template_tab,highlightbackground="green", highlightthickness=2)
        self.file_list = tk.Listbox(self.col_1)
        self.temp_text = tk.Text(self.col_2)
        self.btn_add_template = ttk.Button(self.col_1,text="+")
        self.btn_del_template = ttk.Button(self.col_1, text = "-")
        self.btn_load_template = ttk.Button(self.col_1, text = "Load external template")
        # Grid com atalhos para remover item selecionado ou todos
        self.column_btns = ttk.Frame(self.col_1)
        # self.btn_remove_item = ttk.Button(self.column_btns,image=self.icon_delete)
        # self.btn_remove_all = ttk.Button(self.column_btns,image=self.icon_trash)

        self.parameters_tab = ttk.Frame(self.col_2)
        self.parameters_label = ttk.Label(self.parameters_tab,text = "Adicione parametros")
        self.rename_entry = ttk.Entry(self.parameters_tab)
        self.btn_rename_template = ttk.Button(self.parameters_tab, text = "Save")
        
        #### Configs template
        self.configs_tab = ttk.Frame(self.ui)
        self.config_items = dict()
        self.config_labels = dict()

    def basic_ui_draw(self):
        self.ui.grid_columnconfigure(0,weight=10)
        self.notebook.grid(sticky="nwse",row=0,column=0)
        
        self.col_1.grid(column = 1, row = 1,sticky='nwse', rowspan=3)
        self.col_2.grid(column = 2, row = 1,sticky='nwse')
        self.file_list.grid(column = 1, row = 1, columnspan = 3,sticky = "nwse")
        self.temp_text.grid(sticky="nwse")
        self.btn_add_template.grid(column=1,row = 2,sticky = "nwse")
        self.btn_del_template.grid(column=2,row = 2,sticky = "nwse")
        self.btn_load_template.grid(column=3, row = 2, sticky = "nwse")
        self.temp_text.grid(row = 3,sticky="nwse")
        
        self.template_tab.grid_columnconfigure(1,weight=7)
        self.template_tab.grid_columnconfigure(2,weight=3)

        self.column_btns.grid(column=4,row=1,rowspan=2)

        self.col_1.grid_columnconfigure(1,weight=3)
        self.col_1.grid_columnconfigure(2,weight=3)
        self.col_1.grid_columnconfigure(3,weight=3)


        self.col_2.grid_columnconfigure(0,weight=1)


        self.parameters_tab.grid(column = 0, row = 0,sticky = "nwse")
        self.parameters_label.grid(sticky = "nwse")
        self.rename_entry.grid(sticky = "nwse", columnspan=2)
        self.btn_rename_template.grid(row = 1, column=4,sticky = "nwse")
        
        ### Config tab
        self.configs_tab.grid(sticky="nwse")
        self.configs_tab.grid_columnconfigure(0, weight=1)
        
        

    def basic_ui_commmands(self):
        self.notebook.add(self.template_tab,text = "Templates")
        self.notebook.add(self.configs_tab,text = "Configuration")
        self.btn_add_template['command'] = self.add_template
        self.btn_del_template["command"] = self.del_template
        self.btn_rename_template["command"] = self.rename_template
        self.file_list.bind("<ButtonRelease>",self.load_template)
        
        # self.templates = cli.main(['--list-templates'])
        self.update_templates()
        self.configs = cli.main(['--list-configs'])
        
        for conf in self.configs:
            config = self.configs[conf]
            print(f'{conf}: {config} - {type(config)}')
            self.config_items[conf] = dict()
            self.config_items[conf]["frame"] = ttk.Frame(self.configs_tab)
            self.config_items[conf]["label"] = ttk.Label(self.config_items[conf]["frame"],text=conf, width=30)
            
            if isinstance(config, str):
                self.config_items[conf]["entry"] = tk.Entry(self.config_items[conf]["frame"], width = 60)
            elif isinstance(config,list):
                self.config_items[conf]["entry"] = tk.Entry(self.config_items[conf]["frame"],width = 60)
            elif isinstance(config,bool):
                self.config_items[conf]["vars"] = tk.IntVar()
                self.config_items[conf]["entry"] = tk.Checkbutton(self.config_items[conf]["frame"], variable=self.config_items[conf]["vars"])
            elif isinstance(config,float):
                self.config_items[conf]["entry"] = tk.Entry(self.config_items[conf]["frame"], width = 60)
            else:
                self.config_items[conf]["entry"] = tk.Entry(self.config_items[conf]["frame"], width = 60)
            self.config_items[conf]["frame"].grid(sticky="nwse")
            self.config_items[conf]["label"].grid(column = 1,row = 1,sticky="WE")
            self.config_items[conf]["entry"].grid(column = 2,row = 1,sticky="WE")
        self.set_config()
            
    def set_config(self):
        for conf in self.configs:
            config = self.configs[conf]
            tk_item = self.config_items[conf]["entry"]
            if isinstance(tk_item, (tk.Entry)):
                self.config_items[conf]["entry"].delete(0,"end")
                self.config_items[conf]["entry"].insert("end",''.join(str(config)))
            elif isinstance(tk_item, tk.Checkbutton):
                self.config_items[conf]["vars"].set(config)
            else:
                self.config_items[conf]["entry"].delete(0,"end")
                self.config_items[conf]["entry"].insert("end",config)

        
        # print(self.configs)
        
            
    def update_templates(self):
        self.templates = cli.main(['--list-templates'])
        self.file_list.delete(0,"end")
        for i in self.templates:
            self.file_list.insert("end", i)
            
    
    def load_template(self, event=None):
        path = self.configs["TEMPLATE_FOLDER"]
        self.selected_items = self.file_list.curselection()
        file_name = self.file_list.get(self.selected_items)
        template = path + "//" + file_name
        template = os.path.abspath(template)
        
        file = open(template, mode='r', encoding = "utf-8").read()
        # self.loaded_template = file
        self.temp_text.delete("1.0","end")
        self.temp_text.insert("end",file)
        
        self.rename_entry.delete(0,"end")
        self.rename_entry.insert("end",file_name)
        
        self.update_templates()
        

    def export_folder(self):
        self.files = list(self.file_list.get(0,tk.END))
        # print(self.files)
    
    @property
    def default_template(self):
        file = '''
<!DOCTYPE html>
<html lang="en-US">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{title}}</title>
</head>
<body>
  {% set anterior = namespace('') %}
  {% set anterior.content = highlights[0].content %}
  </pre>
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

  {% endfor -%}'


</article>

</body>
</html> 
        '''
        return file

    def add_template(self):
        # if self.selected_items:
        self.selected_items = []
        file = self.default_template
        self.temp_text.delete("1.0","end")
        self.temp_text.insert("end",file)
        self.rename_entry.delete(0,"end")
        self.rename_entry.insert("end","new_template.html")
        self.update_templates()
    
    def del_template(self):
        if self.selected_items:
            delete_argument = ["--delete-template",f'{self.file_list.get(self.selected_items)}']
            cli.main(delete_argument)
            self.selected_items = []
        self.update_templates()

    def rename_template(self):
        name = "random_write_" + ''.join(random_choices(string.ascii_letters,k = 7))
        file_name = os.path.abspath(name)
        file = open(file_name,mode = 'w',encoding= 'utf-8')
        template = self.temp_text.get(1.0,'end')
        print(template)
        file.write(template)
        file.close()
        
        if self.selected_items:
            rename_argument_1 = ["--rename-template",f'{self.file_list.get(self.selected_items)}',f'{self.rename_entry.get()}']
            cli.main(rename_argument_1)
        add_argument = ['--import-template',f'{file_name}']
        rename_argument = ["--rename-template",f'{name}',f'{self.rename_entry.get()}']
        cli.main(add_argument)
        cli.main(rename_argument)
        # if self.selected_items:
        #     cli.main(delete_argument)
        # os.popen(add_argument)
        # cli.main(add_argument)
        
        self.selected_items = []
        
        os.remove(file_name)
        
        # rename_argument = f'python pydfannots.py  --rename-template "{name}" {self.rename_entry.get()}'
        # cli.main(rename_argument)
        # os.popen(rename_argument)
            
            
        self.update_templates()

    def remove_all(self):
        self.file_list.delete(0,tk.END)
    
    def remove_file(self):
        selected_items = self.file_list.curselection()
        for item in selected_items:
            # print(item)
            self.file_list.delete(item)

    def set_size(self,width = 500, height = 500):
        self.width = width
        self.height = height


