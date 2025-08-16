import os
import sys
import shutil
import json
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, ttk, messagebox

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

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

def get_organization_preview(folder_path):
    folder_path = Path(folder_path)
    file_count = 0
    for entry in os.scandir(folder_path):
        if entry.is_file() and entry.name != "organization_log.json":
            file_count += 1
    return file_count

def organize_directory(folder_path, log_file_path):
    folder_path = Path(folder_path)
    log_data = {}

    for entry in os.scandir(folder_path):
        if entry.is_file():
            file_path = Path(entry)
            if file_path.name == os.path.basename(log_file_path):
                continue

            original_path = str(file_path.parent.resolve())
            file_format = file_path.suffix.lower()

            if file_format in FILE_FORMATS:
                destination_dir = folder_path / FILE_FORMATS[file_format]
            else:
                destination_dir = folder_path / "OTHER-FILES"

            destination_dir.mkdir(exist_ok=True)
            destination_path = destination_dir / file_path.name
            shutil.move(str(file_path), str(destination_path))
            log_data[str(destination_path.resolve())] = original_path

    with open(log_file_path, 'w') as f:
        json.dump(log_data, f, indent=4)

def undo_organization(log_file_path):
    log_file_path = Path(log_file_path)
    if not log_file_path.exists():
        raise FileNotFoundError("Log file not found. Cannot undo.")

    with open(log_file_path, 'r') as f:
        log_data = json.load(f)

    for new_path_str, original_parent_str in log_data.items():
        new_path = Path(new_path_str)
        original_parent = Path(original_parent_str)
        if new_path.exists():
            shutil.move(str(new_path), str(original_parent / new_path.name))

    os.remove(log_file_path)

    # Clean up empty directories
    for directory in set(FILE_FORMATS.values()):
        try:
            os.rmdir(log_file_path.parent / directory)
        except OSError:
            pass # Directory not empty or doesn't exist
    try:
        os.rmdir(log_file_path.parent / "OTHER-FILES")
    except OSError:
        pass


class FileOrganizerApp:
    def __init__(self, master):
        self.master = master
        master.title("File Organizer")
        master.geometry("700x550")
        master.configure(bg="#2C3E50")

        # ... (icon and style setup)
        try:
            p1 = tk.PhotoImage(file=resource_path('folder.png'))
            master.iconphoto(False, p1)
        except tk.TclError:
            print("Could not find folder.png")

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

        self.title_label = ttk.Label(master, text="File Organizer", font=("Helvetica", 24, "bold"), foreground="#ECF0F1")
        self.title_label.pack(pady=20)

        self.control_frame = ttk.Frame(master, padding="20")
        self.control_frame.pack(expand=True)

        self.folder_label = ttk.Label(self.control_frame, text="Selected Folder:")
        self.folder_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.folder_path_entry = ttk.Entry(self.control_frame, textvariable=self.selected_folder, width=50, state="readonly")
        self.folder_path_entry.grid(row=0, column=1, padx=10, pady=10, sticky="we")

        self.open_button = ttk.Button(self.control_frame, text="Browse...", command=self.select_folder)
        self.open_button.grid(row=0, column=2, padx=10, pady=10)

        self.button_frame = ttk.Frame(self.control_frame)
        self.button_frame.grid(row=1, column=1, pady=20)

        self.execute_button = ttk.Button(self.button_frame, text="Organize", command=self.organize_folder_gui, state="disabled")
        self.execute_button.pack(side="left", padx=5)

        self.undo_button = ttk.Button(self.button_frame, text="Undo", command=self.undo_folder_gui, state="disabled")
        self.undo_button.pack(side="left", padx=5)

        self.status_label = ttk.Label(master, textvariable=self.status_text, padding="10", anchor="center")
        self.status_label.pack(side="bottom", fill="x")
        self.status_label.configure(background="#34495E", foreground="#ECF0F1")

    def select_folder(self):
        folder_path = filedialog.askdirectory(initialdir="/", title="Select Folder")
        if folder_path:
            self.selected_folder.set(folder_path)
            self.status_text.set(f"Selected folder: {folder_path}")
            self.execute_button.config(state="normal")

            log_file = Path(folder_path) / "organization_log.json"
            if log_file.exists():
                self.undo_button.config(state="normal")
            else:
                self.undo_button.config(state="disabled")

    def organize_folder_gui(self):
        folder_path = self.selected_folder.get()
        if not folder_path:
            messagebox.showerror("Error", "Please select a folder first.")
            return

        file_count = get_organization_preview(folder_path)
        if file_count == 0:
            messagebox.showinfo("Info", "No files to organize in this folder.")
            return

        confirm = messagebox.askyesno("Confirmation", f"{file_count} file(s) will be organized. Do you want to continue?")
        if not confirm:
            self.status_text.set("Organization cancelled.")
            return

        self.status_text.set("Organizing files...")
        self.master.update_idletasks()

        log_file = Path(folder_path) / "organization_log.json"

        try:
            organize_directory(folder_path, log_file)
            self.status_text.set("Organization complete!")
            messagebox.showinfo("Success", "Files organized successfully!")
            self.undo_button.config(state="normal")
        except Exception as e:
            self.status_text.set("An error occurred.")
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            self.execute_button.config(state="disabled")
            self.status_text.set("Select a folder to organize.")

    def undo_folder_gui(self):
        folder_path = self.selected_folder.get()
        if not folder_path:
            messagebox.showerror("Error", "Please select a folder to undo.")
            return

        log_file = Path(folder_path) / "organization_log.json"
        if not log_file.exists():
            messagebox.showerror("Error", "No organization log found in this folder. Cannot undo.")
            return

        confirm = messagebox.askyesno("Confirmation", "Are you sure you want to undo the last organization?")
        if not confirm:
            return

        self.status_text.set("Undoing organization...")
        self.master.update_idletasks()

        try:
            undo_organization(log_file)
            self.status_text.set("Undo complete!")
            messagebox.showinfo("Success", "Organization successfully undone.")
        except Exception as e:
            self.status_text.set("An error occurred during undo.")
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            self.undo_button.config(state="disabled")
            self.status_text.set("Select a folder to organize.")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileOrganizerApp(root)
    root.mainloop()
