<div align="center">

# ShrinkConvert

<p>
  A lightweight, open-source image compression and conversion REST API.
  <br>
  Compress, convert, and resize images with a single self-hosted service.
</p>

<p>
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-REST_API-009688?style=flat-square&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/License-MIT-black?style=flat-square" alt="License">
</p>

</div>

---

## Overview

ShrinkConvert is a simple, self-hosted REST API that combines image compression, format conversion, and resizing into a single service.

Images are processed locally in memory and returned directly to the client.

No external APIs, cloud services, or databases are required.

## Features

- Image compression with adjustable quality
- Image conversion between popular formats
- JPEG, PNG, WebP, BMP, and TIFF support
- Automatic input format detection
- Combined compression and conversion
- Optional image resizing
- WebP lossless compression
- Automatic EXIF orientation correction
- Maximum upload size of 20 MiB
- Interactive API documentation
- Fully self-hosted

## Installation

**1. Clone the repository**

```bash
git clone https://github.com/louizmac/ShrinkConvert.git
cd ShrinkConvert
```

**2. Create a virtual environment**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Start the server**

```bash
python3 -m uvicorn main:app --host 127.0.0.1 --port 8000
```

The API will be available at:

`http://127.0.0.1:8000`

Interactive documentation:

`http://127.0.0.1:8000/docs`

## API Reference

### Compress Image

`POST /api/v1/compress`

Compress an image while keeping its original format.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| file | File | Required | Image to compress |
| quality | Integer | 80 | Quality between 1 and 100 |

**Example Request**

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/compress?quality=80" \
  -F "file=@image.jpg" \
  --output compressed.jpg
```

### Convert Image

`POST /api/v1/convert`

Convert an image to a selected output format.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| file | File | Required | Image to convert |
| output_format | String | png | Target image format |

**Example Request**

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/convert?output_format=png" \
  -F "file=@image.webp" \
  --output converted.png
```

### Process Image

`POST /api/v1/process`

Compress, convert, and optionally resize an image in a single request.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| file | File | Required | Image to process |
| output_format | String | original | Target format |
| quality | Integer | 80 | Compression quality |
| max_width | Integer | None | Maximum image width |
| max_height | Integer | None | Maximum image height |
| lossless | Boolean | false | Enable lossless WebP encoding |

**Example Request**

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/process?output_format=webp&quality=80&max_width=1920" \
  -F "file=@image.png" \
  --output processed.webp
```

## Python Example

Install the requests library:

```bash
pip install requests
```

```python
import requests

url = "http://127.0.0.1:8000/api/v1/process"

with open("image.png", "rb") as image:
    response = requests.post(
        url,
        files={"file": image},
        params={
            "output_format": "webp",
            "quality": 80,
            "max_width": 1920
        }
    )

response.raise_for_status()

with open("processed.webp", "wb") as output:
    output.write(response.content)

print("Image processed successfully!")
```

## Supported Formats

| Format | Input | Output |
|--------|-------|--------|
| JPEG | Yes | Yes |
| PNG | Yes | Yes |
| WebP | Yes | Yes |
| BMP | Yes | Yes |
| TIFF | Yes | Yes |

JPG and JPEG refer to the same image format.

## Project Structure

```text
ShrinkConvert/
├── main.py
├── core/
│   ├── __init__.py
│   ├── compression.py
│   ├── conversion.py
│   └── processing.py
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

## Notes

- Compression results depend on the original image.
- Output files may be larger than the originals.
- PNG optimization is lossless.
- The quality parameter does not affect all formats.
- Transparency may be lost when converting to JPEG or BMP.
- Animated images and multi-page TIFF files are not supported.
- Additional security measures are recommended before public deployment.

## License

Distributed under the MIT License. See `LICENSE` for details.

---

<div align="center">

  <sub>Built with Python, FastAPI and Pillow.</sub>
  <br>
  <sub>Created by <a href="https://github.com/louizmac">louizmac</a></sub>

</div>
