import numpy as np
import certifi
import paho.mqtt.client as mqtt
import cv2
import json

np.set_printoptions(precision=3) #소수점 세 번째에서 반올림

src = cv2.imread("subway.jpg", cv2.IMREAD_COLOR)

width = 160
height = 810

srcPoint = np.array([[267,249], [338,247], [630,425], [0,425]], dtype=np.float32) #원본 이미지 특징점
dstPoint = np.array([[0, 0], [width, 0], [width, height], [0, height]], dtype=np.float32) #변환된 이미지 크기 지정

matrix = cv2.getPerspectiveTransform(srcPoint, dstPoint) #투영(원근) 변환 행렬
inverse = np.linalg.pinv(matrix) #투영 변환 행렬의 의사 역행렬

"""inverse = np.array([[-4.40, 3.46, -2803.13],
 [ 0.31, 2.57,-2614.16],
 [ 0.01, 0.01,-10.49]])"""

def on_connect(client, userdata, flags, rc):  # The callback for when the client connects to the broker
    print("MQTT 통신 준비 완료")  # Print result of connection attempt
    client.subscribe('too')

def on_message(client, userdata, msg):  # The callback for when a PUBLISH message is received from the server.
    print("좌표 데이터가 송신되었습니다.")
    data = json.loads(msg.payload)
    img = cv2.imread("subway.jpg", cv2.IMREAD_COLOR)
    for i in data:
        if i['is_jam'] == 0: #혼잡X
            pos = np.array([i['X'], i['Y']])
            p1 = np.squeeze(inverse @ np.expand_dims(np.append(pos, 1), axis=1))
            p1 = p1[:2] / p1[2]
            img = cv2.circle(img, (int(p1[0]), int(p1[1])), 2, (255,0,0), 2)
        elif i['is_jam'] == 1: #혼잡O
            pos = np.array([i['X'], i['Y']])
            p1 = np.squeeze(inverse @ np.expand_dims(np.append(pos, 1), axis=1))
            p1 = p1[:2] / p1[2]
            img = cv2.circle(img, (int(p1[0]), int(p1[1])), 3, (0,0,255), 4)
    cv2.imshow('subway', img)
    cv2.waitKey(10000)
    cv2.destroyAllWindows()

mqttc = mqtt.Client(transport='websockets') #solace 페이지에서 실시간 확인을 위해 webSocket Secured MQTT HOST로 연결
mqttc.on_connect = on_connect #on_connect 함수 매핑
mqttc.on_message = on_message #on_message 함수 매핑
mqttc.tls_set(ca_certs=certifi.where()) #wss 인증 추가
mqttc.username_pw_set("solace-cloud-client", "ebq00j24cs437t3gand65kdi60") #username과 password 설정
mqttc.connect("mruupcsnwrxka.messaging.solace.cloud", port=8443) #host와 port 설정 wss->8443
mqttc.loop_forever()  # Start networking daemon
