import cv2
import mediapipe as mp
import pandas as pd
import time


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands


# order = "incr"
# order = "decr"
order = "back"
# order = "stab"

# For webcam input:
cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:

  hand_data = pd.DataFrame(index=range(0,0), columns=['0.x','0.y','1.x','1.y','2.x','2.y',
  '3.x','3.y','4.x','4.y','5.x','5.y','6.x','6.y','7.x','7.y','8.x','8.y','9.x','9.y',
  '10.x','10.y','11.x','11.y','12.x','12.y','13.x','13.y','14.x','14.y','15.x','15.y',
  '16.x','16.y','17.x','17.y','18.x','18.y','19.x','19.y','20.x','20.y','order'])
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)
    image_height, image_width, _ = image.shape

    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:

      for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
        mp_drawing.draw_landmarks(
            image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())

        hand_list = []
        for landmrk in hand_landmarks.landmark:
          hand_list.append(landmrk.x*image_width)
          hand_list.append(landmrk.y*image_height)
        hand_list.append(order)
        print(hand_list)
      hand_data.loc[len(hand_data)] = hand_list

      # Flip the image horizontally for a selfie-view display.
    text = "up down back sta"
    cv2.putText(image, text, (50, 100), cv2.FONT_HERSHEY_DUPLEX, 1.2, (0, 0, 255), 1, cv2.LINE_AA)
    cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(5) & 0xFF == 27:
      now = time.strftime("%H%M")
      hand_data.to_csv('./hand'+ order + now +'.csv',mode='a', index=False)
      break
cap.release()

