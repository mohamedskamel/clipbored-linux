import tkinter as tk
from tkinter import ttk
import pyautogui
from pynput import mouse  

class ClipboardManagerGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Clipboard Manager")
        self.geometry("500x700")

        self.gui_status = False
        self.withdraw()  # Hide the window

        # Remove window frame (frameless)
        self.overrideredirect(True)

        # Initialize dragging variables
        self.x_offset = 0
        self.y_offset = 0

        self.setup_ui()
        self.make_window_draggable()

    def setup_ui(self):
        """Setup UI components"""
        ttk.Label(self, text="Clipboard").pack(pady=5)

        # Frame for Listbox & Scrollbar
        frame = ttk.Frame(self)
        frame.pack(expand=True, fill="both", padx=10, pady=5)

        # Listbox
        self.listbox = tk.Listbox(frame, selectmode=tk.SINGLE)
        self.listbox.pack(side="left", expand=True, fill="both")

        # Scrollbar
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.listbox.config(yscrollcommand=scrollbar.set)

    def make_window_draggable(self):
        """Allows dragging the frameless window"""
        self.bind("<ButtonPress-1>", self.start_move)
        self.bind("<B1-Motion>", self.on_move)

    def start_move(self, event):
        """Stores initial mouse position"""
        self.x_offset = event.x
        self.y_offset = event.y

    def on_move(self, event):
        """Moves the window"""
        x = self.winfo_pointerx() - self.x_offset
        y = self.winfo_pointery() - self.y_offset
        self.geometry(f"+{x}+{y}")

    def on_global_click(self, x, y, button, pressed):
        """Detects global clicks and closes if clicked outside the window"""
        if pressed:  # Only detect mouse down, not release
            x_root, y_root = self.winfo_rootx(), self.winfo_rooty()
            width, height = self.winfo_width(), self.winfo_height()

            # Check if the click is outside the window
            if not (x_root <= x <= x_root + width and y_root <= y <= y_root + height):
                self.hide_window()

    def add_data(self, data):
        self.listbox.insert(tk.END, data)

    def get_status(self):
        return self.gui_status

    def show_window(self):
        self.gui_status = True
        # Start global mouse listener
        self.mouse_listener = mouse.Listener(on_click=self.on_global_click)
        self.mouse_listener.start()  # Start global mouse listener
        # Position at cursor
        x, y = pyautogui.position()
        self.geometry(f"+{x}+{y}")
        self.deiconify()  # Show the window

    def hide_window(self):
        self.gui_status = False
        self.mouse_listener.stop()  # Stop global mouse listener
        self.withdraw()  # Hide the window

if __name__ == "__main__":
    app = ClipboardManagerGUI()
    app.mainloop()
