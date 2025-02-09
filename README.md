```markdown
# Insta360 INSP File Recovery and Conversion

This Python script helps recover and convert Insta360 INSP (3D photo) files, which are in a proprietary format.  It's particularly useful if your SD card fails during transfer, leaving your INSP files incomplete or corrupted. This tool leverages a template INSP file to reconstruct the damaged files.  **Specifically, it addresses the common scenario where damaged INSP files are recovered as stereoscopic JPG images.**

## Table of Contents

*   [Introduction](#introduction)
*   [Requirements](#requirements)
*   [Features](#features)
*   [Usage](#usage)
    *   [Single File Conversion](#single-file-conversion)
    *   [Directory Conversion](#directory-conversion)
*   [Installation](#installation)
*   [Contributing](#contributing)
*   [License](#license)

## Introduction

This project addresses the frustrating issue of SD card failures interrupting the transfer of Insta360 INSP files.  These files, used for 3D photos, are crucial for post-processing.  Often, when recovery is attempted, these damaged INSP files are salvaged as stereoscopic JPG images, losing the crucial metadata that defines them as 3D photos. This script uses a known good "template" INSP file, likely one taken with the same camera settings, to help reconstruct the missing metadata and restore the files to their proper INSP format. It offers both single file and directory processing for maximum flexibility.

## Requirements

*   Python 3.x
*   pip

Dependencies listed in `requirements.txt`:

```
Pillow
tqdm
```

## Features

*   **INSP Metadata Recovery:** Fixes damaged INSP files recovered as stereoscopic JPGs by recreating the necessary metadata.
*   **Template-Based Reconstruction:** Uses a healthy INSP file as a template to reconstruct damaged data.
*   **Single File and Directory Processing:**  Process individual INSP files or entire directories of them.
*   **Command-Line Interface:**  Easy-to-use command-line interface accepts either a file or directory path as input.
*   **Improved Progress Reporting:**  Clear progress bar for single file processing using `tqdm`.
*   **Clearer Validation Messages:**  More informative error and validation messages.
*   **Robust Path Handling:** Prevents accidental overwriting of files by implementing checks and safeguards.

## Usage

### Single File Conversion

```bash
python insp_convert.py path/to/image.jpg output_directory/ path/to/template.insp -v
```

*   `path/to/image.jpg`: Path to the damaged INSP file (recovered as a stereoscopic JPG).
*   `output_directory/`: Path to the directory where the converted file will be saved.
*   `path/to/template.insp`: Path to the template INSP file.
*   `-v`: Verbose mode (optional).

### Directory Conversion

```bash
python insp_convert.py path/to/input_directory/ output_directory/ path/to/template.insp -v
```

*   `path/to/input_directory/`: Path to the directory containing the damaged INSP files (recovered as stereoscopic JPGs).
*   `output_directory/`: Path to the directory where the converted files will be saved.
*   `path/to/template.insp`: Path to the template INSP file.
*   `-v`: Verbose mode (optional).

## Installation

1.  **Clone the repository (optional):** If you are contributing or want to keep track of changes, clone the repository.

    ```bash
    git clone [https://github.com/your-username/insp_convert.git](https://www.google.com/search?q=https://github.com/your-username/insp_convert.git)  # Replace with your repo URL
    cd insp_convert
    ```

2.  **Install the requirements:**

    ```bash
    pip install -r requirements.txt
    ```

## Contributing

Contributions are welcome!  Please open an issue or submit a pull request.

## License

This project is licensed under the GNU General Public License v3.0.  See the [LICENSE](LICENSE) file for details.
```
