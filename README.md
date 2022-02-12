# turtlebot3_motion_driving

# 시연 모습   

# 개발환경1(라즈베리파이)     
PC : 우분투 20.04 , Python3.8 , VScode , ros2 foxy  
Turtlebot : Turtlebot3 , Opencr , Raspberry pi , Ros foxy , raspberry pi camera ,   

# 개발환경2(젯슨 나노) --  
PC : 우분투 20.04 , Python3.8 , VScode , ros2 foxy  
Turtlebot : Turtlebot3 , opencr , Jetson nano , Xubuntu(ros2 설치버전)

# 선행작업  
1. 터틀봇 3 메뉴얼 따라서 조립  
2. 터틀봇 사이트에서 3번 Quick start guide를 따라 ros버전을 foxy로 선택하고 절차대로 진행하여 bringup까지 마친다.  
https://emanual.robotis.com/docs/en/platform/turtlebot3/quick-start/  
절차대로 진행하던 중 어떤 과정에서 에러가 발생하면 처음부터 다시 하거나,  
그에 맞게 필요한 것들을 설치하거나, 수정하여 에러없이 진행을 완료시켜야 한다.  

# PC에 이 프로젝트를 구현할 ROS 패키지를 생성한다.  
패키지를 생성하고 setup.py를 덮어쓰고,  
나머지 파일을 src 폴더에 다운로드 후  
작업 디렉토리를 해당 워크스페이스로 이동하여 
```
colcon build
```
한다.  
동일한 네트워크 안에서 여러 터틀봇을 사용할 경우 노드명을 구별되게 바꿔주도록 한다.  

# 손 동작 학습시키기  
필자는 13만개의 손모양 데이터를 수집하여 XGBOOST를 이용하여 학습시켰다.   
여기서 제공되는 모델을 갖다 쓴다면 굳이 손 동작은 학습시킬 필요가 없다.  
하지만, 손 동작을 새롭게 학습시키고 싶다면 다음과 같은 과정을 거친다.  
1. 손 동작 데이터 수집하기.  
PC에 웹캠을 연결하고 learning.zip을 다운받는다.  
learning.zip이라는 압축파일을 풀고 gather.py라는 파일을 pc에서 실행한다.  
ctrl alt T 를 통해 터미널 창을 열고, 아래의 코드를 복사 붙여넣기 하여 필요한 라이브러리를 설치한다.  
```pip install mediapipe```  
라벨링 할 태그를 설정하고 해당하는 손 모양을 만든 후,  
손을 카메라위치에 두고 F5를 눌러 파이썬 파일을 실행하여 손 모양 데이터를 모은다.  
다양한 위치와 각도로 손 모양 데이터를 수집한다.  
다른 태그에 대해서도 반복한다.  
2. 손 동작 학습시키기.  
learning.py라는 파이썬 파일을 열고,  

# 학습된 모델을 사용하여 손 동작을 기계적인 명령으로 변환하고, ROS로 터틀봇에 그 명령을 전달하기.  

# 터틀봇의 Camera 정보 PC에서 받아보기.  

# 실행 
ctrl alt T를 통하여 터미널 창을 4개 띄운다. (터미네이터를 사용하면 편리하다)   
2개는 turtlebot 용이고, 2개는 pc용이다.  
2개의 터미널에서  
```
ssh turtlebotID@turtlebotIP주소
```  
를 입력하여 ssh접속을 시도한다.  
비밀번호도 입력하여 준다.  
그 중 1개의 터미널은 bringup을 하여 터틀봇이 모터 제어 토픽을 받을 수 있도록 만들 것이다.  
나머지 1개의 터미널은 터틀봇의 카메라를 퍼블리싱할 것이다.  
PC용 터미널 중 1개의 터미널에서는 손 동작을 인식받아서 모터 제어 토픽을 퍼블리싱할 것이다.   
PC용 나머지 터미널에서는 터틀봇이 보낸 카메라 이미지를 받아와서 화면에 출력하고 저장할 것이다.  

