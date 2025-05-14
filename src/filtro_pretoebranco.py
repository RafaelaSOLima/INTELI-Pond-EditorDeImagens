def apply(image):
    """Converte a imagem para tons de cinza (preto e branco)."""
    # Converte para escala de cinza e depois retorna para 'RGB' para manter consistência
    return image.convert("L").convert("RGB")