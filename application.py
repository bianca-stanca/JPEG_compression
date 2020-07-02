import tkinter as tk
import pages
from tkinter.filedialog import askopenfilename
import matplotlib as plt
import cv2
from scipy import fftpack as fft
import numpy as np


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
            self.root_window.rowconfigure(i, weight = 1)
            self.root_window.columnconfigure(i, weight = 1)

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
        parameters = self.main_view.get_parameters()
        compressed_image = self.compress(parameters)

        self.show_comparison(compressed_image)


    def compress(self, parameters):
        block_size = parameters["block_size"]
        cutoff = parameters["frequence_cutoff"]
        row_blocks = self.image.shape[0] // block_size
        column_blocks = self.image.shape[1] // block_size

        compressed_image = np.zeros((row_blocks*block_size, column_blocks*block_size))
        #create index arrays
        x, y = np.mgrid[0:block_size, 0:block_size]
        #keep only the frequences where the indices sum to less than cutoff
        eliminated_frequencies = x + y >= cutoff


        for i in np.arange(start = 0, stop = row_blocks):
            row_start = i*block_size
            row_end = row_start + block_size
            for j in np.arange(start = 0, stop = column_blocks):
                column_start = j*block_size
                column_end = column_start + block_size
                #extract block
                f = self.image[row_start:row_end, column_start:column_end]
                c = fft.dctn(f, norm='ortho')

                # print("start i: "+str(i)+" end i: "+str(i+block_size))
                c[eliminated_frequencies] = 0
                #inverse cosine transform
                ff = fft.idctn(c, norm = 'ortho')

                rounded_ff = np.rint(ff).astype(np.int)

                #replace invalid values with valid ones
                rounded_ff[rounded_ff < 0] = 0
                rounded_ff[rounded_ff > 255] = 255
                compressed_image[row_start:row_end, column_start:column_end] = rounded_ff


        return compressed_image


    def show_comparison(self, compressed):
        self.main_view.destroy()
        self.main_view = pages.Comparison(self.root_window,
                        self.image, compressed)
        self.layout()
