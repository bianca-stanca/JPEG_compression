import tkinter as tk
from abc import ABC, abstractmethod
from PIL.ImageTk import PhotoImage
from PIL import Image


class View(ABC):
    container = None
    frm_self = None

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



class ParameterInput(View):

    lbl_block_dimension = None
    ent_block_dimension = None

    lbl_frequence_cutoff = None
    ent_frequence_cutoff = None

    image_dimensions = None

    btn_submit = None
    submit = None

    lbl_error = None


    def __init__(self, container, submit, image_dimensions):
        super().__init__(container)
        self.submit = submit
        self.image_dimensions = image_dimensions
        self.setup()
        self.layout()

    def setup(self):

        self.frm_self = tk.Frame(self.container)

        self.lbl_block_dimension = tk.Label(self.frm_self)
        self.ent_block_dimension = tk.Entry(self.frm_self)

        self.lbl_frequence_cutoff = tk.Label(self.frm_self)
        self.ent_frequence_cutoff = tk.Entry(self.frm_self)

        self.lbl_error = tk.Label(self.frm_self)

        self.btn_submit = tk.Button(self.frm_self, command = self.submit)

        self.ent_block_dimension.bind("<KeyRelease>", self.on_block_dimension_entry_change) #keyup
        self.ent_frequence_cutoff.bind("<KeyRelease>", self.on_frequence_cutoff_entry_change) #keyup

    def layout(self):
        self.frm_self.columnconfigure(0, minsize = 100, weight = 1)
        self.frm_self.columnconfigure(1, minsize = 100, weight = 1)
        self.frm_self.rowconfigure([0, 1, 2], minsize = 50, weight = 1)

        self.lbl_block_dimension["text"] = """Choose a block dimension greater
        than 0, lesser than """
        self.lbl_block_dimension["text"] = self.lbl_block_dimension["text"] + str(min(self.image_dimensions))

        self.ent_block_dimension.insert(0, "0")


        self.lbl_frequence_cutoff["text"] = """Choose a frequency cutoff point"""
        self.ent_frequence_cutoff.insert(0, "0")

        self.btn_submit["text"] = "Submit"

        #disable submit button until valid input is provided
        self.btn_submit.config(state = tk.DISABLED)

        #disable frequency cutoff input until valid block dimension is provided
        self.ent_frequence_cutoff.config(state = tk.DISABLED)

        self.lbl_block_dimension.grid(row = 0, column = 0, sticky = "ew")
        self.ent_block_dimension.grid(row = 0, column = 1, sticky = "ew")


        self.lbl_frequence_cutoff.grid(row = 1, column = 0, sticky = "ew")
        self.ent_frequence_cutoff.grid(row = 1, column = 1, sticky = "ew")

        self.btn_submit.grid(row = 2, column = 1, sticky = "e")

        self.lbl_error.grid(row=2, column=0, sticky = "w")
        self.lbl_error.grid_remove()


        self.lbl_error["fg"] = "red"

    def place(self, **kwargs):
        self.frm_self.grid(kwargs)

    def get_parameters(self):
        block_dimension_string = self.ent_block_dimension.get()
        frequence_cutoff_string = self.ent_frequence_cutoff.get()
        parameters = {}
        parameters["block_size"] = int(block_dimension_string)
        parameters["frequence_cutoff"] = int(frequence_cutoff_string)
        return parameters


    def on_block_dimension_entry_change(self, event):
        block_dimension_string = self.ent_block_dimension.get()

        try:

            block_dimension = int(block_dimension_string)

            #Remove previous limits to frequence cutoff
            self.lbl_frequence_cutoff["text"] = """Choose a frequency cutoff point"""

            #Remove any eventual previous error messages
            self.lbl_error.grid_remove()
            self.ent_frequence_cutoff.config(state = tk.NORMAL)

            if block_dimension < 1 or block_dimension > min(self.image_dimensions):
                raise Exception()

            self.max_cutoff = 2*block_dimension - 2
            self.lbl_frequence_cutoff["text"] = self.lbl_frequence_cutoff["text"] + "\n between 0 and " + str(self.max_cutoff)
            self.check_frequence_cutoff_validity()
        except:
            #show error message, disable frequency cutoff and submit button
            self.lbl_error.grid()
            self.ent_frequence_cutoff.config(state = tk.DISABLED)
            self.btn_submit.config(state = tk.DISABLED)
            self.lbl_error["text"] = "Please enter a valid block dimension"
            self.lbl_frequence_cutoff["text"] = "Choose a frequency cutoff point"

    def on_frequence_cutoff_entry_change(self, event):
        self.check_frequence_cutoff_validity()

    def destroy(self):
        self.frm_self.destroy()

    def check_frequence_cutoff_validity(self):
        frequence_cutoff_string = self.ent_frequence_cutoff.get()
        try:
            if len(frequence_cutoff_string) == 0:
                raise Exception()

            frequence_cutoff = int(frequence_cutoff_string)

            if frequence_cutoff < 0 or frequence_cutoff > self.max_cutoff:
                raise Exception()

            #Remove any residual messages
            self.lbl_error.grid_remove()
            self.btn_submit.config(state = tk.NORMAL)

        except:
            #show error message, disable frequency cutoff and submit button
            self.lbl_error.grid()
            self.lbl_error["text"] = "Please enter a valid frequency cutoff"
            self.btn_submit.config(state = tk.DISABLED)

class Comparison(View):
    resized_original = None
    resized_compressed = None

    original = None
    compressed = None
    lbl_original = None
    lbl_compressed = None
    def __init__(self, container, original, compressed):
        super().__init__(container)

        self.original = Image.fromarray(original)
        self.compressed = Image.fromarray(compressed)
        self.setup()
        self.layout()

    def setup(self):
        self.frm_self = tk.Frame(self.container)
        self.lbl_original = tk.Label(self.frm_self)
        self.lbl_compressed = tk.Label(self.frm_self)

    def layout(self):
        width, height = self.original.size


        #figure out initial scale of images
        scale = 500/max((height, width))


        #resize image to fit scaled down aspect
        resized_compressed = self.compressed.resize(size =(int(width*scale), int(height*scale)))
        resized_original = self.original.resize(size =(int(width*scale), int(height*scale)))


        #keep reference to resized picture in order to be able to display it
        self.resized_compressed = PhotoImage(image = resized_compressed)
        self.resized_original = PhotoImage(image = resized_original)


        #set minsize so it fits images scaled down to 500px along max dimension
        self.frm_self.columnconfigure([0,1], minsize = (width*scale), weight = 1)
        self.frm_self.rowconfigure(0, minsize = (height*scale), weight = 1)

        self.lbl_original["image"] = self.resized_original

        self.lbl_original.grid(row = 0, column = 0, sticky = "nsew")
        self.lbl_original.config(width = (width*scale), height = (height*scale))

        self.lbl_compressed["image"] = self.resized_compressed
        self.lbl_compressed.grid(row = 0, column = 1, sticky = "ew")
        self.lbl_compressed.config(width = (width*scale), height = (height*scale))
        # self.lbl_compressed.bind("<Configure>", self.resize)




    # def resize(self, event):
    #     # import ipdb; ipdb.set_trace()
    #     width, height = self.original.size
    #
    #
    #     #figure out initial scale of images
    #     scale = max(event.height, event.width)/max((height, width))
    #     self.lbl_original.config(width = (width*scale), height = (height*scale))
    #     original_resized = self.original.resize((int(width*scale), int(height*scale)))
    #     self.resized_original= PhotoImage(original_resized)
    #     self.lbl_original["image"] = self.resized_original
    #


        ###NEEDS TO BE MOVED TO PARENT CLASS
    def place(self, **kwargs):
        self.frm_self.grid(kwargs)
