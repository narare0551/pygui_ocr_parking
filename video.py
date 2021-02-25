import urllib

import numpy as np

import cv2


def get_video(url):


    global frame
    global height
    global width
    global top_left_x
    global top_left_y
    global bottom_right_x
    global bottom_right_y
    imgResp = urllib.request.urlopen(url)
    imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
    # opencv에서 사용할 수 있는 형식으로 decode한다.

    frame = cv2.imdecode(imgNp, -1)

    height, width = frame.shape[:2]
    top_left_x = int(width / 4)
    top_left_y = int((height / 2) + (height / 6))
    bottom_right_x = int((width / 4) + (width / 5))
    bottom_right_y = int((height / 2) - (height / 55))
    return frame



