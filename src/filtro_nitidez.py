from PIL import ImageFilter

def apply(image):
    """Aumenta a nitidez da imagem."""
    return image.filter(ImageFilter.SHARPEN)