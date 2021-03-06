# TURTLEBOT3_wireless_motion_detection_driving_ROS2  
<br/>  
<br/>   
<br/>   

## 시연 모습    
![KakaoTalk_20220212_111535165](https://user-images.githubusercontent.com/79293543/153692619-bda131b6-4eed-4d21-8d10-427d254ff046.gif)  
    
![driving](https://user-images.githubusercontent.com/79293543/155058176-077bdf7e-c12a-406b-ab67-a17a47b42870.gif)  

![enter_desk](https://user-images.githubusercontent.com/79293543/155056879-83381471-4bb4-4764-b96d-4567a9662027.gif)  

<br/>   


## 개발환경1(라즈베리파이)     
PC : 우분투 20.04 , Python3.8 , VScode , ros2 foxy  
Turtlebot : Turtlebot3 , Opencr , Raspberry pi , Ros foxy , raspberry pi camera ,   
![라파 프로젝트 서현호 개발사양서 (14) (1)](https://user-images.githubusercontent.com/79293543/153694164-926ad39e-fd31-4f1b-b37b-944eca7fc874.jpg)  

<br/>   

  
  

## 개발환경2(젯슨 나노) -- 추천하지 않음
PC : 우분투 20.04 , Python3.8 , VScode , ros2 foxy  
Turtlebot : Turtlebot3 , opencr , Jetson nano , Xubuntu(ros2 설치버전)  
https://www.dropbox.com/s/tjg4irahues8esz/jetson_ros2_211015.zip?dl=0  
(ID : r1mini , PW : 1 )  
<br/>   

  
  
## 선행작업  
1. 터틀봇 3 메뉴얼 따라서 조립  
2. 터틀봇 사이트에서 3번 Quick start guide를 따라 ros버전을 foxy로 선택하고 절차대로 진행하여 bringup까지 마친다.  
https://emanual.robotis.com/docs/en/platform/turtlebot3/quick-start/  
절차대로 진행하던 중 어떤 과정에서 에러가 발생하면 처음부터 다시 하거나,  
그에 맞게 필요한 것들을 설치하거나, 수정하여 에러없이 진행을 완료시켜야 한다.  
<br/>   

  
  
## PC에 이 프로젝트를 구현할 ROS 패키지를 생성한다.  
```
ros2 pkg create --build-type ament_python [패키지명]
```
패키지를 생성하고 setup.py를 덮어쓰고,   
나머지 파일을 src 폴더에 다운로드 후    
작업 디렉토리를 해당 워크스페이스로 이동하여   
```
colcon build  
```
한다.  
동일한 네트워크 안에서 여러 터틀봇을 사용할 경우 노드명을 구별되게 바꿔주도록 한다.  
작업 속도를 향상시키기 위해 나노에디터로 bashrc에 들어가서 alias를 등록한다.  
```  
nano ~/.bashrc  
alias wksetup='source /opt/ros/foxy/setup.bash && source ~/[해당 워크스페이스]/install/local_setup.bash'  
```  
ctrl x  ->  y  ->  enter  
<br/>   
 
   
  
## 손 동작 학습시키기  
필자는 13만개의 손모양 데이터를 수집하여 XGBOOST를 이용하여 학습시켰다.   
여기서 제공되는 모델을 갖다 쓴다면 굳이 손 동작은 학습시킬 필요가 없다.  
하지만, 손 동작을 새롭게 학습시키고 싶다면 다음과 같은 과정을 거친다.  
![라파 프로젝트 서현호 개발사양서 (9)](https://user-images.githubusercontent.com/79293543/153701674-c64d8abe-e9e8-42d3-a489-677b40da7f2c.jpg)  
1. 손 동작 데이터 수집하기.  
PC에 웹캠을 연결하고 hand_data_gather.py와 hand_data_train.ipynb를 다운받는다.  
hand_data_gather.py라는 파일을 pc에서 실행한다.  
ctrl alt T 를 통해 터미널 창을 열고, 아래의 코드를 복사 붙여넣기 하여 필요한 라이브러리를 설치한다.  
```pip install mediapipe```  
파이썬 파일 내에서 라벨링 할 태그를 설정하고 해당하는 손 모양을 만든 후,  
손을 카메라위치에 두고 F5를 눌러 파이썬 파일을 실행하여 손 모양 데이터를 모은다.  
다양한 위치와 각도로 손 모양 데이터를 수집한다.  
![data_gather](https://user-images.githubusercontent.com/79293543/155054375-a12122c8-4451-42bd-9955-86fd04c6256b.gif)  
다른 태그에 대해서도 반복한다.  
미디어파이프로 데이터를 수집하고 학습시키는 이유는,   
필요없는 노이즈가 제거되어 대량의 데이터를 학습시키기가 용이하고,   
아주 짧은 시간의 학습으로 상당한 수준으로 정확도를 높일 수 있기 때문이다.   
2. 손 동작 학습시키기.  
hand_data_train.ipynb라는 파일을 열고,  
수집한 손 동작 데이터를 불러온다.  
![스크린샷, 2022-02-13 19-15-22](https://user-images.githubusercontent.com/79293543/153749294-d66930ae-78ab-4f34-9c3b-acdf942acad4.png)  
학습은 빠르고 성능이 좋은 XGBOOST를 사용한다.  
이 경우에 학습은 손 모양을 분류하는 것이므로,  
```from xgboost import XGBClassifier```  
를 사용한다.  
xgboost를 처음 사용한다면 ctrl alt T로 터미널창을 열어 라이브러리를 설치한다.  
```pip install xgboost```
Accuracy 값을 확인하면서 파라미터값을 조정해본다.  
(필자가 제공하는 모델은 Accuracy가 97%이다.)  
만족스러운 정확도가 나오면 모델을 저장한다.  
<br/>   

  
  

## 학습된 모델을 사용하여 손 동작을 기계적인 명령으로 변환하고, ROS로 터틀봇에 그 명령을 전달하기.  
학습된 모델을 불러와서 손 동작을 분류하는 함수를 만들고,  
그 분류된 값에 따라 서로 다른 제어 명령을 터틀봇으로 퍼블리싱하는 코드가 구현되어 있다.  
<br/>   
   
  
  
## 터틀봇의 Camera 정보 PC에서 받아보기.  
터틀봇에서 CompressedImage로 보내준 데이터를 PC 모니터에 출력하기.  
실시간 전송을 위하여 압축률이 높은 CompressedImage를 활용한다.  
터틀봇에 ssh로 접근하여 카메라 Publisher 노드를 실행하고,  
PC에서 카메라 Subscribe 노드를 실행하여 터틀봇 화면을 PC에 띄운다.  
CV_bridge를 이용하여 동일한 이미지에 대하여 로스와 opencv를 모두 활용할 수 있게 한다.  
퍼블리싱, 섭스크라이브 노드의 실행은 아래와 같이 한다.  
<br/>   
    
  
  
## 실행 
ctrl alt T를 통하여 터미널 창을 4개 띄운다. (터미네이터를 사용하면 편리하다)   
2개는 turtlebot 용이고, 2개는 pc용이다.  
![Screenshot from 2022-02-12 17-07-33](https://user-images.githubusercontent.com/79293543/153703383-1d100f2a-be4c-4671-bdee-90342b5a74cb.jpg) 
2개의 터미널에서  
```
ssh [turtlebotID]@[turtlebotIP주소]
```  
를 입력하여 ssh접속을 시도한다.  
비밀번호도 입력하여 준다.  
(터틀봇3의 기본설정 ID는 ubuntu 이며, PW는 turtlebot 이다.)  
(turtlebot의 IP확인은 터틀봇에 모니터를 연결하여 ifconfig로 확인하거나,  
http://192.168.0.1/ 로 들어가서 IP의 연결/끊김의 변화를 테스트해봐야한다.)  
그 중 1개의 터미널은 bringup을 하여 터틀봇이 모터 제어 토픽을 받을 수 있도록 만들 것이다.  
나머지 1개의 터미널은 터틀봇의 카메라를 퍼블리싱할 것이다.  
PC용 터미널 중 1개의 터미널에서는 손 동작을 인식받아서 모터 제어 토픽을 퍼블리싱할 것이다.   
PC용 나머지 터미널에서는 터틀봇이 보낸 카메라 이미지를 받아와서 화면에 출력하고 저장할 것이다.  
<br/>   
   
  
  
## 중간지점 및 Final지점 인식
코스를 만들고 체크포인트를 지정하면 여러 사람이 즐길 수 있는 주행게임을 만들 수 있다.  
중간지점과 도착지점을 인식도 카메라를 사용한다.  
터틀봇이 읽어들인 카메라 이미지에서 OCR로 읽어들인 글자가 미리 "중간지점" 이면,  
그 때의 주행 시간을 기억한다. 마지막 도착지점에서의 주행 시간은 총 주행시간이 된다.  
주행기록을 DB에 모아서 랭킹을 만들고 웹에서 보여줄 수 있다.  
![finish](https://user-images.githubusercontent.com/79293543/155057279-a80c477b-fefb-42b1-8235-5ac26f16c407.gif)  
![finish00](https://user-images.githubusercontent.com/79293543/155907012-b3a2fd2f-fba8-4ee2-9df6-a371424a7919.gif)  

<br/>   
 
  
  
## 인간 주행데이터로부터 자율주행 학습하기 
인간의 주행데이터를 다량으로 모으면 자율주행을 어느정도 학습시킬 수 있다.  
![Screenshot from 2022-02-14 10-49-02](https://user-images.githubusercontent.com/79293543/153787994-02fae01d-7a88-4dca-a4df-fb5eec67d2d1.png)  
성능 좋은 자율주행을 구현하고자 한다면 양질의 데이터와 훌륭한 알고리즘과 즉각적으로 처리할 수 있는 컴퓨팅 파워가 필요하다.  
또한 다양성을 줄일 수록 좋은 성능을 얻을 수 있다.  
피사체의 다양성 , 경로의 다양성을 줄이기 위해  
실내 비치물의 이동이 거의 없는 정해진 특정 실내 공간에 한해, 특정한 코스를 만들고  
데이터를 수집하는 것을 추천한다.  
학습은 구현하고자 하는 인공지능의 핵심 판단원리를 선정하고, 데이터 수집과 모델선정, 전처리, 학습과정으로 진행된다.  
1. 이미지를 통해 회피주행을 하고자 한다.   
그러기 위해서는 길이 없는 곳을 피하고 길이 있는 곳으로 나아가야 하는데,  
여기서는 도형의 무게중심을 이용하여 그 판단을 할 것이다.  
터틀봇 카메라로 인식된 이미지의 바닥면만을 추출하면 임의의 도형이 되는데, 그 도형에 대해 무게중심을 구한다.  
터틀봇은 그 무게중심 좌표 방향으로 이동한다.(앞이 막혀있으면, 즉 가운데 영역의 바닥면의 y값이 특정값보다 크면 우선 후진)  
추후에 보정계수를 넣어서 정확도를 높인다.  
핵심 가정은, '무게중심이 있는 곳에 넓은 길이 있다'이다.  
![ezgif com-gif-maker (2)](https://user-images.githubusercontent.com/79293543/155263305-256fa223-9cea-4bec-b9aa-66b126300435.gif)

2. 터틀봇이 보낸 프레임을 모두 PC에 저장하여 데이터를 수집한다.   
동시에 사람이 입력한 명령(전진/후진 속도, 좌/우 각도)을 이미지의 제목에 포함하여 이미지 이름으로 라벨링한다.  
또는 명령어를 담은 파일을 사진이름과 같게 저장하여 라벨링파일을 따로 생성할 수도 있다.  
3. 이미지를 전처리하여 2개의 단순한 이미지를 추가로 생성한다.  
받아온 이미지에서 수작업으로 주행 가능한 바닥면만 추출한다.  
![20220215_091429](https://user-images.githubusercontent.com/79293543/153968912-1dc67025-23c4-4e33-9c66-ebf67182f65e.gif)  
![20220215_091654](https://user-images.githubusercontent.com/79293543/153968791-51748390-ab6b-4f38-a56c-d959e7e12e3a.gif)  
![Screenshot from 2022-02-14 15-58-41](https://user-images.githubusercontent.com/79293543/153815161-6ff6a4ab-96af-4f73-afcc-bff34d444cef.png)  
추출된 바닥면이미지로부터 바닥면의 경계선만 남기는 이미지를 생성한다.  
우리는 이 폐곡면의 무게중심을 구할 것이다.  
4. GAN image-to-image를 통하여 이미지에서 바닥 폐곡면을 추출하는 과정을 학습시킨다.  
![image](https://user-images.githubusercontent.com/79293543/155912269-fb033fe1-f656-478e-9dcb-9f64bf707d7e.png)  
![image](https://user-images.githubusercontent.com/79293543/155912401-47f5a96e-f5e2-4ead-8cb5-5a0fa0e36481.png)  


