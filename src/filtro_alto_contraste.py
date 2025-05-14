from PIL import ImageEnhance

def apply(image):
    """Aumenta o contraste da imagem."""
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(2.0)  # fator 2.0 aumenta o contraste