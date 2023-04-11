import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
import string as str
import pathlib

import os
import PyDFannots.cli as cli
import PyDFannots.utils as utils
import re
import json
import shutil


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
        self.basic_ui()
        self.basic_ui_draw()
        self.basic_ui_commmands()

    def assets_import(self):
        self.icon_delete = tk.PhotoImage(file = os.path.abspath(self.__file_location + "//gui_assets//delete.png"))
        self.icon_trash = tk.PhotoImage(file = os.path.abspath(self.__file_location + "//gui_assets//trash.png"))
       
    def basic_ui(self):
        self.column_1 = tk.Frame(self.ui,highlightbackground="blue", highlightthickness=2)
        self.column_2 = tk.Frame(self.ui,highlightbackground="green", highlightthickness=2)
        self.file_list = tk.Listbox(self.column_1)

        

        self.btn_file_selector = ttk.Button(self.column_1,text="Select files")
        self.btn_pdf_export = ttk.Button(self.column_1, text = "Export PDF highlights")

        # Grid com atalhos para remover item selecionado ou todos
        self.column_btns = ttk.Frame(self.column_1)
        self.btn_remove_item = ttk.Button(self.column_btns,image=self.icon_delete)
        self.btn_remove_all = ttk.Button(self.column_btns,image=self.icon_trash)

        self.parameters_tab = ttk.Frame(self.column_2)
        self.parameters_label = ttk.Label(self.parameters_tab,text = "Add parameters")
        # self.parameters_entry = ttk.Entry(self.parameters_tab)
        self.parameters_template_label = ttk.Label(self.parameters_tab,text="Select a template")
        self.parameters_template = ttk.Combobox(self.parameters_tab)
        self.parameters_il_label = ttk.Label(self.parameters_tab,text="Select a intersection level between text and highlights.")
        self.parameters_il = ttk.Spinbox(self.parameters_tab,from_=0,to=1, increment=0.1)
        self.parameters_entry = ttk.Entry(self.parameters_tab)

    def basic_ui_draw(self):
        self.column_1.grid(column = 1, row = 1,sticky='nwse')
        self.column_2.grid(column = 2, row = 1,sticky='nwse')
        self.file_list.grid(column = 1, row = 1, columnspan = 3,sticky = "nwse")

        self.btn_file_selector.grid(column=1,row = 2,sticky = "nwse")
        self.btn_pdf_export.grid(column=2,row = 2,sticky = "nwse")
        self.ui.grid_columnconfigure(1,weight=7)
        self.ui.grid_columnconfigure(2,weight=3)

        self.column_btns.grid(column=4,row=1,rowspan=2)
        self.btn_remove_item.grid()
        self.btn_remove_all.grid()

        self.column_1.grid_columnconfigure(1,weight=3)
        self.column_1.grid_columnconfigure(2,weight=3)
        self.column_1.grid_columnconfigure(3,weight=6)


        self.column_2.grid_columnconfigure(0,weight=1)


        self.parameters_tab.grid(column = 0, row = 0,sticky = "nwse")
        self.parameters_label.grid(sticky = "nwse")
        self.parameters_entry.grid(sticky = "nwse")
        self.parameters_template_label.grid(sticky = "nwse")
        self.parameters_template.grid(sticky = "nwse")
        self.parameters_il_label.grid(sticky = "nwse")
        self.parameters_il.grid(sticky = "nwse")
        self.edit_parameters()
        
    def edit_parameters(self):
        self.parameters_entry.delete('0','end')
        self.parameters_entry.insert('0','aaaaaaaaaaaas')

    def basic_ui_commmands(self):
        self.btn_file_selector['command'] = self.add_file
        self.btn_remove_all["command"] = self.remove_all
        self.btn_remove_item["command"] = self.remove_file
        self.btn_pdf_export["command"] = self.export_folder
        
        self.parameters_template["values"] = cli.main(['--list-templates'])
        self.parameters_template["command"] = self.edit_parameters()
        
        
        
        # print(os.popen("python pydfannots.py --list-templates").read())

        self.file_list.drop_target_register(DND_FILES)

        self.file_list.dnd_bind("<<Drop>>", self.add_file_drag_drop) #lambda e: self.file_list.insert("end", e.data))


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
        print(lista)
        
        for i in lista:
            if not i == '':
                self.file_list.insert("end",re.sub("^[ ]+","",i))
        self.validate_files()

    def validate_files(self):
        self.files = list(self.file_list.get(0,tk.END))
        for i in range(0,len(self.files)):
            self.files[i] = re.sub("\\\\","/",self.files[i])
            print(i)
        self.files = set(self.files)
        self.files = list(self.files)

        self.remove_all()

        for i in self.files:
            
            self.file_list.insert("end", i)



    def export_folder(self):
        self.files = list(self.file_list.get(0,tk.END))
        print(self.files)

        if len(self.files) >= 1:
            self.folder = filedialog.askdirectory(title="Select export folder")
            # self.folder = str(os.path.abspath(self.folder))
            
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
            print(item)
            self.file_list.delete(item)

    def set_size(self,width = 500, height = 500):
        self.width = width
        self.height = height

    def pdf_export(self,pdf_location = [], export = 'output/',config_file = ""):
        if os.path.exists(export) == False:
            os.mkdir(export)
        
        for pdf in pdf_location:

            pdf = re.sub("\\\\","//",pdf)
            
            pdf_path = os.path.abspath(pdf)

            print("\n\nPDF location: ",pdf)
            
            execution_path = 'python pydfannots.py -i "' + pdf_path + '" '
            execution_path = execution_path + ' -o "' + export + '" '
            if os.path.exists(config_file):
                execution_path = execution_path + ' -config "' + config_file + '" '
            if self.parameters_entry.get():
                execution_path = execution_path + self.parameters_entry.get()
            print(execution_path)
            os.popen(execution_path)

        print("\n\nEnd!")






class gui_settings(gui_interface):
    def __init__(self, master = None) -> None:
        self.__master = master
        self.ui = tk.Frame(self.__master)

        self.basic_ui()
        self.basic_ui_draw()
        self.basic_ui_commmands()

       
    def basic_ui(self):
        self.column_1 = tk.Frame(self.ui,highlightbackground="blue", highlightthickness=2)
        self.column_2 = tk.Frame(self.ui,highlightbackground="green", highlightthickness=2)
        self.file_list = tk.Listbox(self.column_1)
        self.btn_file_selector = ttk.Button(self.column_1,text="Select files")
        self.btn_pdf_export = ttk.Button(self.column_1, text = "Export PDF highlights")

        # Grid com atalhos para remover item selecionado ou todos
        self.column_btns = ttk.Frame(self.column_1)
        # self.btn_remove_item = ttk.Button(self.column_btns,image=self.icon_delete)
        # self.btn_remove_all = ttk.Button(self.column_btns,image=self.icon_trash)

        self.parameters_tab = ttk.Frame(self.column_2)
        self.parameters_label = ttk.Label(self.parameters_tab,text = "Adicione parametros")
        self.parameters_entry = ttk.Entry(self.parameters_tab)

    def basic_ui_draw(self):
        self.column_1.grid(column = 1, row = 1,sticky='nwse')
        self.column_2.grid(column = 2, row = 1,sticky='nwse')
        self.file_list.grid(column = 1, row = 1, columnspan = 3,sticky = "nwse")
        self.btn_file_selector.grid(column=1,row = 2,sticky = "nwse")
        self.btn_pdf_export.grid(column=2,row = 2,sticky = "nwse")
        self.ui.grid_columnconfigure(1,weight=7)
        self.ui.grid_columnconfigure(2,weight=3)

        self.column_btns.grid(column=4,row=1,rowspan=2)
        # self.btn_remove_item.grid()
        # self.btn_remove_all.grid()

        self.column_1.grid_columnconfigure(1,weight=3)
        self.column_1.grid_columnconfigure(2,weight=3)
        self.column_1.grid_columnconfigure(3,weight=6)


        self.column_2.grid_columnconfigure(0,weight=1)


        self.parameters_tab.grid(column = 0, row = 0,sticky = "nwse")
        self.parameters_label.grid(sticky = "nwse")
        self.parameters_entry.grid(sticky = "nwse")

    def basic_ui_commmands(self):
        self.btn_file_selector['command'] = self.add_file
        # self.btn_remove_all["command"] = self.remove_all
        # self.btn_remove_item["command"] = self.remove_file
        self.btn_pdf_export["command"] = self.export_folder

    def export_folder(self):
        self.files = list(self.file_list.get(0,tk.END))
        print(self.files)

        if len(self.files) >= 1:
            self.folder = filedialog.askdirectory(title="Select export folder")
            # self.folder = str(os.path.abspath(self.folder))
            
            self.pdf_export(pdf_location=self.files,export = self.folder)
        else:
            messagebox.showerror(title = "Select at least one PDF file.",
            message = "You have to select at least one PDF file on the <Select files> button.")

    def add_file(self):
        file_open = filedialog.askopenfiles(defaultextension=['pdf'],filetypes=[('PDF','.pdf')])
        if isinstance(file_open,list):
            for i in file_open:
                path = str(os.path.abspath(i.name))
                # self.file_list
                self.file_list.insert("end", path)

    def remove_all(self):
        self.file_list.delete(0,tk.END)
    
    def remove_file(self):
        selected_items = self.file_list.curselection()
        for item in selected_items:
            print(item)
            self.file_list.delete(item)

    def set_size(self,width = 500, height = 500):
        self.width = width
        self.height = height


