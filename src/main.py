import FreeSimpleGUI as sg
from image_selector import select_image

sg.theme('SystemDefaultForReal')   # Muda o tema da Janela

# Extrutura da Janela
layout = [
    [sg.Text('Olá! Escolha sua imagem para começar a editar:')],
    [sg.InputText(key='-IMG_PATH-', readonly=True), sg.Button('Selecionar Imagem')],
    [sg.Button('Ok'), sg.Button('Cancel')],
    [sg.Push(),  # Centraliza o quadrado horizontalmente
     sg.Frame('', [[sg.Text('', size=(900, 400), background_color='black')]],
              pad=(20, 20), element_justification='center', key='-QUADRO-'),
     sg.Push()]  # Centraliza o quadrado horizontalmente
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