import FreeSimpleGUI as sg
from PIL import Image
import io
from image_selector import select_image

# Importa os módulos dos filtros
import filtro_embacado
import filtro_nitidez
import filtro_inversao
import filtro_alto_contraste
import filtro_baixo_contraste
import filtro_pretoebranco

sg.theme('SystemDefaultForReal')

layout = [
    [sg.Text('Olá! Escolha sua imagem para começar a editar:')],
    [sg.Text('Filtros:'),
     sg.Checkbox('Embaçado', key='-CHK_A-', enable_events=True),
     sg.Checkbox('Nitido', key='-CHK_B-', enable_events=True),
     sg.Checkbox('Invertido', key='-CHK_C-', enable_events=True),
     sg.Checkbox('Alto Contraste', key='-CHK_D-', enable_events=True),
     sg.Checkbox('Baixo Contraste', key='-CHK_E-', enable_events=True),
     sg.Checkbox('Preto e Branco', key='-CHK_F-', enable_events=True)],
    
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

def load_and_resize_image(image_path, max_width, max_height):
    """
    Abre e redimensiona a imagem mantendo a proporção para o tamanho máximo disponível.
    Retorna a imagem PIL redimensionada.
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
    return img

def image_to_bytes(img):
    """Converte uma imagem PIL para bytes (PNG) para usar no elemento Image."""
    bio = io.BytesIO()
    img.save(bio, format="PNG")
    return bio.getvalue()

# Armazena a imagem base redimensionada para aplicar os filtros
base_img = None

def apply_filters(base_img, values):
    """
    Aplica, em sequência, os filtros selecionados à imagem base.
    """
    img_filtered = base_img.copy()
    if values.get('-CHK_A-'):
        img_filtered = filtro_embacado.apply(img_filtered)
    if values.get('-CHK_B-'):
        img_filtered = filtro_nitidez.apply(img_filtered)
    if values.get('-CHK_C-'):
        img_filtered = filtro_inversao.apply(img_filtered)
    if values.get('-CHK_D-'):
        img_filtered = filtro_alto_contraste.apply(img_filtered)
    if values.get('-CHK_E-'):
        img_filtered = filtro_baixo_contraste.apply(img_filtered)
    if values.get('-CHK_F-'):
        img_filtered = filtro_pretoebranco.apply(img_filtered)
    return img_filtered

while True:
    event, values = window.read(timeout=100)
    if event in (sg.WINDOW_CLOSED, 'Cancelar'):
        break

    if event == 'Selecionar Imagem':
        image_path = select_image()
        if image_path:
            window['-IMG_PATH-'].update(image_path)
            window.refresh()  # Atualiza a janela para obter dimensões reais

            # Obtém as dimensões atuais da janela
            win_width = window.TKroot.winfo_width()
            win_height = window.TKroot.winfo_height()

            # Define o espaço disponível para a imagem (reservando área para textos e botões)
            available_height = win_height - 150  
            available_width = (win_width // 2) - 20  

            # Carrega e redimensiona a imagem
            base_img = load_and_resize_image(image_path, available_width, available_height)
            base_bytes = image_to_bytes(base_img)
            # Atualiza ambas as imagens inicialmente com a imagem base
            window['-IMG_ESQ-'].update(data=base_bytes)
            window['-IMG_DIR-'].update(data=base_bytes)

            # Reinicia os filtros (desmarca os checkboxes)
            window['-CHK_A-'].update(False)
            window['-CHK_B-'].update(False)
            window['-CHK_C-'].update(False)
            window['-CHK_D-'].update(False)
            window['-CHK_E-'].update(False)
            window['-CHK_F-'].update(False)

    # Se alguma checkbox for clicada e a imagem estiver carregada, atualiza a imagem da esquerda
    if event in ('-CHK_A-', '-CHK_B-', '-CHK_C-', '-CHK_D-', '-CHK_E-', '-CHK_F-') and base_img:
        filtered_img = apply_filters(base_img, values)
        filtered_bytes = image_to_bytes(filtered_img)
        # Atualiza somente a imagem da esquerda com os filtros aplicados
        window['-IMG_ESQ-'].update(data=filtered_bytes)

    if event == 'Salvar':
        print("Imagem selecionada:", values["-IMG_PATH-"])
        # Aqui você pode adicionar a lógica para salvar a imagem final, se desejar.

window.close()