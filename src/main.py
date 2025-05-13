import FreeSimpleGUI as sg
from PIL import Image
import io
from image_selector import select_image

sg.theme('SystemDefaultForReal')

layout = [
    [sg.Text('Olá! Escolha sua imagem para começar a editar:')],
    [sg.Column([
        [sg.Frame('', [[sg.Image(key='-IMG_ESQ-')]], key='-QUADRO_ESQ-', expand_x=True, expand_y=True)]
    ], expand_x=True, expand_y=True),
     sg.Column([
        [sg.Frame('', [[sg.Image(key='-IMG_DIR-')]], key='-QUADRO_DIR-', expand_x=True, expand_y=True)]
    ], expand_x=True, expand_y=True)],
    [sg.InputText(key='-IMG_PATH-', readonly=True), sg.Button('Selecionar Imagem')],
    [sg.Button('Ok'), sg.Button('Cancel')]
]

window = sg.Window(
    "Akirah s Image Editor",
    layout,
    icon='../assets/picture.ico',
    finalize=True,
    resizable=True
)
window.Maximize()


def resize_image(image_path, max_width, max_height):
    """
    Redimensiona a imagem para preencher o espaço disponível (max_width x max_height)
    sem distorção, mantendo a proporção.
    """
    img = Image.open(image_path)
    img_ratio = img.width / img.height
    frame_ratio = max_width / max_height

    if img_ratio > frame_ratio:
        # Encaixa pela largura
        new_width = max_width
        new_height = int(max_width / img_ratio)
    else:
        # Encaixa pela altura
        new_height = max_height
        new_width = int(max_height * img_ratio)
    
    # Redimensiona (permitindo upscaling se necessário)
    img = img.resize((new_width, new_height), Image.LANCZOS)
    bio = io.BytesIO()
    img.save(bio, format="PNG")
    return bio.getvalue()


while True:
    event, values = window.read(timeout=100)
    if event in (sg.WINDOW_CLOSED, 'Cancel'):
        break

    # Quando o usuário seleciona uma imagem
    if event == 'Selecionar Imagem':
        image_path = select_image()
        if image_path:
            window['-IMG_PATH-'].update(image_path)
            # Permite que a janela finalize seu redimensionamento e obtenha valores reais
            window.refresh()

            # Obtém as dimensões atuais da janela
            win_width = window.TKroot.winfo_width()
            win_height = window.TKroot.winfo_height()

            # Definindo margens:
            # - Supomos que a área superior (texto) e inferior (botões) ocupem cerca de 150 pixels
            available_height = win_height - 150  
            # Cada imagem ocupa metade da largura disponível, com uma margem horizontal de 20 pixels
            available_width = (win_width // 2) - 20  

            # Calcula e gera a imagem redimensionada
            resized_image = resize_image(image_path, available_width, available_height)
            
            # Atualiza as duas imagens na interface
            window['-IMG_ESQ-'].update(data=resized_image)
            window['-IMG_DIR-'].update(data=resized_image)

    if event == 'Ok':
        print("Imagem selecionada:", values["-IMG_PATH-"])

window.close()