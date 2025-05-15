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
     sg.Checkbox('Preto e Branco', key='-CHK_F-', enable_events=True),
     sg.Button('Rotacionar', key='-ROTATE-'),
     sg.Button('Recortar', key='-CROP-')],
    [
        sg.Column(
            [[sg.Canvas(key='-CANVAS_ESQ-', background_color='black', expand_x=True, expand_y=True)]],
            expand_x=True, expand_y=True
        ),
        sg.Column(
            [[sg.Image(key='-IMG_DIR-')]],
            expand_x=True, expand_y=True
        )
    ],
    [sg.InputText(key='-IMG_PATH-', readonly=True),
     sg.Button('Selecionar Imagem'),
     sg.Button('Salvar'),
     sg.Button('Cancelar')],
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
    bio = io.BytesIO()
    img.save(bio, format="PNG")
    return bio.getvalue()

def rotate_image(img, max_width, max_height):
    img = img.rotate(90, expand=True)
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

def apply_filters(base_img, values):
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

def draw_image_on_canvas(canvas, img):
    from PIL import ImageTk
    photo_img = ImageTk.PhotoImage(img)
    canvas.image = photo_img  # Referência para evitar garbage collector
    canvas.create_image(0, 0, image=photo_img, anchor="nw")

def crop_selection(start_x, start_y, end_x, end_y, resized_img, base_img):
    if resized_img and base_img:
        x1 = min(start_x, end_x)
        y1 = min(start_y, end_y)
        x2 = max(start_x, end_x)
        y2 = max(start_y, end_y)

        scale_x = base_img.width / resized_img.width
        scale_y = base_img.height / resized_img.height

        crop_box = (int(x1 * scale_x), int(y1 * scale_y), int(x2 * scale_x), int(y2 * scale_y))

        cropped_base = base_img.crop(crop_box)
        resized = load_and_resize_image(io.BytesIO(image_to_bytes(cropped_base)), resized_img.width, resized_img.height)
        return cropped_base, resized
    return base_img, resized_img

# Estados globais
base_img = None
resized_img = None
is_cropping = False

canvas_elem = window['-CANVAS_ESQ-']
canvas_widget = canvas_elem.Widget
canvas = None  # Definido após imagem ser carregada

while True:
    event, values = window.read(timeout=100)
    if event in (sg.WINDOW_CLOSED, 'Cancelar'):
        break

    if event == 'Selecionar Imagem':
        image_path = select_image()
        if image_path:
            window['-IMG_PATH-'].update(image_path)
            window.refresh()

            win_width = window.TKroot.winfo_width()
            win_height = window.TKroot.winfo_height()
            available_height = win_height - 150
            available_width = (win_width // 2) - 20

            base_img = Image.open(image_path)
            resized_img = load_and_resize_image(image_path, available_width, available_height)
            image_bytes = image_to_bytes(resized_img)

            if canvas:
                canvas.delete("all")
            else:
                from tkinter import Canvas
                canvas = Canvas(canvas_widget, bg='black', width=resized_img.width, height=resized_img.height)
                canvas.pack(expand=True, fill="both")

            draw_image_on_canvas(canvas, resized_img)
            window['-IMG_DIR-'].update(data=image_bytes)

            for chk in ['-CHK_A-', '-CHK_B-', '-CHK_C-', '-CHK_D-', '-CHK_E-', '-CHK_F-']:
                window[chk].update(False)

    if event in ('-CHK_A-', '-CHK_B-', '-CHK_C-', '-CHK_D-', '-CHK_E-', '-CHK_F-') and base_img:
        filtered_img = apply_filters(base_img, values)
        filtered_resized = load_and_resize_image(io.BytesIO(image_to_bytes(filtered_img)), resized_img.width, resized_img.height)
        draw_image_on_canvas(canvas, filtered_resized)

    if event == '-ROTATE-' and base_img:
        win_width = window.TKroot.winfo_width()
        win_height = window.TKroot.winfo_height()
        available_height = win_height - 150
        available_width = (win_width // 2) - 20

        base_img = base_img.rotate(90, expand=True)
        resized_img = load_and_resize_image(io.BytesIO(image_to_bytes(base_img)), available_width, available_height)
        draw_image_on_canvas(canvas, resized_img)

    if event == 'Salvar' and base_img:
        save_path = sg.popup_get_file('Salvar imagem como', save_as=True,
                                      file_types=(("PNG Files", "*.png"), ("JPEG Files", "*.jpg")))
        if save_path:
            filtered_img = apply_filters(base_img, values)
            filtered_img.save(save_path)
            sg.popup('Imagem salva com sucesso!')

    if event == '-CROP-' and base_img and resized_img:
        is_cropping = True
        coords = {'start_x': 0, 'start_y': 0, 'end_x': 0, 'end_y': 0}

        def on_press(e):
            coords['start_x'], coords['start_y'] = e.x, e.y

        def on_drag(e):
            coords['end_x'], coords['end_y'] = e.x, e.y
            canvas.delete("rect")
            canvas.create_rectangle(coords['start_x'], coords['start_y'], coords['end_x'], coords['end_y'],
                                    outline='red', width=2, tags="rect")

        def on_release(e):
            coords['end_x'], coords['end_y'] = e.x, e.y
            canvas.delete("rect")
            global base_img, resized_img, is_cropping
            base_img, resized_img = crop_selection(coords['start_x'], coords['start_y'],
                                                    coords['end_x'], coords['end_y'],
                                                    resized_img, base_img)
            draw_image_on_canvas(canvas, resized_img)
            is_cropping = False
            canvas.unbind("<ButtonPress-1>")
            canvas.unbind("<B1-Motion>")
            canvas.unbind("<ButtonRelease-1>")

        canvas.bind("<ButtonPress-1>", on_press)
        canvas.bind("<B1-Motion>", on_drag)
        canvas.bind("<ButtonRelease-1>", on_release)

window.close()
