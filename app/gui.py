#!/usr/bin/env python
"""GUI for app
"""
import tkinter as tk
import tkinter.ttk as ttk

from tkinterdnd2 import TkinterDnD

import app.gui_classes as gui


def main():
    """GUI for app
    """
    root = TkinterDnD.Tk()

    root.geometry('800x800')

    root.minsize(width = 600,  height = 400)

    def _quit():
        root.quit()
        root.destroy()
        print("BDU fechado")

    root.protocol("WM_DELETE_WINDOW",  _quit)


    notebook = ttk.Notebook(root)
    # notebook.grid()
    notebook.grid_rowconfigure(1,  weight=1)
    notebook.grid_columnconfigure(1,  weight=1)

    load_pdf = gui.gui_pdf_load(notebook)

    load_pdf.set_size(width=root.winfo_screenmmwidth(), height=root.winfo_screenmmheight())


    pdf_settings = gui.gui_settings(notebook)


    #root.state('zoomed')

    notebook.grid(sticky = "nsew")

    notebook.add(load_pdf.ui, text="File choose")
    notebook.add(pdf_settings.ui,  text="Settings")

    notebook.grid_columnconfigure(0, weight=10)
    notebook.grid_columnconfigure(1, weight=10)
    notebook.grid_rowconfigure(0, weight=10)

    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)

    logo = tk.PhotoImage(file = "app/gui_assets/logo.png")

    root.iconphoto(False,  logo)

    root.title("app-GUI")

    root.style = ttk.Style()

    root.style.theme_use("clam")

    root.mainloop()


    root.quit()

if __name__ == "__main__":
    main()
