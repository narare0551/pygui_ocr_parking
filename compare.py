import cv2


def compare_match(temp_i, m):
    print('유사이미지 찾기 들어옴')
    global found, frame
    #(pH,pW)= processed_2compare.shape[:2]
    #print('pH, pW',pH, pW)
    templatepath = ('C:\\Users\\USER\\Desktop\\test\\template\\facnroll7seg_v20\\20FACNROLL_' + str(
        temp_i) + '.png')  # trainImage
    print(templatepath)
    # 이미지 템플렛을 로딩해서 참고한다.
    template = cv2.imread(templatepath, cv2.IMREAD_COLOR)  # trainImage
    print('template',template)
    cv2.imshow('template',template)
    template_2gray=cv2.cvtColor(cv2.UMat(template), cv2.COLOR_BGR2GRAY)

    compare = cv2.matchTemplate(frame, template_2gray, m)
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(compare)
    print('minVal, maxVal, minLoc, maxLoc', minVal, maxVal, minLoc, maxLoc)
    if found == [] or maxVal > found[0] - 20000:
        found = [maxVal, maxLoc, temp_i]
    print('found', found)

compare_match(1,1)
