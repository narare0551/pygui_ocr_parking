import cv2
def video_process(image):
    global mask
    global top_left_x
    global top_left_y
    global bottom_right_x
    global bottom_right_y
    #cropped = video[bottom_right_y:top_left_y, top_left_x:bottom_right_x]
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # blur처리 한다
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    # canny함수를 사용한다.
    canny = cv2.Canny(blur, 10, 100)
    cv2.imshow('canny', canny)
    # 이진화해서 나온 이미지 결과값을 mask에 저장한다.
    ret, mask = cv2.threshold(canny, 1, 255, cv2.THRESH_BINARY)
    contours, hier = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
