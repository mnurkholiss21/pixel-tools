# PixelTools

A small desktop app for turning regular images into pixel art.

## Features

- Live preview while changing pixel size
- Original, grayscale, vivid, Game Boy, and limited-color modes
- Supports PNG, JPG, JPEG, BMP, and WEBP input
- Keeps the original image unchanged
- Corrects common photo orientation metadata
- Saves full-resolution results as PNG or JPEG
- Preserves transparent PNG output

## Requirements

- Python 3.9 or newer
- Pillow
- Tkinter (included with most standard Python installations)

## Installation

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Run

```bash
python pixelconverter.py
```

1. Click **Open image**.
2. Adjust **Pixel size** with the slider.
3. Choose a color mode.
4. Click **Save result**.

The preview is scaled for the window, but the saved image keeps its original resolution.

## Project structure

```text
PixelConverter/
|-- pixelconverter.py
|-- requirements.txt
|-- README.md
|-- LICENSE
`-- .gitignore
```

## License

Copyright (c) 2026 Ajie Kurniawan.

This project is available under the MIT License. See [LICENSE](LICENSE).
The MIT License allows others to use, modify, and distribute the project while
requiring the original copyright and license notice to remain included.

The project name **PixelTools** and its logo, if one is added later, are not
automatically protected as a trademark by this software license. Consider a
separate trademark registration if the name becomes an important product or
brand.
