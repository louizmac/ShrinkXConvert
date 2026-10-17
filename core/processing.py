from io import BytesIO
import warnings

from PIL import Image, ImageOps

SUPPORTED_FORMATS = {
    "JPEG", "PNG", "WEBP", "BMP", "TIFF"
}

OUTPUT_FORMATS = {
    "jpg": "JPEG",
    "jpeg": "JPEG",
    "png": "PNG",
    "webp": "WEBP",
    "bmp": "BMP",
    "tiff": "TIFF"
}

MAX_DIMENSION = 10000

def process_image(
    original,
    output_format="original",
    quality=80,
    max_width=None,
    max_height=None,
    lossless=False
):
    if not 1 <= quality <= 100:
        raise ValueError("Quality must be between 1 and 100")

    if max_width is not None and not 1 <= max_width <= MAX_DIMENSION:
        raise ValueError("Invalid max_width")

    if max_height is not None and not 1 <= max_height <= MAX_DIMENSION:
        raise ValueError("Invalid max_height")

    output_format = output_format.lower()

    if output_format not in OUTPUT_FORMATS and output_format != "original":
        raise ValueError("Unsupported output format")

    with warnings.catch_warnings():
        warnings.simplefilter("error", Image.DecompressionBombWarning)

        with Image.open(BytesIO(original)) as image:
            if image.format not in SUPPORTED_FORMATS:
                raise ValueError("Unsupported input format")

            if getattr(image, "n_frames", 1) > 1:
                raise ValueError(
                    "Animated or multi-page images are not supported"
                )

            input_format = image.format

            image = ImageOps.exif_transpose(image)
            image.load()

    if output_format == "original":
        output_format = (
            "jpeg" if input_format == "JPEG"
            else input_format.lower()
        )

    if max_width is not None or max_height is not None:
        width = max_width if max_width is not None else image.width
        height = max_height if max_height is not None else image.height

        image.thumbnail(
            (width, height),
            Image.Resampling.LANCZOS
        )

    if output_format in ("jpg", "jpeg", "bmp"):
        if image.mode not in ("RGB", "L"):
            if "A" in image.getbands():
                background = Image.new("RGB", image.size, "white")
                background.paste(
                    image.convert("RGBA"),
                    mask=image.getchannel("A")
                )
                image = background
            else:
                image = image.convert("RGB")

    elif output_format in ("png", "webp", "tiff"):
        if image.mode not in ("RGB", "RGBA", "L", "LA"):
            image = image.convert("RGBA")

    output = BytesIO()
    save_options = {}

    if output_format in ("jpg", "jpeg"):
        save_options = {
            "quality": quality,
            "optimize": True
        }

    elif output_format == "webp":
        save_options = {
            "quality": quality,
            "lossless": lossless,
            "method": 6
        }

    elif output_format == "png":
        save_options = {
            "optimize": True
        }

    elif output_format == "tiff":
        save_options = {
            "compression": "tiff_deflate"
        }

    image.save(
        output,
        format=OUTPUT_FORMATS[output_format],
        **save_options
    )

    return output.getvalue(), output_format