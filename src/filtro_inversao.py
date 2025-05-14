from PIL import ImageOps

def apply(image):
    """Inverte as cores da imagem."""
    # Certifica que a imagem está em modo RGB para inverter corretamente
    if image.mode != "RGB":
        image = image.convert("RGB")
    return ImageOps.invert(image)