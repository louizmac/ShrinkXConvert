from io import BytesIO

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import Response
from PIL import Image, UnidentifiedImageError

from core.compression import compress_image
from core.conversion import convert_image
from core.processing import process_image

app = FastAPI(
    title="ShrinkXConvert",
    description="A self-hosted image compression and conversion REST API",
    version="1.0.0"
)

MAX_FILE_SIZE = 20 * 1024 * 1024
Image.MAX_IMAGE_PIXELS = 25_000_000

@app.get("/")
def home():
    return {
        "name": "ShrinkXConvert",
        "version": "1.0.0",
        "status": "online",
        "endpoints": [
            "/api/v1/compress",
            "/api/v1/convert",
            "/api/v1/process"
        ]
    }

async def read_image(file: UploadFile):
    data = await file.read(MAX_FILE_SIZE + 1)

    if len(data) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File too large"
        )

    if not data:
        raise HTTPException(
            status_code=400,
            detail="Empty file"
        )

    return data

def send_image(data, original, output_format):
    extension = "jpg" if output_format in ("jpg", "jpeg") else output_format

    media_types = {
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "png": "image/png",
        "webp": "image/webp",
        "bmp": "image/bmp",
        "tiff": "image/tiff"
    }

    saved_percent = round(
        (1 - len(data) / len(original)) * 100,
        2
    )

    return Response(
        content=data,
        media_type=media_types[output_format],
        headers={
            "Content-Disposition": (
                f'attachment; filename="output.{extension}"'
            ),
            "X-Original-Size": str(len(original)),
            "X-Output-Size": str(len(data)),
            "X-Saved-Percent": str(saved_percent)
        }
    )

def handle_error(error):
    if isinstance(error, HTTPException):
        raise error
    
    if isinstance(error, (ValueError, UnidentifiedImageError)):
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    if isinstance(error, (
        OSError,
        Image.DecompressionBombError,
        Image.DecompressionBombWarning
    )):
        raise HTTPException(
            status_code=400,
            detail="Unable to process image"
        )

    raise error

@app.post("/api/v1/compress")
async def compress(
    file: UploadFile = File(...),
    quality: int = 80
):
    original = await read_image(file)

    try:
        data, output_format = compress_image(original, quality)
        return send_image(data, original, output_format)

    except Exception as error:
        handle_error(error)

@app.post("/api/v1/convert")
async def convert(
    file: UploadFile = File(...),
    output_format: str = "png"
):
    original = await read_image(file)

    try:
        data, format_name = convert_image(original, output_format)
        return send_image(data, original, format_name)

    except Exception as error:
        handle_error(error)

@app.post("/api/v1/process")
async def process(
    file: UploadFile = File(...),
    output_format: str = "original",
    quality: int = 80,
    max_width: int | None = None,
    max_height: int | None = None,
    lossless: bool = False
):
    original = await read_image(file)

    try:
        data, format_name = process_image(
            original,
            output_format=output_format,
            quality=quality,
            max_width=max_width,
            max_height=max_height,
            lossless=lossless
        )

        return send_image(data, original, format_name)

    except Exception as error:
        handle_error(error)