import tkinter as tk
import pages
from tkinter.filedialog import askopenfilename
import matplotlib as plt
import cv2

class Application():

    root_window = None
    main_view = None
    image = None

####SETUP METHODS FOR FIRST VIEW OF APP####
    def __init__(self):
        self.root_window = tk.Tk()
        self.setup()
        self.layout()


    def setup(self):
        self.main_view = pages.FileSelection(self.root_window, self.open_file)

    def layout(self):
        self.root_window.title("JPEG compression")
        self.root_window.minsize(width = 500, height = 500)

        for i in range(3):
            self.root_window.rowconfigure(i, weight = 1, minsize = 100)
            self.root_window.columnconfigure(i, weight = 1, minsize = 100)

        self.main_view.place(column = 1, row = 1, sticky ="ew")


####BUTTON COMMAND FUNCTIONS AND NAVIGATION####
    def open_file(self):
        """Open a file for editing, and navigate to next page"""
        file_path = askopenfilename(filetypes=[("BMP Images", "*.bmp")])
        if not file_path:
            return
        self.image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
        self.navigate_to_input_view()

    def navigate_to_input_view(self):
        self.main_view.destroy();
        self.main_view = pages.ParameterInput(self.root_window,
                        self.submit, self.image.shape)
        self.layout()

    def submit(self):
        pass
