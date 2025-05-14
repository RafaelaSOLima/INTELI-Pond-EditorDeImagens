from PIL import ImageEnhance

def apply(image):
    """Reduz o contraste da imagem."""
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(0.5)  # fator 0.5 diminui o contraste