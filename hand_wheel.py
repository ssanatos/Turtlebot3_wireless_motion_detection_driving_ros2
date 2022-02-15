import rclpy
from rclpy.node import Node
import cv2 as cv
from geometry_msgs.msg import Twist
from cvzone.HandTrackingModule import HandDetector
from xgboost import XGBClassifier
import time
import math



class BasicPublisher(Node):

    def __init__(self):  
        super().__init__('basic_publisher')
        self.motor = self.create_publisher(Twist, 'cmd_vel', 10)


    def pub_motor(self,vel_x,vel_z):
        cmd_vel = Twist()        
        cmd_vel.linear.x = vel_x
        cmd_vel.angular.z = vel_z
        self.motor.publish(cmd_vel)
        print(cmd_vel.linear.x, ' , ',cmd_vel.linear.z)  



def classify_hand(model_path, hand_point_list):
    model = XGBClassifier()
    model.load_model(model_path)
    try :
        pred = model.predict([hand_point_list])   
    except Exception as e:
        pred = ['fail']
    if pred[0] == 'incr':
        order = 'up'
    elif pred[0] == 'side':
        order = 'down'
    elif pred[0] == 'stab':
        order = 'D'
    elif pred[0] == 'back':
        order = 'R'
    else :
        order = 'D'

    return order



def mark_list(lmList):
  hand_point = []
  for landmrk in lmList:
    for i in range(len(landmrk)):
      hand_point.append(landmrk[i])

  return hand_point



def alpha_img(image,png,y,x):
    # 이미지의 가로길이 세로길이 가져온다. 
    rows_a, cols_a, channel = png.shape 
    # 입력받은 roi지정 
    roi = image[y:y + rows_a, x:x + cols_a] 

    # 마스크 만들기 
    pnggray = cv.cvtColor(png, cv.COLOR_BGR2GRAY) 
    ret, mask = cv.threshold(pnggray, 10, 255, cv.THRESH_BINARY) 
    mask_inv = cv.bitwise_not(mask) 
    # 0이면 그대로 두고 아니면 그대로 mask를 씌움 
    img1_bg = cv.bitwise_and(roi, roi, mask=mask_inv) 
    png_fg = cv.bitwise_and(png, png, mask=mask) 

    # 두 이미지를 더해서 검은 부분과 색이 있는 부분이 더해져서 없어짐
    dst = cv.add(img1_bg, png_fg)
    image[y:y + rows_a, x:x + cols_a] = dst
    return image



def main(args=None):

    rclpy.init(args=args)
    pub = BasicPublisher()
    
    cap = cv.VideoCapture(0)
    detector = HandDetector(detectionCon = 0.8, maxHands = 2)

    img1 = cv.imread('./66.png')
    img1 = cv.resize(img1, (200, 200))
    right = cv.imread('./right_arrow263x197.png')
    right = cv.resize(right, (130, 100))
    left = cv.imread('./left_arrow263x197.png')
    left = cv.resize(left, (130, 100))
    ppp = cv.imread('./ppp.png')
    ppp = cv.resize(ppp, (80, 80))
    rrr = cv.imread('./rrr.png')
    rrr = cv.resize(rrr, (80, 80))
    nnn = cv.imread('./nnn.png')
    nnn = cv.resize(nnn, (80, 80))
    ddd = cv.imread('./ddd.png')
    ddd = cv.resize(ddd, (80, 80))
    nono = cv.imread('./none.png')
    nono = cv.resize(nono, (80, 80))
    speedo = cv.imread('./speedometer495x271.png')
    speedo = cv.resize(speedo, (248, 136))
    needle = cv.imread('./needle165x166.png')
    speed_bar = cv.imread('./speed__bar.png')


    order = 'RAISE YOUR HAND TO START'
    rad = 0.0
    direction = 'straight'
    vel_x = 0.0
    delta_v = 0.01
    start = None
    lap_time = 0

    while cap.isOpened():
        success, img = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue
        img = cv.flip(img, 1)           # 480x640
        hands, image = detector.findHands(img)

        if hands:
            
            hand1 = hands[0]
            lmList1 = hand1["lmList"]

            del_x = 100
            if len(hands) == 2:
                if start == None:
                    start = time.time()

                hand2 = hands[1]
                lmList2 = hand2["lmList"]
                del_x = (lmList1[0][0]-lmList2[0][0])
                if del_x == 0 :
                    del_x = 0.01
                del_y = (lmList1[0][1]-lmList2[0][1])
                grad = -del_y / del_x
                
                rad = math.atan(grad)
    
                theta = rad*180/math.pi
                print("기울기 : ", grad, " 라디안 : ", rad, " 쎄타 : ", theta)
                rot = cv.getRotationMatrix2D((100,100), theta, 1)
                img2 = cv.warpAffine(img1,rot,(0,0))
                

                image = alpha_img(image,img2,250,240)
                
            
            hand_point = mark_list(lmList1)
            order = classify_hand('./xgb_class.model', hand_point) 
            if del_x > -100 and del_x <100 :
                order = 'P' 
            if rad <= 0.1 :
                direction = 'Right'
            elif rad >= -0.1 :
                direction = 'Left' 
            else:
                direction = 'Straight'
            

            if order == 'up' :   
                if vel_x < 0.4 :            # jetson nano는 4
                    vel_x += delta_v
                else : 
                    pass

            elif order == 'down' :
                if vel_x > -0.4 :           # jetson nano는 -4
                    vel_x -= delta_v
                else : 
                    pass

            elif order == 'P' :
                vel_x = 0.0
                rad = 0.0
                image =  alpha_img(image,ppp,380,540)

            elif order == 'R' :
                vel_x = -0.1                # jetson nano는 -0.2
                image =  alpha_img(image,rrr,380,540)

            if vel_x < 0 :
                rad *= -1 
            
        
        if direction == 'Right':
            arrow = right
        
        elif direction == 'Left':      
            arrow = left

        else :
            arrow = None

        try :
            image = alpha_img(image,arrow,10,240)

        except Exception as e:
            pass
        
        if vel_x :
            image =  alpha_img(image,speedo,289,5)

            theta = abs(vel_x)*-450         # jetson nano는 *-45
            rot = cv.getRotationMatrix2D((83,83), theta, 1)
            needle1 = cv.warpAffine(needle,rot,(0,0))
            image =  alpha_img(image,needle1,311,46)

        else :
            image =  alpha_img(image,speedo,289,5)
            image =  alpha_img(image,needle,311,46)


        if order == 'D':
            image =  alpha_img(image,ddd,380,540)
        elif order == None :
            image =  alpha_img(image,nono,380,540)
        
        image[425:480,5:248,:] = speed_bar

        if start :
            end = time.time()
            lap_time = end - start
            
        cv.putText(image, f"{40*vel_x:.1f} km/h", (20, 463), cv.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0), 1, cv.LINE_AA)
        cv.putText(image, f"{lap_time:.5f} sec", (15, 45), cv.FONT_HERSHEY_DUPLEX, 0.8, (0, 0, 0), 1, cv.LINE_AA)
        cv.imshow('Fantasy Driving', image)
        pub.pub_motor(vel_x,rad)

        if cv.waitKey(5) & 0xFF == 27:
            pub.pub_motor(0.0,0.0)
            break
    cap.release()



if __name__ == '__main__':
    main()