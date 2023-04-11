import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
import tkinter.ttk as ttk
import PyDFannots.gui_classes as gui
import PyDFannots.utils as utils
import os
import json
import re


def execute_pdf_annot(pdf_location = ['tests/PDF_WIKI.pdf'],export = 'output/', config_file = ""):
    anotacoes = {}
    # os.mkdir("temp/")
    if os.path.exists(export) == False:
        os.mkdir(export)
    
    for pdf in pdf_location:
        print("PDF: ", pdf)
        execution_path = "python pydfannots.py -i " + pdf
        execution_path = execution_path + " -o " + export
        execution_path = execution_path + " -cfg " + config_file
        os.system(execution_path)

    


def main():

    # root = tk.Tk()

    root = TkinterDnD.Tk()

    root.geometry('800x800')

    root.minsize(width = 600, height = 400)

    def _quit():
        root.quit()
        root.destroy()
        print("BDU fechado")

    
    root.protocol("WM_DELETE_WINDOW", _quit)


    notebook = ttk.Notebook(root)
    # notebook.grid()
    notebook.grid_rowconfigure(1, weight=1)
    notebook.grid_columnconfigure(1, weight=1)

    load_pdf = gui.gui_pdf_load(notebook)

    load_pdf.set_size(width=root.winfo_screenmmwidth(),height=root.winfo_screenmmheight())


    pdf_settings = gui.gui_settings(notebook)

    # load_pdf.file_list.drop_target_register(DND_FILES)
    # load_pdf.file_list.dnd_bind('<<Drop>>', lambda e: load_pdf.file_list.insert(tk.END, e.data.sub('\\{','').strip('}')))

    


    root.title = "AAA"
    root.state('zoomed')

    notebook.grid(sticky = "nsew")


    notebook.add(load_pdf.ui,text="File choose")
    notebook.add(pdf_settings.ui, text="Settings")

    notebook.grid_columnconfigure(0,weight=10)
    notebook.grid_columnconfigure(1,weight=10)

    root.grid_columnconfigure(0,weight=1)

    print(root.winfo_screenwidth())
    # noteb

    root.mainloop()


    root.quit()

if(__name__ == "__main__"):
	main()