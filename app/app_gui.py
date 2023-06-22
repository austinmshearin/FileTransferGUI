"""
Tkinter application for the file transfer GUI
"""
# Standard Imports
import tkinter as tk
import filetransfer_utils.file_transfer as file_transfer

# Local Imports


class FileTransferGUI:
    """
    The main Tkinter class to create the GUI
    """

    def __init__(self, window):
        # Main widget is the window
        self.window = window
        # Title of the window
        self.window.title("File Transfer")
        # Generate all widgets within the window
        self.create_widgets()

    def create_widgets(self):
        """
        Adds widgets to the window
        """
        pass


if __name__ == "__main__":
    root = tk.Tk()
    program = FileTransferGUI(root)
    root.mainloop()
