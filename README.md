# clipbored-linux

ClipBored is a Linux clipboard manager that functions similarly to Windows' built-in clipboard history (Win + V). It stores copied text and allows easy retrieval using a hotkey.

## Features
- Monitors clipboard history and stores unique entries.
- Displays a GUI window to browse clipboard history.
- Allows selecting and pasting clipboard content where the cursor is located.
- Runs as a background daemon with systemd support.

## Requirements
Ensure you have the following dependencies installed:

```sh
pip install pyperclip keyboard tkinter systemd
```

## Installation
Clone the repository and navigate to the project folder:

```sh
git clone https://github.com/yourusername/ClipboardManager.git
cd ClipboardManager
```

## Usage
Run the script manually:

```sh
python3 ClipBored.py
```

Press `Win + V` to open the clipboard history window, then double-click an entry to paste it where your cursor is located.

## Running as a Systemd Service
To run the clipboard manager automatically at startup, create a systemd service file:

```sh
sudo nano /etc/systemd/system/clipboard.service
```

Add the following content:

```
[Unit]
Description=Clipboard Manager
After=network.target

[Service]
ExecStart=/usr/bin/python3 /path/to/ClipBored.py
Restart=always
User=yourusername

[Install]
WantedBy=default.target
```

Enable and start the service:

```sh
sudo systemctl enable clipboard
sudo systemctl start clipboard
```

## License
This project is open-source and available under the MIT License.

## Contributing
Feel free to submit issues or pull requests to improve the project!

