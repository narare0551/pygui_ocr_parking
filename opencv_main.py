import urllib

import PySimpleGUI as sg
import cv2
import numpy as np
from PIL import ImageGrab

global frame, cropped, croppedgrab ,template
"""
Demo program that displays a webcam using OpenCV and applies some very basic image functions
- functions from top to bottom -
none:       no processing
threshold:  simple b/w-threshold on the luma channel, slider sets the threshold value
canny:      edge finding with canny, sliders set the two threshold values for the function => edge sensitivity
blur:       simple Gaussian blur, slider sets the sigma, i.e. the amount of blur smear
hue:        moves the image hue values by the amount selected on the slider
enhance:    applies local contrast enhancement on the luma channel to make the image fancier - slider controls fanciness.
"""
theme_dict = {'BACKGROUND': '#2B475D',
              'TEXT': '#FFFFFF',
              'INPUT': '#F2EFE8',
              'TEXT_INPUT': '#000000',
              'SCROLL': '#F2EFE8',
              'BUTTON': ('#000000', '#C2D4D8'),
              'PROGRESS': ('#FFFFFF', '#C7D5E0'),
              'BORDER': 1, 'SLIDER_DEPTH': 0, 'PROGRESS_DEPTH': 0}

# sg.theme_add_new('Dashboard', theme_dict)     # if using 4.20.0.1+
sg.LOOK_AND_FEEL_TABLE['Dashboard'] = theme_dict

BORDER_COLOR = '#C7D5E0'
DARK_HEADER_COLOR = '#1B2838'
BPAD_TOP = (20, 20)
BPAD_LEFT = ((20, 10), (0, 10))
BPAD_LEFT_INSIDE = (0, 10)
BPAD_RIGHT = ((100, 20), (10, 20))


def draw_rect(frame):
    global cropped
    height, width = frame.shape[:2]
    top_left_x = int(width / 4)
    top_left_y = int((height / 2) + (height / 3))
    bottom_right_x = int((width / 4) + (width / 3))
    bottom_right_y = int((height / 2) - (height / 40))
    cv2.rectangle(frame, (top_left_x, top_left_y), (bottom_right_x, bottom_right_y), 255, 3)
    cropped = frame[bottom_right_y:top_left_y, top_left_x:bottom_right_x]

def templates(a):
    global template
    global tH
    global tW
    global zipped_template


    # 저장경로에서 0-9까지의 template을 들고온다.
    templatepath = ('C:\\Users\\USER\\Desktop\\test\\verniersegment\\' + str(a) + 'vernier.png')  # trainImage
    # 이미지 템플렛을 로딩해서 참고한다.
    template = cv2.imread(templatepath, 1)  # trainImage
    # print('비교하는 숫자',a)

    # 이미지 template의 가로 세로를 구한다
    # grayscale로 변경하고
    template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    cv2.imshow('template', template)
    # 테두리를 감지한다  -> 인식률을 높여줌 (template이 이미 테두리 처리 된 거라서 일단 주석처리함)
    template = cv2.Canny(template, 50, 200)
    print(template)

    # templates.append(template)
    # numbers = range(0, 10)
    # zipped_template = (templates, numbers)

    # 템플렛의 가로 세로를 구한다
    (tH, tW) = template.shape[:2]
    return template
def main():
    global cropped, frame
    sg.theme('Dashboard')
    top = [[sg.Text('사용자화면', size=(10, 1), justification='c', pad=(10, 10), font='Any 20')],
           [sg.Image(filename='', key='-IMAGE-')], ]
    # define the window layout
    block_3 = [
        [sg.Radio('None', 'Radio', True, size=(10, 1))],
        [sg.Radio('threshold', 'Radio', size=(10, 1), key='-THRESH-'),
         sg.Slider((0, 255), 128, 1, orientation='h', size=(40, 15), key='-THRESH SLIDER-')],
        [sg.Radio('canny', 'Radio', size=(10, 1), key='-CANNY-'),
         sg.Slider((0, 255), 128, 1, orientation='h', size=(20, 15), key='-CANNY SLIDER A-'),
         sg.Slider((0, 255), 128, 1, orientation='h', size=(20, 15), key='-CANNY SLIDER B-')],
        [sg.Radio('blur', 'Radio', size=(10, 1), key='-BLUR-'),
         sg.Slider((1, 11), 1, 1, orientation='h', size=(40, 15), key='-BLUR SLIDER-')],
        [sg.Radio('hue', 'Radio', size=(10, 1), key='-HUE-'),
         sg.Slider((0, 225), 0, 1, orientation='h', size=(40, 15), key='-HUE SLIDER-')],
        [sg.Radio('enhance', 'Radio', size=(10, 1), key='-ENHANCE-'),
         sg.Slider((1, 255), 128, 1, orientation='h', size=(40, 15), key='-ENHANCE SLIDER-')],
        [sg.Button('Exit', size=(10, 1))]
    ]
    block_2 = [[sg.Text('캡처, 전처리', font='Any 20')],

               [sg.Image(filename='', key='-cropped_captured-'),
                sg.Image(filename='', key='-cropped_processed-'),
                ],
               [sg.Button('CUT', size=(10, 1))],
               [sg.Column(block_3, size=(500, 300), pad=(5, 5), background_color=BORDER_COLOR)],
               ]
    block_execute_btn = [
        [sg.Button('딥러닝', button_color=('white', 'black'), key='deeplearning'),
         sg.Button('TESSERACT', button_color=('white', 'black'), key='TESSERACT'),
         sg.Button('유사이미지', button_color=('white', 'firebrick3'), key='matchtemplate'),
         sg.Button('품목분류', button_color=('white', 'springgreen4'), key='categorize')]
    ]

    block_template=[
        [sg.Image(filename='', key='-template0-'),
         sg.Image(filename='', key='-template1-'),
         sg.Image(filename='', key='-template2-'),
         sg.Image(filename='', key='-template3-'),
         sg.Image(filename='', key='-template4-'),
         sg.Image(filename='', key='-template5-'),
         sg.Image(filename='', key='-template6-'),
         sg.Image(filename='', key='-template7-'),
         sg.Image(filename='', key='-template8-'),
         sg.Image(filename='', key='-template9-'),
         ],

    ]
    layout = [

        [sg.Column([
            [sg.Column(top, size=(400, 450), pad=(5, 5)),
             sg.Column(block_2, size=(520, 600), pad=(10, 10))]
            , [sg.Column(block_execute_btn, size=(800, 40), pad=(10, 10))]
            ,[sg.Column(block_template, size=(800, 100), pad=(10, 10))]
        ],

            background_color=BORDER_COLOR),

            # [sg.Column(top, size=(500, 500), pad= BPAD_LEFT_INSIDE, background_color=DARK_HEADER_COLOR)],
            # [sg.Column(block_3, size=(600, 300), pad=BPAD_TOP)],
        ],
    ]

    # create the window and show it without the plot
    window = sg.Window('OpenCV Integration', layout, location=(100, 200))

    cap = cv2.VideoCapture(0)


    while True:

        global cropped
        event, values = window.read(timeout=20)
        if event == 'Exit' or event == sg.WIN_CLOSED:
            break

        url = 'http://192.168.0.20:8080/shot.jpg'
        imgResp = urllib.request.urlopen(url)
        imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
        # cap = cv2.VideoCapture(0)
        cap = imgNp
        # ret, frame = cap.read()
        frame = cv2.imdecode(imgNp, -1)
        frame = cv2.resize(frame, dsize=(640, 480))
        draw_rect(frame)

        if values['-THRESH-']:
            processed = cv2.cvtColor(croppedgrab, cv2.COLOR_BGR2LAB)[:, :, 0]
            processed = cv2.threshold(processed, values['-THRESH SLIDER-'], 255, cv2.THRESH_BINARY)[1]
            processedbyte = cv2.imencode('.png', processed)[1].tobytes()
            window['-cropped_processed-'].update(data=processedbyte)

        elif values['-CANNY-']:
            processed = cv2.Canny(croppedgrab, values['-CANNY SLIDER A-'], values['-CANNY SLIDER B-'])
            processedbyte = cv2.imencode('.png', processed)[1].tobytes()
            window['-cropped_processed-'].update(data=processedbyte)
        elif values['-BLUR-']:
            processed = cv2.GaussianBlur(croppedgrab, (21, 21), values['-BLUR SLIDER-'])
            processedbyte = cv2.imencode('.png', processed)[1].tobytes()
            window['-cropped_processed-'].update(data=processedbyte)

        elif values['-HUE-']:
            processed = cv2.cvtColor(croppedgrab, cv2.COLOR_BGR2HSV)
            processedbyte = cv2.imencode('.png', processed)[1].tobytes()
            window['-cropped_processed-'].update(data=processedbyte)
        elif values['-ENHANCE-']:
            enh_val = values['-ENHANCE SLIDER-'] / 40
            clahe = cv2.createCLAHE(clipLimit=enh_val, tileGridSize=(8, 8))
            lab = cv2.cvtColor(croppedgrab, cv2.COLOR_BGR2LAB)
            lab[:, :, 0] = clahe.apply(lab[:, :, 0])
            processed = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
            processedbyte = cv2.imencode('.png', processed)[1].tobytes()
            window['-cropped_processed-'].update(data=processedbyte)
        # __cut image 부터 다시 하기
        elif event == 'CUT':

            croppedgrab = cropped
            croppedgrabbyte = cv2.imencode('.png', croppedgrab)[1].tobytes()
            window['-cropped_captured-'].update(data=croppedgrabbyte)

        elif event =='matchtemplate':
            for a in range(0, 10):
                templates(a)
                templatebytes = cv2.imencode('.png', template)[1].tobytes()
                window['-template' + str(a) + '-'].update(data=templatebytes)
        imgbytes = cv2.imencode('.png', frame)[1].tobytes()
        window['-IMAGE-'].update(data=imgbytes)

    window.close()


main()
