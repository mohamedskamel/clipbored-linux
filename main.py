import threading
import keyboard  # Using the keyboard library for hotkey functionality
from Gui.gui import ClipboardManagerGUI

def hotkey_listener():
    """Background thread for listening to hotkeys."""
    while True:  
        keyboard.wait("win+v")  # Blocking call
        print("Hotkey detectevd: Win+V")
        if app.get_status() == False:
                app.show_window()

def main():
    global app
    app = ClipboardManagerGUI()

    # Start the GUI event loop (must run in the main thread)
    app.mainloop()

if __name__ == "__main__":
    # Start hotkey listener in a separate thread
    threading.Thread(target=hotkey_listener, daemon=False).start()
    
    # Start main GUI application
    main()
