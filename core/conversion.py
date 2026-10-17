from core.processing import process_image

def convert_image(original, output_format="png"):
    return process_image(
        original,
        output_format=output_format,
        quality=95
    )