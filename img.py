import matplotlib.pyplot as plt
import matplotlib.image as img
import numpy as np
from sklearn.cluster import KMeans
import math
import certifi
import paho.mqtt.client as mqtt
import json
import random
np.set_printoptions(precision=4, suppress=True)
img_test = img.imread('way.jpg') #칸 하나의 넓이는 3M에 해당한다.

global mqttc

def circlehave(Xlist,center,length):
  incount=0
  for item in Xlist:
    distance=math.sqrt(((item[0]-center[0])**2)+(item[1]-center[1])**2)
    if(distance<=length):
      incount+=1
  return incount
def subway(K,data,max,last,datajson,end):
  check_people = 3
  jamlist = []
  circle = 0
  Kmeans = KMeans(n_clusters=K,init='k-means++',random_state=0)
  Kmeans.fit(data)
  center = Kmeans.cluster_centers_
  new_label = Kmeans.labels_
  count = new_label.tolist()
  if(end==0):
    a=plt.axes()
    plt.axis('off')
  for i in range(K):
    clusterlist = list(filter(lambda x : count[x]==i, range(len(count))))
    circle_center = (center[i][0],center[i][1])
    circle_length = 10 
    inner_count = circlehave(data[clusterlist],circle_center,circle_length)
    if(inner_count>=check_people):
      circle+=1
      if(end==0):
        jamlist.extend(clusterlist)
        c = plt.Circle(circle_center, circle_length, fc="w",ec='r')
        a.add_patch(c)
  if(end==0):
    for (i,index) in enumerate(datajson):
      index["is_jam"] = 0
      if(jamlist.count(i)):
        index["is_jam"] = 1
    mqttc.publish('too',payload=json.dumps(datajson))
    print("현재 부분 혼잡 구역은 최소 ",last[0],"개 존재합니다.")
    print("부분 혼잡 구역 좌표")
    for i in range(0,max):
      if(count.count(i)>=check_people):
        print(center[i])
    plt.imshow(img_test)
    plt.scatter(data[:,0], data[:,1], c=new_label)
    # plt.show()
    plt.pause(10)
    plt.show(block=False)
    plt.pause(10)
    plt.close()
    return
  if(circle>=last[0]):
    last[0] = circle
    last[1] = K    
  if(K<max):
    subway(K+1,data,max,last,datajson,1)
  else:
    subway(last[1],data,max,last,datajson,0)

def on_connect(client, userdata, flags, rc):  # The callback for when the client connects to the broker
    print("MQTT 통신 준비 완료")  # Print result of connection attempt
    client.subscribe('foo')
def on_message(client, userdata, msg):  # The callback for when a PUBLISH message is received from the server.
    plt.close()
    print("좌표 데이터가 송신되었습니다.")
    data = json.loads(msg.payload)
    localList = []
    count = 0
    last = [0,0]
    for i in data:
      localList.append([i['X'],i['Y']])
      count+=1
    kList = np.array(localList)
    print("데이터 분석을 시작합니다.")
    subway(2,kList,count,last,data,1)

    # mqttc.publish("too",data)
mqttc = mqtt.Client(transport='websockets') #solace 페이지에서 실시간 확인을 위해 webSocket Secured MQTT HOST로 연결
mqttc.on_connect = on_connect #on_connect 함수 매핑
mqttc.on_message = on_message #on_message 함수 매핑
mqttc.tls_set(ca_certs=certifi.where()) #wss 인증 추가
mqttc.username_pw_set("solace-cloud-client", "ebq00j24cs437t3gand65kdi60") #username과 password 설정
mqttc.connect("mruupcsnwrxka.messaging.solace.cloud", port=8443) #host와 port 설정 wss->8443
mqttc.loop_forever()  # Start networking daemon


# 랜덤 데이터 -> 테스트 용
# n=100
# XY= np.random.rand(n,2)
# XY[:,1] = XY[:,1]*830
# XY[:,0] = XY[:,0]*160
# subway(2,XY,n,[0,0])




