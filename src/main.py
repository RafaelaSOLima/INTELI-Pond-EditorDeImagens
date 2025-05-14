import FreeSimpleGUI as sg
from PIL import Image
import io
from image_selector import select_image

sg.theme('SystemDefaultForReal')

layout = [
    [sg.Text('Olá! Escolha sua imagem para começar a editar:')],
    [sg.Text('Filtros:'),
     sg.Checkbox('Embaçado', key='-CHK_A-'),
     sg.Checkbox('Nitido', key='-CHK_B-'),
     sg.Checkbox('Invertido', key='-CHK_C-'),
     sg.Checkbox('Alto Contraste', key='-CHK_D-'),
     sg.Checkbox('Baixo Contraste', key='-CHK_E-'),
     sg.Checkbox('Preto e Branco', key='-CHK_F-')],  

    [
        sg.Column(
            [
                [sg.Frame(
                    '',
                    [
                        [sg.Column(
                            [
                                [sg.VPush()],
                                [sg.Image(key='-IMG_ESQ-')],
                                [sg.VPush()]
                            ],
                            expand_x=True,
                            expand_y=True,
                            justification='center'
                        )]
                    ],
                    key='-QUADRO_ESQ-',
                    expand_x=True,
                    expand_y=True
                )]
            ],
            expand_x=True,
            expand_y=True
        ),
        sg.Column(
            [
                [sg.Frame(
                    '',
                    [
                        [sg.Column(
                            [
                                [sg.VPush()],
                                [sg.Image(key='-IMG_DIR-')],
                                [sg.VPush()]
                            ],
                            expand_x=True,
                            expand_y=True,
                            justification='center'
                        )]
                    ],
                    key='-QUADRO_DIR-',
                    expand_x=True,
                    expand_y=True
                )]
            ],
            expand_x=True,
            expand_y=True
        )
    ],
    [sg.InputText(key='-IMG_PATH-', readonly=True), sg.Button('Selecionar Imagem')],
    [sg.Button('Salvar'), sg.Button('Cancelar')]
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
    Redimensiona a imagem para preencher o espaço disponível sem distorção,
    mantendo sua proporção.
    """
    img = Image.open(image_path)
    img_ratio = img.width / img.height
    frame_ratio = max_width / max_height

    if img_ratio > frame_ratio:
        new_width = max_width
        new_height = int(max_width / img_ratio)
    else:
        new_height = max_height
        new_width = int(max_height * img_ratio)

    img = img.resize((new_width, new_height), Image.LANCZOS)
    bio = io.BytesIO()
    img.save(bio, format="PNG")
    return bio.getvalue()


while True:
    event, values = window.read(timeout=100)
    if event in (sg.WINDOW_CLOSED, 'Cancelar'):
        break

    if event == 'Selecionar Imagem':
        image_path = select_image()
        if image_path:
            window['-IMG_PATH-'].update(image_path)
            window.refresh()  # Atualiza a janela para obter dimensões reais

            # Captura as dimensões atuais da janela
            win_width = window.TKroot.winfo_width()
            win_height = window.TKroot.winfo_height()

            # Reserva espaço para textos e botões
            available_height = win_height - 150  
            available_width = (win_width // 2) - 20  

            # Redimensiona a imagem para ocupar o máximo possível do espaço disponível
            resized_image = resize_image(image_path, available_width, available_height)

            # Atualiza as duas imagens com a imagem redimensionada
            window['-IMG_ESQ-'].update(data=resized_image)
            window['-IMG_DIR-'].update(data=resized_image)

    if event == 'Salvar':
        print("Imagem selecionada:", values["-IMG_PATH-"])

window.close()