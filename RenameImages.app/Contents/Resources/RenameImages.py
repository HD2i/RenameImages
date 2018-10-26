import glob, os
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter.messagebox import showinfo
from subprocess import call
from PIL import ImageTk, Image

def browse_button(*args):
    # Allow user to select a directory and store it in global var
    # called folder_path
    global folder_path
    filename = filedialog.askdirectory()
    folder_path.set(filename)


def rename(start_index, dir, file_type, new_name, separator_type):
    if os.path.isdir(dir):
        if new_name == "" or new_name == " ":
            showinfo("Invalid File Name", "Please enter a valid file name.")
        else:
            num_images = 0
            for eachfile in os.listdir(dir):
                if eachfile.endswith(default_imagetype.get()):
                    num_images += 1
            if num_images == 0:
                showinfo("Number of Images", "There are no " + default_imagetype.get() + " images in this folder. "
                         "Please make sure you have the right folder.")
            else:
                i = int(start_index)
                if separator_type != "None":
                    new_name = new_name + separator_type + "%s"
                else:
                    new_name = new_name + "%s"

                for pathAndFilename in sorted(glob.iglob(os.path.join(dir, file_type))):
                    title, ext = os.path.splitext(os.path.basename(pathAndFilename))
                    os.rename(pathAndFilename, os.path.join(dir, new_name % str(i) + default_imagetype.get()))
                    i += 1
                call(["open", dir])
    else:
        showinfo("Directory Not Valid!", "Please enter a valid directory")


def update_label(*args):
    if default_separator.get() == "None":
        previewText.set(fileName.get() + default_startingIndex.get() + default_imagetype.get())
    else:
        previewText.set(fileName.get() + default_separator.get() + default_startingIndex.get()
                        + default_imagetype.get())
    preview.config(text=previewText.get())


root = Tk()
root.title("Rename Images")

folder_path = StringVar()
fileName = StringVar()
previewText = StringVar()

separator_options = ["None", "-", "_"]
default_separator = StringVar()
default_separator.set(separator_options[0])

startingIndex_options = [0, 1]
default_startingIndex = StringVar()
default_startingIndex.set(startingIndex_options[0])

imagetype_options = [".png", ".jpg"]
default_imagetype = StringVar()
default_imagetype.set(imagetype_options[0])

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

## Row 1
ttk.Label(mainframe, text="Folder Location:").grid(column=1, row=1, sticky=E)
location_entry = ttk.Entry(mainframe, width=30, textvariable=folder_path)
location_entry.grid(column=2, row=1, sticky=(W, E))
ttk.Button(mainframe, text="Browse", command=lambda: browse_button()).grid(column=3, row=1, sticky=E)

## Row 2
ttk.Label(mainframe, text="Change File Names to:").grid(column=1, row=2, sticky=E)

fileName_entry = ttk.Entry(mainframe, width=30, textvariable=fileName)
fileName_entry.grid(column=2, row=2, sticky=(W, E), columnspan=2)

## Row 3
ttk.Label(mainframe, text="Separator:").grid(column=1, row=3, sticky=E)
separator = OptionMenu(mainframe, default_separator, *separator_options)
default_separator.set(default_separator.get())
separator.grid(column=2, row=3, sticky=W)

## Row 4
ttk.Label(mainframe, text="Starting Index:").grid(column=1, row=4, sticky=E)
startIndex = OptionMenu(mainframe, default_startingIndex, *startingIndex_options)
startIndex.grid(column=2, row=4, sticky=W)

## Row 5
ttk.Label(mainframe, text="Image Type:").grid(column=1, row=5, sticky=E)
imageOptions = OptionMenu(mainframe, default_imagetype, *imagetype_options)
imageOptions.grid(column=2, row=5, sticky=W)

## Row 6
ttk.Label(mainframe, text="Preview:").grid(column=1, row=6, sticky=E)
preview = ttk.Label(mainframe, text="")
preview.grid(column=2, row=6, sticky=W)

button = ttk.Button(mainframe, text="Rename",
                    command=lambda: rename(str(default_startingIndex.get()),
                                           str(folder_path.get()),
                                           "*" + default_imagetype.get(),
                                           str(fileName.get()),
                                           str(default_separator.get()))) \
    .grid(column=3, row=6, sticky=E)


## Row 7
ttk.Label(mainframe, text="Made with ❤️ by: HD2i.org").grid(column = 2, row = 7, sticky = S)

# hd2ipath = "a.png"
#mountsinaipath = "mountsinai.gif"
#hd2i = PIL.ImageTk.PhotoImage(PIL.Image.open(hd2ipath))
#mountsinai = PIL.ImageTk.PhotoImage(file = mountsinaipath)
#ttk.Label(mainframe, width=10, image = hd2i).grid(column = 2, row = 8, sticky = (S, E))
#ttk.Label(mainframe, width=10, image = mountsinai).grid(column = 2, row = 8, sticky = (S, W))


fileName.trace("w", update_label)
default_separator.trace("w", update_label)
default_startingIndex.trace("w", update_label)
default_imagetype.trace("w", update_label)

for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

location_entry.focus()
root.bind('<Rename>')

root.mainloop()
