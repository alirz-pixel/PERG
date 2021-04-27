import mediapipe as mp
import PoseEstimationModule as pea
import numpy as np
import cv2

dict_PostAngle = {}
cap = cv2.VideoCapture(0)


with mp.solutions.holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    while cap.isOpened():
        _, frame = cap.read()
        white_img = cv2.imread('640x480-white-solid-color-background.jpg')

        image, white_img = pea.pose_estimation(frame, holistic, dict_PostAngle, white_img)

        cv2.imshow('Raw Webcam Feed', image)
        cv2.imshow('asdf', white_img)

        print(dict_PostAngle)


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()