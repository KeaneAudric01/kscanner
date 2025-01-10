# kscanner 🚀

kscanner is a fast and efficient port scanner written in Python. It features multi-threading, progress tracking, and customizable port ranges for comprehensive network diagnostics.

## Disclaimer ⚠️

The `.exe` file attached on the [release page](https://github.com/KeaneAudric01/kscanner/releases) might trigger a false positive virus detection (tested with Windows Defender). Please be assured that the file is safe to use.

## Features ✨

- Scan a specified IP address for open ports
- Multi-threaded scanning for faster results
- Progress tracking with a visual progress bar
- Customizable port ranges
- Display of open ports and their associated services

## Usage 📋

```sh
Usage: kscanner.py

Follow the prompts to enter the IP address and port range options.
```

### Example Commands

- Scan ports on a specified IP address:
    ```sh
    python kscanner.py
    ```

## Installation 🛠️

### Prerequisites

- Python 3.x

## Running the Script Directly with Python 🐍

To use the script directly with Python without creating an executable, follow these steps:

1. Ensure you have Python 3.x installed on your machine.

2. Navigate to the directory containing `kscanner.py`:

    ```sh
    cd /path/to/kscanner
    ```

3. Run the script using Python:

    ```sh
    python kscanner.py
    ```

## Building the Executable 🏗️

To build your own executable file from the source code, follow these steps:

1. Install `pyinstaller`:

    ```sh
    pip install pyinstaller
    ```

2. Navigate to the directory containing `kscanner.py`:

    ```sh
    cd /path/to/kscanner
    ```

3. Run `pyinstaller` to create the executable:

    ```sh
    pyinstaller --onefile kscanner.spec
    ```

4. The executable file will be created in the `dist` directory.

## License 📄

This project is licensed under the MIT License. See the [LICENSE](https://github.com/KeaneAudric01/kscanner/blob/main/LICENSE) file for details.

## Author 👤

Keane Audric

GitHub: [KeaneAudric01](https://github.com/KeaneAudric01)
