import tkinter as tk
from abc import ABC, abstractmethod



class View(ABC):
    container = None

    def __init__(self, container):
        self.container = container

    @abstractmethod
    def setup(self):
        pass

    @abstractmethod
    def layout(self):
        pass

class FileSelection(View):

    btn_open_file = None
    lbl_instruction = None
    frm_self = None
    container = None
    open_file = None

    def __init__(self, container, open_file):
        super().__init__(container)
        self.open_file = open_file
        self.setup()
        self.layout()

    def setup(self):
        self.frm_self = tk.Frame(self.container)
        self.lbl_instruction = tk.Label(self.frm_self)
        self.btn_open_file = tk.Button(self.frm_self, command = self.open_file)

    def layout(self):
        self.frm_self.columnconfigure(0, minsize = 100, weight = 1)
        self.frm_self.rowconfigure(1, minsize = 60, weight = 1)

        self.lbl_instruction["text"] = """
        Please load a grayscale .bmp image (color images will be converted)"""
        self.btn_open_file["text"] = "Open..."
        self.lbl_instruction.grid(row = 0, column = 0, sticky = "ew")
        self.btn_open_file.grid(row = 1, column = 0, sticky = "ew")

    def place(self, **kwargs):
        self.frm_self.grid(kwargs)

    def destroy(self):
        self.frm_self.destroy()



# class
