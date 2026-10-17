from core.processing import process_image

def compress_image(original, quality=80):
    return process_image(
        original,
        output_format="original",
        quality=quality
    )