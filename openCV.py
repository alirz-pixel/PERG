import mediapipe as mp
import PoseEstimationModule as pea
import numpy as np
import cv2
import win32api

dict_PoseAngle = {}
dict_PoseLength = {}
cap = cv2.VideoCapture(0)
state_bigclap = 0
state_skip = 0
state_ChestFly = 0

with mp.solutions.holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    while cap.isOpened():
        _, frame = cap.read()
        white_img = cv2.imread('640x480-white-solid-color-background.jpg')

        image, white_img = pea.pose_estimation(frame, holistic, dict_PoseAngle, dict_PoseLength,  white_img)

        cv2.imshow('Cam Bg Pose Estimation', image)
        cv2.imshow('White Bg Pose Estimation', white_img)
        
        #스쿼트 인식
        if 0.4 <= dict_PoseLength['26, 24'] / dict_PoseLength['28, 26'] <= 0.8 \
                and 0.4 <= dict_PoseLength['25, 23'] / dict_PoseLength['27, 25'] <= 0.8:
            print("squat")

        #if 1.1 <= dict_PoseLength['26, 24'] / dict_PoseLength['28, 26'] \
        #        and 1.1 <= dict_PoseLength['25, 23'] / dict_PoseLength['27, 25']:
        
        #런지 인식
        if (dict_PoseAngle['LeftKnee'] <= 95 and dict_PoseAngle['RightKnee'] >= 105) or\
                (dict_PoseAngle['RightKnee'] <= 95 and dict_PoseAngle['LeftKnee'] >= 105):
            if dict_PoseAngle['LA-LK-RA'] >= 145 or dict_PoseAngle['RA-RK-LA'] >= 145:
                print('lunge')

        #KneeLift 인식
        if ((dict_PoseAngle['LeftKnee'] <= 105 and dict_PoseAngle['RightKnee'] >= 160)
            or (dict_PoseAngle['RightKnee'] <= 105 and dict_PoseAngle['LeftKnee'] >= 160))\
                and(dict_PoseAngle['LeftHip'] >= 160 or dict_PoseAngle['RightHip'] >= 160):
            print('KneeLift')

        #big clap 인식
        if state_bigclap == 0:
             if (55 <= dict_PoseAngle['LeftShoulder'] <= 90 and 55 <= dict_PoseAngle['RightShoulder'] <= 90) and\
                     (dict_PoseLength['16, 15'] / dict_PoseLength['12, 11'] >= 3):
                 state_bigclap = 1

        if state_bigclap != 0:
             if (dict_PoseAngle['LeftShoulder'] <= 50 and dict_PoseAngle['RightShoulder'] <= 50) and\
                     (dict_PoseLength['16, 15'] / dict_PoseLength['12, 11'] <= 1):
                 state_bigclap = 0
                 print('big clap')

        #chest fly 인식
        if state_ChestFly == 0:
            if 70 <= dict_PoseAngle['LeftShoulder'] <= 105 and 70 <= dict_PoseAngle['RightShoulder'] <= 105:
                if 55 <= dict_PoseAngle['LeftElbow'] <= 100 and 55 <= dict_PoseAngle['RightElbow'] <= 100:
                    state_ChestFly = 1
        if state_ChestFly != 0:
            if dict_PoseLength['14, 13'] / dict_PoseLength['12, 11'] <= 1.2 and dict_PoseLength['16, 15'] / dict_PoseLength['12, 11'] >= 0.15:
                print('chestfly')
                state_ChestFly = 0

        #프론트 & 백레이즈
        if dict_PoseLength['16, 15'] / dict_PoseLength ['12, 11'] >= 2:
            if dict_PoseAngle['RightElbow'] >= 140 and dict_PoseAngle['LeftElbow'] >= 140:
                if dict_PoseAngle['RightShoulder'] >= 90 and 20 <= dict_PoseAngle['LeftShoulder'] <= 60:
                    print('Right-Front&BackRaise')
        if dict_PoseLength['16, 15'] / dict_PoseLength ['12, 11'] >= 2:
            if dict_PoseAngle['LeftElbow'] >= 140 and dict_PoseAngle['RightElbow'] >= 140:
                if dict_PoseAngle['LeftShoulder'] >= 90 and 20 <= dict_PoseAngle['RightShoulder'] <= 60:
                    print('Left-Front&BackRaise')

        #Full-Body Motion 1-R
        if dict_PoseAngle['LeftElbow'] <= 110 and dict_PoseAngle['RightElbow'] >= 150:
            if dict_PoseAngle['RightShoulder'] >= 80 and dict_PoseAngle['LeftShoulder'] <= 50:
                if 20 <= dict_PoseAngle ['RA-RK-LA'] <= 70:
                    print('Full-Body Motion 1-R')
        #Full-Body Motion 1-L
        if dict_PoseAngle['RightElbow'] <= 110 and dict_PoseAngle['LeftElbow'] >= 150:
            if dict_PoseAngle['LeftShoulder'] >= 80 and dict_PoseAngle['RightShoulder'] <= 50:
                if 20 <= dict_PoseAngle ['LA-LK-RA'] <= 70:
                    print('Full-Body Motion 1-L')

        #Full-Body Motion 2-R
        if 70 <= dict_PoseAngle['RightKnee'] <= 110 and dict_PoseAngle['LeftKnee'] >= 150:
            if 70 <= dict_PoseAngle['RightHip'] <= 110 and dict_PoseAngle['LeftHip'] >= 150 and\
                    70 <= dict_PoseAngle['LeftElbow'] <= 110:
                print('Full-Body Motion 2-R')
        #Full-Body Motion 2-L
        if 70 <= dict_PoseAngle['LeftKnee'] <= 110 and dict_PoseAngle['RightKnee'] >= 150:
            if 70 <= dict_PoseAngle['LeftHip'] <= 110 and dict_PoseAngle['RightHip'] >= 150 and\
                    70 <= dict_PoseAngle['RightElbow'] <= 110:
                print('Full-Body Motion 2-L')

        #Full-Body Motion 3
        if 2.25 <=dict_PoseLength['16, 15'] / dict_PoseLength['12, 11'] <= 3.5 and 1.75 <= dict_PoseLength['14, 13'] / dict_PoseLength['12, 11'] <= 3:
            if 1.3 <= dict_PoseLength['28, 27'] / dict_PoseLength['12, 11'] <= 2.55 and 1.05 <= dict_PoseLength['26, 25'] / dict_PoseLength['12, 11'] <= 2.3:
                if (dict_PoseAngle['LeftHip'] >= 150 and dict_PoseAngle['RightHip'] >= 150) and\
                        (dict_PoseAngle['LeftElbow'] >= 150 and dict_PoseAngle['RightElbow'] >= 150) and\
                        (dict_PoseAngle['LeftKnee'] >= 150 and dict_PoseAngle['RightKnee'] >= 150):
                    print('Full-Body Motion 3')

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


cap.release()
cv2.destroyAllWindows()
