'''
2021.05.01  10:24 기본적인 틀 작성 - 최문형
2021.05.01  10:25 ~ 2021.05.15  20:30  - 이범석
2021.05.15  20:31 상체 인식률 개선 - (최문형, 이범석)
2021.05.20~21  14:30 ~ 2:30 인식률 개선 및 동작 추가 - (이범석,최문형)
'''

import threading
import time

import mediapipe as mp
import PoseEstimationModule as pea
import cv2


dict_PoseAngle = {}
dict_PoseLength = {}
dict_PoseLower = {}
cap = cv2.VideoCapture(0)

#(상체, 하체, 전신 구분함수 05.15 이범석)
def UpperBody():
    # 기본 기립자세 인식 (이범석)
    if dict_PoseLength['23, 15'] <= 7.5 and dict_PoseLength['24, 16'] <= 7.5:
        if dict_PoseLength['12, 11'] >= dict_PoseLength['26, 25']:
            if dict_PoseAngle['LeftHip'] >= 165 and dict_PoseAngle['RightHip'] >= 165:
                if dict_PoseAngle['LeftKnee'] >= 165 and dict_PoseAngle['RightKnee'] >= 165:
                    print('standing')
                    return 'standing'

    # big clap 인식 (이범석, 최문형)
    if 88.9851 * 0.56 <= dict_PoseAngle['LeftShoulder'] <= 88.9851 * 1.25 and \
       88.9851 * 0.56 <= dict_PoseAngle['RightShoulder'] <= 88.9851 * 1.25:
        if dict_PoseLength['16, 15'] / dict_PoseLength['12, 11'] >= 3.4:
            if 130 <= dict_PoseAngle['LeftElbow'] and 130 <= dict_PoseAngle['RightElbow']:
                print('big clap-1')
                return 'big clap-1'

    if (dict_PoseAngle['LeftShoulder'] <= 50 and dict_PoseAngle['RightShoulder'] <= 50) and \
        (dict_PoseLength['16, 15'] / dict_PoseLength['12, 11'] <= 1.4):
        if dict_PoseLength['15, 11'] / dict_PoseLength['12, 11'] <= 0.5 and dict_PoseLength['16, 12'] / dict_PoseLength['12, 11'] <= 0.5:
            print('big clap-2')
            return 'big clap-2'

    # chest fly 인식 (이범석, 최문형)
    if dict_PoseLower['Wrist'] == 0:
        if 70 <= dict_PoseAngle['LeftShoulder'] <= 110 and 70 <= dict_PoseAngle['RightShoulder'] <= 110:
            if 55 <= dict_PoseAngle['LeftElbow'] <= 105 and 55 <= dict_PoseAngle['RightElbow'] <= 105:
                print('chestfly-1')
                return('chestfly-1')

    if dict_PoseLength['14, 13'] / dict_PoseLength['12, 11'] <= 1.2 and \
            dict_PoseLength['16, 15'] / dict_PoseLength['12, 11'] >= 0.1:
        if dict_PoseLower['Wrist'] == 0:
            print('chestfly-2')
            return 'chestfly-2'

    # 프론트 & 백레이즈 (이범석)
    if dict_PoseLength['16, 15'] / dict_PoseLength['12, 11'] >= 2:
        if dict_PoseAngle['RightElbow'] >= 140 and dict_PoseAngle['LeftElbow'] >= 140:
            if dict_PoseAngle['RightShoulder'] >= 90 and 20 <= dict_PoseAngle['LeftShoulder'] <= 60:
                print('Left-Front&BackRaise')
                return 'Left-Front&BackRaise'

    if dict_PoseLength['16, 15'] / dict_PoseLength['12, 11'] >= 2:
        if dict_PoseAngle['LeftElbow'] >= 140 and dict_PoseAngle['RightElbow'] >= 140:
            if dict_PoseAngle['LeftShoulder'] >= 90 and 20 <= dict_PoseAngle['RightShoulder'] <= 60:
                print('Right-Front&BackRaise')
                return 'Right-Front&BackRaise'
def LowerBody():
    # 기본 기립자세 인식 (이범석)
    if dict_PoseLength['23, 15'] <= 7.5 and dict_PoseLength['24, 16'] <= 7.5:
        if dict_PoseLength['12, 11'] >= dict_PoseLength['26, 25']:
            if dict_PoseAngle['LeftHip'] >= 165 and dict_PoseAngle['RightHip'] >= 165:
                if dict_PoseAngle['LeftKnee'] >= 165 and dict_PoseAngle['RightKnee'] >= 165:
                    print('standing')
                    return 'standing'
                
    # 스쿼트 인식 (이범석)
    if 0.4 <= dict_PoseLength['26, 24'] / dict_PoseLength['28, 26'] <= 0.9 \
            and 0.4 <= dict_PoseLength['25, 23'] / dict_PoseLength['27, 25'] <= 0.9:
        print('squat-1')
        return 'squat-1'

    # 런지 인식 (이범석, 최문형)
    if (dict_PoseAngle['LeftKnee'] <= 120 and dict_PoseAngle['RightKnee'] >= 105):
        if dict_PoseAngle['LA-LK-RA'] >= 135:
            print('lunge')
            return 'lunge'
    if (dict_PoseAngle['RightKnee'] <= 120 and dict_PoseAngle['LeftKnee'] >= 105):
        if dict_PoseAngle['RA-RK-LA'] >= 135:
            print('lunge')
            return 'lunge'

    # Side KneeLift 인식 (이범석)
    if (dict_PoseAngle['LeftKnee'] <= 105 and dict_PoseAngle['RightKnee'] >= 160) and \
        dict_PoseAngle['RightHip'] >= 160:
        print('R-KneeLift')
        return 'R-KneeLift'
    if (dict_PoseAngle['RightKnee'] <= 105 and dict_PoseAngle['LeftKnee'] >= 160) and \
        dict_PoseAngle['LeftHip'] >= 160:
        print('L-KneeLift')
        return 'L-KneeLift'


def FullBody():
    # 기본 기립자세 인식 (이범석)
    if dict_PoseLength['23, 15'] <= 7.5 and dict_PoseLength['24, 16'] <= 7.5:
        if dict_PoseLength['12, 11'] >= dict_PoseLength['26, 25']:
            if dict_PoseAngle['LeftHip'] >= 165 and dict_PoseAngle['RightHip'] >= 165:
                if dict_PoseAngle['LeftKnee'] >= 165 and dict_PoseAngle['RightKnee'] >= 165:
                    print('standing')
                    return 'standing'
                
    # Full-Body Motion 1-R
    if 50 <= dict_PoseAngle['LeftElbow'] <= 125 and dict_PoseAngle['RightElbow'] >= 150:
        if 60 <= dict_PoseAngle['RightShoulder'] <= 120 and dict_PoseAngle['LeftShoulder'] <= 50:
            if 15 <= dict_PoseAngle['RA-RK-LA'] <= 90:
                if 140 <= dict_PoseAngle['LeftHip'] and 140 <= dict_PoseAngle['RightHip']:
                    if 40 <= dict_PoseAngle['RH-LH-LK'] <= 90 and 40 <= dict_PoseAngle['LH-RH-RK'] <= 90:
                        if dict_PoseLength['26, 25'] / dict_PoseLength['24, 23'] <= 1.5:
                            print('Full-Body Motion 1-R')
                            return 'Full-Body Motion 1-R'
    # Full-Body Motion 1-L
    if dict_PoseAngle['RightElbow'] <= 125 and dict_PoseAngle['LeftElbow'] >= 150:
        if 60 <= dict_PoseAngle['LeftShoulder'] <= 120 and dict_PoseAngle['RightShoulder'] <= 50:
            if 15 <= dict_PoseAngle['LA-LK-RA'] <= 90:
                if 140 <= dict_PoseAngle['LeftHip'] and 140 <= dict_PoseAngle['RightHip']:
                    if 40 <= dict_PoseAngle['LH-RH-RK'] <= 90 and 40 <= dict_PoseAngle['RH-LH-LK'] <= 90:
                        if dict_PoseLength['26, 25'] / dict_PoseLength['24, 23'] <= 1.5:
                            print('Full-Body Motion 1-L')
                            return 'Full-Body Motion 1-L'

    # Full-Body Motion 2 (이범석, 최문형)
    if 150 <= dict_PoseAngle['LeftShoulder'] and 150 <= dict_PoseAngle['RightShoulder']:
        if 140 <= dict_PoseAngle['LeftElbow'] and 140 <= dict_PoseAngle['RightElbow']:
            if 110 <= dict_PoseAngle['LeftKnee'] <= 150 and 110 <= dict_PoseAngle['RightKnee'] <= 150:
                if 110 <= dict_PoseAngle['LeftHip'] <= 150 and 110 <= dict_PoseAngle['RightHip'] <= 150:
                    print('Full-Body Motion 2')
                    return 'Full-Body Motion 2'

    # Full-Body Motion 3 (이범석)
    if dict_PoseLower['Wrist'] == 0:
        if 2.25 <= dict_PoseLength['16, 15'] / dict_PoseLength['12, 11'] <= 3.5 and 1.75 <= dict_PoseLength['14, 13'] / \
                dict_PoseLength['12, 11'] <= 3:
            if 1.3 <= dict_PoseLength['28, 27'] / dict_PoseLength['12, 11'] <= 2.55 and \
                    1.05 <= dict_PoseLength['26, 25'] / dict_PoseLength['12, 11'] <= 2.3:
                if (dict_PoseAngle['LeftHip'] >= 150 and dict_PoseAngle['RightHip'] >= 150) and \
                        (dict_PoseAngle['LeftElbow'] >= 150 and dict_PoseAngle['RightElbow'] >= 150) and \
                        (dict_PoseAngle['LeftKnee'] >= 150 and dict_PoseAngle['RightKnee'] >= 150):
                    print('Full-Body Motion 3')
                    return 'Full-Body Motion 3'

    # Full-Body Motion 4-L (이범석, 최문형)
    if dict_PoseLength['26, 14'] / dict_PoseLength['24, 23'] <= 2:
        if dict_PoseAngle['RightElbow'] <= 65 and dict_PoseAngle['LeftElbow'] <= 65:
            if dict_PoseAngle['LeftShoulder'] >= 105 and 30 <= dict_PoseAngle['RightShoulder'] <= 85:
                if dict_PoseAngle['LeftKnee'] >= 160 and 30 <= dict_PoseAngle['RightKnee'] < 115:
                    if 30 <= dict_PoseAngle['RightHip'] <= 110 and 150 <= dict_PoseAngle['LeftHip']:
                        print('FBM 4-L')
                        return 'FBM 4-L'
    # Full-Body Motion 4-R (이범석, 최문형)
    if dict_PoseLength['25, 13'] / dict_PoseLength['24, 23'] <= 2:
        if dict_PoseAngle['LeftElbow'] <= 65 and dict_PoseAngle['RightElbow'] <= 65:
            if dict_PoseAngle['RightShoulder'] >= 105 and 30 <= dict_PoseAngle['LeftShoulder'] <= 85:
                if dict_PoseAngle['RightKnee'] >= 160 and 30 <= dict_PoseAngle['LeftKnee'] < 115:
                    if 30 <= dict_PoseAngle['LeftHip'] <= 110 and 150 <= dict_PoseAngle['RightHip']:
                        print('FBM 4-R')
                        return 'FBM 4-R'

    # Full-Body Motion 5-R (이범석, 최문형)
    if dict_PoseLength['16, 15'] / dict_PoseLength['12, 11'] >= 3.5:
        if 96.0691 * 0.85 <= dict_PoseAngle['LW-RW-LA'] <= 96.0691 * 1.15 and dict_PoseAngle['RW-LW-RA'] <= 10:
            if dict_PoseAngle['LeftKnee'] >= 145 and dict_PoseAngle['RightKnee'] >= 145:
                if dict_PoseLength['28, 27'] / dict_PoseLength['24, 23'] >= 3.5:
                    if dict_PoseAngle['LeftHip'] >= 130 and dict_PoseAngle['RightHip'] <= 90:
                        print('FBM 5-R')
                        return 'FBM 5-R'
    # Full-Body Motion 5-L (이범석, 최문형)
    if dict_PoseLength['16, 15'] / dict_PoseLength['12, 11'] >= 3.5:
        if 75 <= dict_PoseAngle['RW-LW-RA'] <= 105 and dict_PoseAngle['LW-RW-LA'] <= 10:
            if dict_PoseAngle['LeftKnee'] >= 145 and dict_PoseAngle['RightKnee'] >= 145:
                if dict_PoseLength['28, 27'] / dict_PoseLength['24, 23'] >= 3.5:
                    if dict_PoseAngle['RightHip'] >= 130 and dict_PoseAngle['LeftHip'] <= 90:
                        print('FBM 5-L')
                        return 'FBM 5-L'


# 리듬게임에 반환할 동작을 위해 동작 인식 모듈로 입력값을 넣어주는 함수 (최문형)
def Func_GetUpperPose(frame, holistic):
    pea.pose_estimation(frame, holistic, dict_PoseAngle, dict_PoseLength, dict_PoseLower)
    return UpperBody()


# 리듬게임과 병합하기 전 사용되었던 main 함수 (최문형)
def main():
    with mp.solutions.holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        while cap.isOpened():
            _, frame = cap.read()
            white_img = cv2.imread('640x480-white-solid-color-background.jpg')
            frame = cv2.flip(frame, 1)

            image, white_img = pea.pose_estimation(frame, holistic, dict_PoseAngle, dict_PoseLength, dict_PoseLower, white_img)

            cv2.imshow('Cam Bg Pose Estimation', image)
            cv2.imshow('White Bg Pose Estimation', white_img)

            #UpperBody()
            #LowerBody()
            FullBody()

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()



# 최문형
def printDict():
    # 여기서 오류난 동작을 출력시켜준다. (오류날 때마다 작성)
    pass


# 현재 오류난 동작을 확인하기 위한 코드 (최문형)
def Pose_Test():
    threading.Timer(6, printDict).start()
    threading.Timer(6 + 3, printDict).start()
    threading.Timer(6 + 6, printDict).start()
    threading.Timer(6 + 9, printDict).start()
    threading.Timer(6 + 12, printDict).start()
    threading.Timer(6 + 15, printDict).start()
    threading.Timer(6 + 18, printDict).start()

    with mp.solutions.holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        while cap.isOpened():
            _, frame = cap.read()
            white_img = cv2.imread('640x480-white-solid-color-background.jpg')

            frame = cv2.flip(frame, 1)

            image, white_img = pea.pose_estimation(frame, holistic, dict_PoseAngle, dict_PoseLength, dict_PoseLower,
                                                   white_img)

            cv2.imshow('Cam Bg Pose Estimation', image)
            cv2.imshow('White Bg Pose Estimation', white_img)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

#main()

#Pose_Test()
