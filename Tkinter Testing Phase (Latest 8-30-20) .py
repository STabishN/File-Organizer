import os
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, Text


# Root is equivalent to HTML body
root = tk.Tk()
root.title("Junk Organizer")

# Creating object of photoimage class 
# Image should be in the same folder 
# in which script is saved 
p1 = tk.PhotoImage(file = 'folder.png') 
# Setting icon of master window 
root.iconphoto(False, p1) 

# Selecting directory
def addApp():
   addApp.filename = filedialog.askdirectory(initial="/", title="Select Folder")
   print ("The current working directory is {}".format(addApp.filename))
   os.chdir(addApp.filename)

DIRECTORIES = {
   "HTML": [".html5", ".html", ".htm", ".xhtml"],
   "IMAGES": [".jpeg", ".jpg", ".tiff", ".gif", ".bmp", ".png", ".bpg", "svg",
   ".heif", ".psd"],
   "VIDEOS": [".avi", ".flv", ".wmv", ".mov", ".mp4", ".webm", ".vob", ".mng",
   ".qt", ".mpg", ".mpeg", ".3gp"],
   "DOCUMENTS": [".oxps", ".epub", ".pages", ".docx", ".doc", ".fdf", ".ods",
   ".odt", ".pwi", ".xsn", ".xps", ".dotx", ".docm", ".dox",
   ".rvg", ".rtf", ".rtfd", ".wpd", ".xls", ".xlsx", ".ppt",
   "pptx"],
   "ARCHIVES": [".a", ".ar", ".cpio", ".iso", ".tar", ".gz", ".rz", ".7z",
   ".dmg", ".rar", ".xar", ".zip"],
   "AUDIO": [".aac", ".aa", ".aac", ".dvf", ".m4a", ".m4b", ".m4p", ".mp3",
   ".msv", "ogg", "oga", ".raw", ".vox", ".wav", ".wma"],
   "PLAINTEXT": [".txt", ".in", ".out"],
   "PDF": [".pdf"],
   "PYTHON": [".py"],
   "XML": [".xml"],
   "EXE": [".exe"],
   "SHELL": [".sh"]
}


# Organizer
FILE_FORMATS = {file_format: directory
   for directory, file_formats in DIRECTORIES.items()
   for file_format in file_formats}

def organise_folder():
   print ("Folder Organizing in directory {}".format(addApp.filename))
   for entry in os.scandir():
      if entry.is_dir():
         continue
      file_path = Path(entry)
      file_format = file_path.suffix.lower()
      if file_format in FILE_FORMATS:
         directory_path = Path(FILE_FORMATS[file_format])
         directory_path.mkdir(exist_ok=True)
         file_path.rename(directory_path.joinpath(file_path))
   try:
      os.mkdir("OTHER-FILES")
   except:
      pass

   for dir in os.scandir():
      try:
         if dir.is_dir():
            os.rmdir(dir)
         else:
            os.rename(os.getcwd() + '/' + str(Path(dir)), os.getcwd() + '/OTHER-FILES/' + str(Path(dir)))
      except:
         pass


# Canvas
canvas = tk.Canvas(root, height=700,width=700,bg="#263D42")
# Attaching Canvas to root
canvas.pack()

frame = tk.Frame(root, bg="white")
frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

# Button Open directory
openFile = tk.Button(root, text="Open Folder", padx=10,
                     pady=5, fg="white", bg="#263D42", command = addApp)
openFile.pack()

# Button Execute Organizer
runApps = tk.Button(root, text="Execute Junk Organizer", padx=10,
                     pady=5, fg="white", bg="#263D42", command = lambda: organise_folder())
runApps.pack()

# This line executes and makes a GUI 
root.mainloop()


