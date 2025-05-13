import FreeSimpleGUI as sg
from image_selector import select_image

sg.theme('SystemDefaultForReal')   # Muda o tema da Janela

# Extrutura da Janela
layout = [
    [sg.Text('Olá! Escolha sua imagem para começar a editar:')],
    [sg.Column([
        [sg.Frame('', [[sg.Text('', size=(None, None))]], key='-QUADRO_ESQ-', expand_x=True)]
    ], element_justification='right', expand_x=True),
     sg.Column([
        [sg.Frame('', [[sg.Text('', size=(None, None))]], key='-QUADRO_DIR-', expand_x=True)]
    ], element_justification='left', expand_x=True)],
    [sg.InputText(key='-IMG_PATH-', readonly=True), sg.Button('Selecionar Imagem')],
    [sg.Button('Ok'), sg.Button('Cancel')]
]



# Cria a janela em tela cheia
window = sg.Window(
    'Akirah s Image Editor',
    layout,
    icon='../assets/picture.ico',
    finalize=True,
    resizable=True
)
window.Maximize()  # Deixa a janela em tela cheia
# Loop de eventos
while True:
    event, values = window.read()
    
    if event in (sg.WINDOW_CLOSED, 'Cancelar'):
        break
    
    if event == 'Selecionar Imagem':
        image_path = select_image()
        if image_path:
            window['-IMG_PATH-'].update(image_path)
    
    if event == 'Ok':
        print('Imagem selecionada:', values['-IMG_PATH-'])

window.close()