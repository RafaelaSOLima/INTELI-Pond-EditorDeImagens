from PIL import ImageFilter

def apply(image):
    """Aplica efeito embaçado usando GaussianBlur."""
    return image.filter(ImageFilter.GaussianBlur(radius=2))