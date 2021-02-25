import cv2
def templates():
    global templates
    global tH
    global tW
    global zipped_template

    for a in range(0, 10):
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
        cv2.imshow('template', template)
        # templates.append(template)
        # numbers = range(0, 10)
        # zipped_template = (templates, numbers)

        # 템플렛의 가로 세로를 구한다
        (tH, tW) = template.shape[:2]
templates()

