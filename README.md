# clipbored-linux

ClipBored is a Linux clipboard manager that functions similarly to Windows' built-in clipboard history (Win + alt). It stores copied text and allows easy retrieval using a hotkey.

## Features
- Monitors clipboard history and stores unique entries.
- Displays a GUI window to browse clipboard history.
- Allows selecting and pasting clipboard content where the cursor is located.
- Runs as a background daemon with systemd support. [still in progress]

## Requirements
Ensure you have the following dependencies installed:

```sh
pip install pyperclip keyboard tkinter sqlite3 pynput
```

## Installation
Clone the repository and navigate to the project folder:

```sh
git clone https://github.com/mohamedskamel/ClipboardManager.git
cd ClipboardManager
```

## Usage
Run the script manually:

```sh
xhost +SI:localuser:root
sudo python3 ClipBored.py
```

Press `Win + alt` to open the clipboard history window, then double-click an entry to paste it where your cursor is located.

## Known Limitations /!\

1- Xhost Requirement: This application must be run with the command xhost +SI:localuser:root to grant the necessary permissions for clipboard access.

2- Clipboard Hotkey Restrictions: The application cannot utilize the Win + V hotkey functionality. In Linux environments using Wayland, the suppression of key strokes by external processes is restricted, preventing the clipboard manager from functioning as expected with this key combination.

## License
This project is open-source and available under the MIT License.

## Contributing
Feel free to submit issues or pull requests to improve the project!

