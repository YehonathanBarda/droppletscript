import os
import tkinter as tk
from tkinter import filedialog, messagebox
from dropplet_functions import calculate_contact_angle
from PIL import Image
import subprocess

class DropletApp:
    """
    A GUI application for calculating the contact angle of droplets in images.
    Attributes:
        root (tk.Tk): The root window of the Tkinter application.
        image_files (list): List of selected image file paths.
        log_file_name (tk.StringVar): The name of the log file where results will be stored.
        log_directory (tk.StringVar): The directory where the log file will be saved.
        image_label (tk.Label): Label to display selected image file names.
        directory_label (tk.Label): Label to display the selected log directory.
        open_log_button (tk.Button): Button to open the log file after processing.
    Methods:
        create_widgets(): Creates and places the widgets in the application window.
        load_images(): Opens a file dialog to select image files and updates the image label.
        choose_directory(): Opens a directory dialog to select the log directory and updates the directory label.
        run(): Processes the selected images to calculate contact angles and logs the results.
        open_log_file(): Opens the log file in Notepad.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Droplet Contact Angle Calculation")

        # Set the window icon
        icon_path = os.path.join(os.path.dirname(__file__), 'icon' ,'dropplet_icon.ico')
        self.root.iconbitmap(icon_path)

        self.image_files = []
        self.log_file_name = tk.StringVar(value="results.log")
        self.log_directory = tk.StringVar(value=os.getcwd())

        self.create_widgets()

    def create_widgets(self):
        # Create and place widgets in the application window
        tk.Label(self.root, text="Select Images:").grid(row=0, column=0, padx=10, pady=10)
        tk.Button(self.root, text="Browse", command=self.load_images).grid(row=0, column=1, padx=10, pady=10)
        self.image_label = tk.Label(self.root, text="")
        self.image_label.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        tk.Label(self.root, text="Log File Name:").grid(row=2, column=0, padx=10, pady=10)
        tk.Entry(self.root, textvariable=self.log_file_name).grid(row=2, column=1, padx=10, pady=10)

        tk.Label(self.root, text="Log File Directory:").grid(row=3, column=0, padx=10, pady=10)
        tk.Button(self.root, text="Browse", command=self.choose_directory).grid(row=3, column=1, padx=10, pady=10)
        self.directory_label = tk.Label(self.root, text=self.log_directory.get())
        self.directory_label.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        tk.Button(self.root, text="Run", command=self.run).grid(row=5, column=0, columnspan=2, padx=10, pady=10)
        self.open_log_button = tk.Button(self.root, text="Open Log File", command=self.open_log_file, state=tk.DISABLED)
        self.open_log_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

    def load_images(self):
        # Open a file dialog to select image files and update the image label
        files = filedialog.askopenfilenames(filetypes=[("Image files", "*.jpeg;*.jpg")])
        if files:
            self.image_files = files
            self.image_label.config(text="\n".join(os.path.basename(file) for file in files))
            messagebox.showinfo("Selected Images", f"{len(files)} images selected")

    def choose_directory(self):
        # Open a directory dialog to select the log directory and update the directory label
        directory = filedialog.askdirectory()
        if (directory):
            self.log_directory.set(directory)
            self.directory_label.config(text=self.log_directory.get())

    def run(self):
        # Process the selected images to calculate contact angles and log the results
        if not self.image_files:
            messagebox.showwarning("No Images", "Please select images to process")
            return
        
        log_file_path = os.path.join(self.log_directory.get(), self.log_file_name.get())
        if not log_file_path.endswith('.log'):
            log_file_path += '.log'
            
        with open(log_file_path, 'w', encoding='utf-8') as log_file:
            for file_name in self.image_files:
                try:
                    # Try to open the image using PIL to check if the file is valid
                    with Image.open(file_name) as img:
                        img.verify()  # Verify that it is an image
                except (IOError, SyntaxError) as e:
                    log_file.write(f"Error: Image not found or invalid format. Path: {file_name}\n")
                    messagebox.showerror("Error", f"Image not found or invalid format. Path: {file_name}")
                    continue

                contact_angle = calculate_contact_angle(file_name)
                log_file.write(f"File: {os.path.basename(file_name)} | Contact Angle: {contact_angle} degrees\n")

        messagebox.showinfo("Completed", f"Results stored in {log_file_path}")
        self.open_log_button.config(state=tk.NORMAL)

    def open_log_file(self):
        # Open the log file in Notepad
        log_file_path = os.path.join(self.log_directory.get(), self.log_file_name.get())
        if os.path.isfile(log_file_path):
            subprocess.Popen(['notepad.exe', log_file_path])

if __name__ == "__main__":
    root = tk.Tk()
    app = DropletApp(root)
    root.mainloop()