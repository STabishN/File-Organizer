import os
import shutil
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, ttk, messagebox

DIRECTORIES = {
    "HTML": [".html5", ".html", ".htm", ".xhtml"],
    "IMAGES": [".jpeg", ".jpg", ".tiff", ".gif", ".bmp", ".png", ".bpg", "svg", ".heif", ".psd"],
    "VIDEOS": [".avi", ".flv", ".wmv", ".mov", ".mp4", ".webm", ".vob", ".mng", ".qt", ".mpg", ".mpeg", ".3gp"],
    "DOCUMENTS": [".oxps", ".epub", ".pages", ".docx", ".doc", ".fdf", ".ods", ".odt", ".pwi", ".xsn", ".xps", ".dotx", ".docm", ".dox", ".rvg", ".rtf", ".rtfd", ".wpd", ".xls", ".xlsx", ".ppt", "pptx"],
    "ARCHIVES": [".a", ".ar", ".cpio", ".iso", ".tar", ".gz", ".rz", ".7z", ".dmg", ".rar", ".xar", ".zip"],
    "AUDIO": [".aac", ".aa", ".aac", ".dvf", ".m4a", ".m4b", ".m4p", ".mp3", ".msv", "ogg", "oga", ".raw", ".vox", ".wav", ".wma"],
    "PLAINTEXT": [".txt", ".in", ".out"],
    "PDF": [".pdf"],
    "PYTHON": [".py"],
    "XML": [".xml"],
    "EXE": [".exe"],
    "SHELL": [".sh"]
}
FILE_FORMATS = {file_format: directory
                for directory, file_formats in DIRECTORIES.items()
                for file_format in file_formats}

def organize_directory(folder_path):
    """Organizes files in a directory based on their extension."""
    folder_path = Path(folder_path)
    # Create all necessary directories first
    for file_format in FILE_FORMATS:
        dir_path = folder_path / FILE_FORMATS[file_format]
        dir_path.mkdir(exist_ok=True)

    other_files_dir = folder_path / "OTHER-FILES"
    other_files_dir.mkdir(exist_ok=True)

    # Organize files
    for entry in os.scandir(folder_path):
        if entry.is_file():
            file_path = Path(entry)
            file_format = file_path.suffix.lower()
            if file_format in FILE_FORMATS:
                destination_dir = folder_path / FILE_FORMATS[file_format]
                shutil.move(str(file_path), str(destination_dir / file_path.name))
            else:
                # Move files that are not in the dictionary to OTHER-FILES
                shutil.move(str(file_path), str(other_files_dir / file_path.name))


class FileOrganizerApp:
    def __init__(self, master):
        self.master = master
        master.title("File Organizer")
        master.geometry("700x500")
        master.configure(bg="#2C3E50")

        # Set window icon
        try:
            p1 = tk.PhotoImage(file='folder.png')
            master.iconphoto(False, p1)
        except tk.TclError:
            print("Could not find folder.png")

        # Use a more modern theme
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TButton", foreground="white", background="#3498DB", font=("Helvetica", 12), padding=10)
        self.style.map("TButton", background=[("active", "#2980B9")])
        self.style.configure("TLabel", background="#2C3E50", foreground="white", font=("Helvetica", 12))
        self.style.configure("TFrame", background="#2C3E50")
        self.style.configure("TEntry", fieldbackground="#ECF0F1", font=("Helvetica", 12))


        self.selected_folder = tk.StringVar()
        self.status_text = tk.StringVar()
        self.status_text.set("Select a folder to organize.")

        # Main title
        self.title_label = ttk.Label(master, text="File Organizer", font=("Helvetica", 24, "bold"), foreground="#ECF0F1")
        self.title_label.pack(pady=20)

        # Frame for controls
        self.control_frame = ttk.Frame(master, padding="20")
        self.control_frame.pack(expand=True)

        # Label for selected folder
        self.folder_label = ttk.Label(self.control_frame, text="Selected Folder:")
        self.folder_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.folder_path_entry = ttk.Entry(self.control_frame, textvariable=self.selected_folder, width=50, state="readonly", font=("Helvetica", 12))
        self.folder_path_entry.grid(row=0, column=1, padx=10, pady=10, sticky="we")

        # Button to open folder
        self.open_button = ttk.Button(self.control_frame, text="Browse...", command=self.select_folder, style="TButton")
        self.open_button.grid(row=0, column=2, padx=10, pady=10)

        # Execute button
        self.execute_button = ttk.Button(self.control_frame, text="Organize Folder", command=self.organize_folder_gui, state="disabled", style="TButton")
        self.execute_button.grid(row=1, column=1, padx=10, pady=20)

        # Status label
        self.status_label = ttk.Label(master, textvariable=self.status_text, padding="10", font=("Helvetica", 10), anchor="center")
        self.status_label.pack(side="bottom", fill="x")
        self.status_label.configure(background="#34495E", foreground="#ECF0F1")

    def select_folder(self):
        folder_path = filedialog.askdirectory(initialdir="/", title="Select Folder")
        if folder_path:
            self.selected_folder.set(folder_path)
            self.status_text.set(f"Selected folder: {folder_path}")
            self.execute_button.config(state="normal")

    def organize_folder_gui(self):
        folder_path = self.selected_folder.get()
        if not folder_path:
            messagebox.showerror("Error", "Please select a folder first.")
            return

        self.status_text.set("Organizing files...")
        self.master.update_idletasks()

        try:
            organize_directory(folder_path)
            self.status_text.set("Organization complete!")
            messagebox.showinfo("Success", "Files organized successfully!")
        except Exception as e:
            self.status_text.set("An error occurred.")
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            self.execute_button.config(state="disabled")
            self.selected_folder.set("")
            self.status_text.set("Select a folder to organize.")


if __name__ == "__main__":
    root = tk.Tk()
    app = FileOrganizerApp(root)
    root.mainloop()
