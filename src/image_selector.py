import FreeSimpleGUI as sg
from pathlib import Path

def select_image():
    file_path = sg.popup_get_file(
        'Escolha uma imagem',
        file_types=(("Imagens", ".png;.jpg;.jpeg;.bmp;*.gif"),),
        initial_folder=str(Path.home())
    )
    return file_path