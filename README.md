# Iotproject

다음의 구조로 이루어져 있다.

UWB - Raspberrypi1 -> PC -> Raspberrypi2

UWB-Rasp1는 Blue통신, Rasp1 -> PC ->Rasp2는 MQTT 통신

UWB를 이용 좌표를 계산하여 K-means를 통해 부분 최소 혼잡 구역을 찾고자 하는게 목표다.

K-means는 img.py에 존재한다.

