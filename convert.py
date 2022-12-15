import cv2
import numpy as np
from random import *

np.set_printoptions(precision=3) #소수점 세 번째에서 반올림

src = cv2.imread("subway.jpg", cv2.IMREAD_COLOR)
#height, width, channel = src.shape

width = 160
height = 810

#srcPoint = np.array([[0, 0], [width, 0], [1140, 702], [0, height]], dtype=np.float32)
srcPoint = np.array([[267,249], [338,247], [630,425], [0,425]], dtype=np.float32) #원본 이미지 특징점
dstPoint = np.array([[0, 0], [width, 0], [width, height], [0, height]], dtype=np.float32) #변환된 이미지 크기 지정

matrix = cv2.getPerspectiveTransform(srcPoint, dstPoint) #투영(원근) 변환 행렬
inverse = np.linalg.pinv(matrix) #투영 변환 행렬의 의사 역행렬
print(np.dot(matrix, inverse)) #의사 역행렬이 맞는지 검증
dst = cv2.warpPerspective(src, matrix, (width, height)) #변환 이미지 디스크립터 지정

cv2.imwrite("result.jpg", dst) #변환 이미지 result.jpg로 저장


'''
cv2.line(dst, (107, 0), (107, height), (255,0,0), 2)
cv2.line(dst, (215, 0), (215, height), (255,0,0), 2)
cv2.line(dst, (323, 0), (323, height), (255,0,0), 2)
cv2.line(dst, (431, 0), (429, height), (255,0,0), 2)
cv2.line(dst, (543, 0), (538, height), (255,0,0), 2)
cv2.line(dst, (640, 0), (644, height), (255,0,0), 2)
cv2.line(dst, (747, 0), (750, height), (255,0,0), 2)
cv2.line(dst, (854, 0), (857, height), (255,0,0), 2)
cv2.line(dst, (958, 0), (954, height), (255,0,0), 2)
cv2.line(dst, (1063, 0), (1066, height), (255,0,0), 2)
cv2.line(dst, (1167, 0), (1176, height), (255,0,0), 2)  #vertical line

cv2.line(dst, (0, 70), (width, 70), (255,0,0), 2) #horizontal line
cv2.line(dst, (0, 123), (width, 123), (255,0,0), 2)
cv2.line(dst, (0, 184), (width, 184), (255,0,0), 2)
cv2.line(dst, (0, 230), (width, 230), (255,0,0), 2)
cv2.line(dst, (0, 280), (width, 280), (255,0,0), 2)
cv2.line(dst, (0, 329), (width, 329), (255,0,0), 2)
cv2.line(dst, (0, 381), (width, 381), (255,0,0), 2)
cv2.line(dst, (0, 431), (width, 431), (255,0,0), 2)
cv2.line(dst, (0, 481), (width, 481), (255,0,0), 2)
cv2.line(dst, (0, 531), (width, 531), (255,0,0), 2)
cv2.line(dst, (0, 581), (width, 581), (255,0,0), 2)
cv2.line(dst, (0, 631), (width, 631), (255,0,0), 2)
cv2.line(dst, (0, 691), (width, 691), (255,0,0), 2)
cv2.line(dst, (0, 751), (width, 751), (255,0,0), 2)
cv2.line(dst, (0, 811), (width, 811), (255,0,0), 2)
cv2.line(dst, (0, 881), (width, 881), (255,0,0), 2)
cv2.line(dst, (0, 951), (width, 951), (255,0,0), 2)
cv2.line(dst, (0, 1011), (width, 1011), (255,0,0), 2)
cv2.line(dst, (0, 1064), (width, 1064), (255,0,0), 2)
cv2.line(dst, (0, 1119), (width, 1119), (255,0,0), 2)
cv2.line(dst, (0, 1173), (width, 1173), (255,0,0), 2)
cv2.line(dst, (0, 1225), (width, 1225), (255,0,0), 2)




for i in range(1, 30):
    j = randint(0, 1280)
    k = randint(0, 1280)
    pts3 = np.array([[j,k], [j+20,k-20], [j+40,k]], dtype=np.int32)
    cv2.polylines(dst, [pts3], True, (0,0,255), 15)
'''
cv2.imwrite("test2.jpg", dst)
cv2.imshow("dst", dst)
cv2.waitKey(0)
cv2.destroyAllWindows()

"""
724, 1783 -> 0, 0
726, 2962 -> 0, height
1846, 1690 -> width, 0
3664, 2312 -> width, height
3174, 2141
2684
2194
1704, 1628


1140 702 -> 1280, 720
"""