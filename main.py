import threading
import keyboard  # Using the keyboard library for hotkey functionality
from gui import ClipboardManagerGUI
from clipboard_history_sql import DatabaseManager
import pyperclip
import time

def gui_open():
    if app.get_status() == False:
        app.show_window()
        records = history_database.fetch_all("clipbored_history")
        # Print the retrieved records
        for record in records:
            app.add_data(record)

def monitor_clipboard():
    last_clipboard = ""
    while True:
        clipboard_content = pyperclip.paste()
        if clipboard_content and clipboard_content != last_clipboard:
            history_database.insert("clipbored_history",clipboard_content)
            last_clipboard = clipboard_content
        time.sleep(1)

def main():
    global app
    app = ClipboardManagerGUI()

    # Start the GUI event loop (must run in the main thread)
    app.mainloop()

if __name__ == "__main__":
    # run xhost +SI:localuser:root before run the script

    global history_database

    history_database = DatabaseManager("clipbored_history.db")

    # Create a table for clipboard history
    history_database.create_table("clipbored_history")

    # Clear all records from the clipboard table
    history_database.clear_table("clipbored_history")

    # Start hotkey listener in a separate thread
    threading.Thread(target=monitor_clipboard, daemon=False).start()

    """Background thread for listening to hotkeys."""
    keyboard.add_hotkey("win+alt", gui_open) 

    # Start main GUI application
    main()
