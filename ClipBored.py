import time
import sqlite3
import pyperclip
import tkinter as tk
import keyboard  # Using the keyboard library for hotkey functionality
from tkinter import ttk
from systemd.daemon import notify

db_file = "clipboard_history.db"

def init_db():
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS clipboard (id INTEGER PRIMARY KEY, content TEXT UNIQUE, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

def save_clipboard(content):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO clipboard (content) VALUES (?)", (content,))
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # Ignore duplicates
    conn.close()

def get_clipboard_history():
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute("SELECT content FROM clipboard ORDER BY timestamp DESC LIMIT 10")
    rows = c.fetchall()
    conn.close()
    return rows

def monitor_clipboard():
    last_clipboard = ""
    notify('READY=1')  # Notify systemd that the service is ready
    while True:
        clipboard_content = pyperclip.paste()
        if clipboard_content and clipboard_content != last_clipboard:
            save_clipboard(clipboard_content)
            last_clipboard = clipboard_content
        time.sleep(1)

def show_clipboard_history():
    def on_select(event):
        selected_item = history_listbox.selection()
        if selected_item:
            content = history_listbox.item(selected_item, "values")[0]
            pyperclip.copy(content)  # Copy the selected content to clipboard
            keyboard.press_and_release('ctrl+v')  # Simulate Ctrl + V to paste the content where the cursor is
            history_window.destroy()  # Close the history window after pasting

    history_window = tk.Tk()
    history_window.title("Clipboard History")
    
    # Configure the treeview
    history_listbox = ttk.Treeview(history_window, columns=("Content"), show="headings")
    history_listbox.heading("Content", text="Content")
    history_listbox.column("Content", width=400, anchor='w')

    # Insert data into the treeview
    for row in get_clipboard_history():
        history_listbox.insert("", "end", values=row)

    history_listbox.bind("<Double-1>", on_select)

    # Make the treeview scalable
    history_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Configure resizing behavior
    history_window.grid_rowconfigure(0, weight=1)
    history_window.grid_columnconfigure(0, weight=1)

    # Set a minimum size for the window
    history_window.minsize(400, 300)

    history_window.mainloop()

def on_hotkey():
    show_clipboard_history()

def main():
    init_db()
    
    # Register the hotkey Win + V
    keyboard.add_hotkey('win+v', on_hotkey)
    print("Listening for hotkey Win + V...")
    
    # Start the clipboard monitoring in the main thread
    monitor_clipboard()

if __name__ == "__main__":
    main()
