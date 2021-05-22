'''
2021.05.01  10:24 기본적인 틀 작성 - 최문형
2021.05.01  10:25 ~ 2020.05.22  9:30 추가 동작 인식을 위한 거리 및 각도 추가 (이범석)

최문형 - 몸에 점들을 찍고, 그 점들에 대한 각도 및 거리 구현
이범석 - 추가된 운동동작에 필요한 각도 및 거리 구현
'''

import mediapipe as mp
import numpy as np
import math
import cv2

# 각도 계산을 위한 함수 (최문형)
def calculate_angle(a, b, c):
    a = np.array(a)  # First
    b = np.array(b)  # Mid
    c = np.array(c)  # End

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle



mp_pose = mp.solutions.pose
mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils

mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2)

# opencv의 frame을 입력받고 점들의 각도 및 거리 반환하는 함수 (최문형).
def pose_estimation(frame, holistic, dict_PoseAngle, dict_PoseLength, dict_PoseLower, white_img = 0):
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = holistic.process(image)

    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    try:
        landmarks = results.pose_landmarks.landmark

    except:
        pass

    # LeftElbow 각도 구하기 (최문형)
    try:
        LeftShoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        LeftElbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
        LeftWrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

        angle = calculate_angle(LeftShoulder, LeftElbow, LeftWrist)

        dict_PoseAngle['LeftElbow'] = angle

    except:
        dict_PoseAngle['LeftElbow'] = -1


    # RightElbow 각도 구하기 (최문형)
    try:
        RightShoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                        landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
        RightElbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                        landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
        RightWrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                     landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

        angle = calculate_angle(RightShoulder, RightElbow, RightWrist)

        dict_PoseAngle['RightElbow'] = angle

    except:
        dict_PoseAngle['RightElbow'] = -1


    # Leftshoulder 각도 구하기 (최문형)
    try:
        LeftElbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
        LeftShoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        LeftHip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                   landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]

        angle = calculate_angle(LeftElbow, LeftShoulder, LeftHip)

        dict_PoseAngle['LeftShoulder'] = angle

    except:
        dict_PoseAngle['LeftShoulder'] = -1


    # Rightshoulder 각도 구하기 (최문형)
    try:
        RightElbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                     landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
        RightShoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                        landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
        RightHip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                   landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]

        angle = calculate_angle(RightElbow, RightShoulder, RightHip)

        dict_PoseAngle['RightShoulder'] = angle

    except:
        dict_PoseAngle['RightShoulder'] = -1


    # LeftHip 각도 구하기 (최문형)
    try:
        LeftShoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        LeftHip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                   landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
        LeftKnee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                    landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]

        angle = calculate_angle(LeftShoulder, LeftHip, LeftKnee)

        dict_PoseAngle['LeftHip'] = angle

    except:
        dict_PoseAngle['LeftHip'] = -1


    # RightHip 각도 구하기 (최문형)
    try:
        RightShoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                        landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
        RightHip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                   landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
        RightKnee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                    landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]

        angle = calculate_angle(RightShoulder, RightHip, RightKnee)

        dict_PoseAngle['RightHip'] = angle

    except:
        dict_PoseAngle['RightHip'] = -1


    # Right_Knee 각도 구하기 (최문형)
    try:
        RightHip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                   landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
        RightKnee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                    landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
        RightAnkle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                      landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

        angle = calculate_angle(RightHip, RightKnee, RightAnkle)

        dict_PoseAngle['RightKnee'] = angle

    except:
        dict_PoseAngle['RightKnee'] = -1


    # Left_Knee 각도 구하기 (최문형)
    try:
        LeftHip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                   landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
        LeftKnee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                    landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
        LeftAnkle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                      landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

        angle = calculate_angle(LeftHip, LeftKnee, LeftAnkle)

        dict_PoseAngle['LeftKnee'] = angle

    except:
        dict_PoseAngle['LeftKnee'] = -1

    # LeftAnkle-Leftknee-RightAnkle 각도 구하기 (이범석)
    try:
        LeftAnkle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
        LeftKnee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                    landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
        RightAnkle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                   landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

        angle = calculate_angle(LeftAnkle, LeftKnee, RightAnkle)

        dict_PoseAngle['LA-LK-RA'] = angle

    except:
        dict_PoseAngle['LA-LK-RA'] = -1

    # RightAnkle-Rightknee-LeftAnkle 각도 구하기 (이범석)
    try:
        RightAnkle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                     landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
        RightKnee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                    landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
        LeftAnkle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                   landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

        angle = calculate_angle(RightAnkle, RightKnee, LeftAnkle)

        dict_PoseAngle['RA-RK-LA'] = angle

    except:
        dict_PoseAngle['RA-RK-LA'] = -1

    # LeftKnee-LeftHip-RightKnee 각도 구하기 (이범석)
    try:
        LeftKnee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                   landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
        LeftHip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
        RightKnee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                   landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]

        angle = calculate_angle(LeftKnee, LeftHip, RightKnee)

        dict_PoseAngle['LK-LH-RK'] = angle

    except:
        dict_PoseAngle['LK-LH-RK'] = -1

    # RightKnee-RightHip-LeftKnee 각도 구하기(이범석)
    try:
        RightKnee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                   landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
        RightHip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                     landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
        LeftKnee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                   landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]

        angle = calculate_angle(RightKnee, RightHip, LeftKnee)

        dict_PoseAngle['RK-RH-LK'] = angle

    except:
        dict_PoseAngle['RK-RH-LK'] = -1

    # LeftAnkle-LeftKnee-RightAnkle 각도 구하기 (이범석)
    try:
        LeftAnkle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                   landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
        LeftKnee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
        RightAnkle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                   landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

        angle = calculate_angle(LeftAnkle, LeftKnee, RightAnkle)

        dict_PoseAngle['LA-LK-RA'] = angle

    except:
        dict_PoseAngle['LA-LK-RA'] = -1

    # RightAnkle-RightKnee-LeftAnkle 각도 구하기 (이범석)
    try:
        RightAnkle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                   landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
        RightKnee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                     landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
        LeftAnkle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                   landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

        angle = calculate_angle(RightAnkle, RightKnee, LeftAnkle)

        dict_PoseAngle['RA-RK-LA'] = angle

    except:
        dict_PoseAngle['RA-RK-LA'] = -1

    # LeftWrist-RightWrist-LeftAnkle 각도 구하기, FBM-5 (이범석)
    try:
        LeftWrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                      landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
        RightWrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                     landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
        LeftAnkle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

        angle = calculate_angle(LeftWrist, RightWrist, LeftAnkle)

        dict_PoseAngle['LW-RW-LA'] = angle

    except:
        dict_PoseAngle['LW-RW-LA'] = -1

    # RightWrist-LeftWrist-RightAnkle 각도 구하기, FBM-5 (이범석)
    try:
        RightWrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                     landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
        LeftWrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                      landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
        RightAnkle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                     landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

        angle = calculate_angle(RightWrist, LeftWrist, RightAnkle)

        dict_PoseAngle['RW-LW-RA'] = angle

    except:
        dict_PoseAngle['RW-LW-RA'] = -1

    # LeftWrist-RightAnkle-LeftAnkle 각도 구하기, FBM-5 (이범석)
    try:
        LeftWrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                      landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
        RightAnkle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                     landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
        LeftAnkle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

        angle = calculate_angle(LeftWrist, RightAnkle, LeftAnkle)

        dict_PoseAngle['LW-RA-LA'] = angle

    except:
        dict_PoseAngle['LW-RA-LA'] = -1

    # RightWrist-LeftWrist-RightAnkle 각도 구하기, FBM-5 (이범석)
    try:
        RightWrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                     landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
        LeftAnkle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                      landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
        RightAnkle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                     landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

        angle = calculate_angle(RightWrist, LeftAnkle, RightAnkle)

        dict_PoseAngle['RW-LA-RA'] = angle

    except:
        dict_PoseAngle['RW-LA-RA'] = -1

    # RightWrist-LeftWrist-LeftAnkle 각도 구하기, FBM-6 (이범석)
    try:
        RightWrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                     landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
        LeftWrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                      landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
        LeftAnkle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

        angle = calculate_angle(RightWrist, LeftWrist, LeftAnkle)

        dict_PoseAngle['RW-LW-LA'] = angle

    except:
        dict_PoseAngle['RW-LW-LA'] = -1

    # LeftWrist-RightWrist-RightAnkle 각도 구하기, FBM-6 (이범석)
    try:
        LeftWrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
        RightWrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                      landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
        RightAnkle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                     landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

        angle = calculate_angle(LeftWrist, RightWrist, RightAnkle)

        dict_PoseAngle['LW-RW-RA'] = angle

    except:
        dict_PoseAngle['LW-RW-RA'] = -1

    # RightWrist-RightAnkle-LeftAnkle 각도 구하기, FBM-6 (이범석)
    try:
        RightWrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                     landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
        RightAnkle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                      landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
        LeftAnkle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

        angle = calculate_angle(RightWrist, RightAnkle, LeftAnkle)

        dict_PoseAngle['RW-RA-LA'] = angle

    except:
        dict_PoseAngle['RW-RA-LA'] = -1

    # LeftWrist-RightAnkle-RightAnkle 각도 구하기, FBM-6 (이범석)
    try:
        LeftWrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
        LeftAnkle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                      landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
        RightAnkle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                     landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

        angle = calculate_angle(LeftWrist, LeftAnkle, RightAnkle)

        dict_PoseAngle['LW-LA-RA'] = angle

    except:
        dict_PoseAngle['LW-LA-RA'] = -1

    # LeftHip-RightHip-RightKnee 각도 구하기(이범석)
    try:
        LeftHip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
        RightHip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                      landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
        RightKnee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                     landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]

        angle = calculate_angle(LeftHip, RightHip, RightKnee)

        dict_PoseAngle['LH-RH-RK'] = angle

    except:
        dict_PoseAngle['LH-RH-RK'] = -1

    # RightHip-LeftHip-LeftKnee 각도 구하기(이범석)
    try:
        RightHip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                      landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
        LeftHip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
        LeftKnee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]

        angle = calculate_angle(RightHip, LeftHip, LeftKnee)

        dict_PoseAngle['RH-LH-LK'] = angle

    except:
        dict_PoseAngle['RH-LH-LK'] = -1


    # 16번과 14번 사이 거리 구하기 (최문형)
    try:
        RightWrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                      landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
        RightElbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                      landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]


        length = math.hypot(RightElbow[0] - RightWrist[0], RightElbow[1] - RightWrist[1]) * 100

        dict_PoseLength['16, 14'] = length

    except:
        dict_PoseLength['16, 14'] = -1


    # 14번과 12번 사이 거리 구하기 (최문형)
    try:
        RightElbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                      landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
        RightShoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                         landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]


        length = math.hypot(RightShoulder[0] - RightElbow[0], RightShoulder[1] - RightElbow[1]) * 100

        dict_PoseLength['14, 12'] = length

    except:
        dict_PoseLength['14, 12'] = -1


    # 24번과 12번 사이 거리 구하기 (최문형)
    try:
        RightShoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                         landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
        RightHip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                    landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]


        length = math.hypot(RightHip[0] - RightShoulder[0], RightHip[1] - RightShoulder[1]) * 100

        dict_PoseLength['24, 12'] = length

    except:
        dict_PoseLength['24, 12'] = -1


    # 26번과 24번 사이 거리 구하기 (최문형)
    try:
        RightHip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                    landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
        RightKnee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                     landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]


        length = math.hypot(RightKnee[0] - RightHip[0], RightKnee[1] - RightHip[1]) * 100

        dict_PoseLength['26, 24'] = length

    except:
        dict_PoseLength['26, 24'] = -1


    # 28번과 26번 사이 거리 구하기 (최문형)
    try:
        RightKnee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                     landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
        RightAnkle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                      landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]


        length = math.hypot(RightAnkle[0] - RightKnee[0], RightAnkle[1] - RightKnee[1]) * 100

        dict_PoseLength['28, 26'] = length

    except:
        dict_PoseLength['28, 26'] = -1



    # 15번과 13번 사이 거리 구하기 (최문형)
    try:
        LeftWrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
        LeftElbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                      landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]


        length = math.hypot(LeftElbow[0] - LeftWrist[0], LeftElbow[1] - LeftWrist[1]) * 100

        dict_PoseLength['15, 13'] = length

    except:
        dict_PoseLength['15, 13'] = -1


    # 13번과 11번 사이 거리 구하기 (최문형)
    try:
        LeftElbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                      landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
        LeftShoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]


        length = math.hypot(LeftShoulder[0] - LeftElbow[0], LeftShoulder[1] - LeftElbow[1]) * 100

        dict_PoseLength['13, 11'] = length

    except:
        dict_PoseLength['13, 11'] = -1


    # 23번과 11번 사이 거리 구하기 (최문형)
    try:
        LeftShoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        LeftHip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                   landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]


        length = math.hypot(LeftHip[0] - LeftShoulder[0], LeftHip[1] - LeftShoulder[1]) * 100

        dict_PoseLength['23, 11'] = length

    except:
        dict_PoseLength['23, 11'] = -1


    # 25번과 23번 사이 거리 구하기 (최문형)
    try:
        LeftHip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                   landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
        LeftKnee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                    landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]


        length = math.hypot(LeftKnee[0] - LeftHip[0], LeftKnee[1] - LeftHip[1]) * 100

        dict_PoseLength['25, 23'] = length

    except:
        dict_PoseLength['25, 23'] = -1

    # 27번과 25번 사이 거리 구하기 (최문형)
    try:
        LeftKnee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
        LeftAnkle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                      landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]


        length = math.hypot(LeftAnkle[0] - LeftKnee[0], LeftAnkle[1] - LeftKnee[1]) * 100

        dict_PoseLength['27, 25'] = length

    except:
        dict_PoseLength['27, 25'] = -1

    # 15번과 11번 사이 거리 구하기 (이범석)
    try:
        LeftWrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
        LeftShoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                      landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]


        length = math.hypot(LeftShoulder[0] - LeftWrist[0], LeftShoulder[1] - LeftWrist[1]) * 100

        dict_PoseLength['15, 11'] = length

    except:
        dict_PoseLength['15, 11'] = -1

    # 16번과 12번 사이 거리 구하기 (이범석)
    try:
        RightWrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                     landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
        RightShoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                      landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]


        length = math.hypot(RightShoulder[0] - RightWrist[0], RightShoulder[1] - RightWrist[1]) * 100

        dict_PoseLength['16, 12'] = length

    except:
        dict_PoseLength['16, 12'] = -1

    # 12번과 11번 사이 거리 구하기 (이범석)
    try:
        LeftShoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        RightShoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                      landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]


        length = math.hypot(RightShoulder[0] - LeftShoulder[0], RightShoulder[1] - LeftShoulder[1]) * 100

        dict_PoseLength['12, 11'] = length

    except:
        dict_PoseLength['12, 11'] = -1

    # 16번과 15번 사이 거리 구하기 (이범석)
    try:
        LeftWrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
        RightWrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                      landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]


        length = math.hypot(RightWrist[0] - LeftWrist[0], RightWrist[1] - LeftWrist[1]) * 100

        dict_PoseLength['16, 15'] = length

    except:
        dict_PoseLength['16, 15'] = -1

    # 14번과 13번 사이 거리 구하기 (이범석)
    try:
        LeftElbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
        RightElbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                      landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]


        length = math.hypot(RightElbow[0] - LeftElbow[0], RightElbow[1] - LeftElbow[1]) * 100

        dict_PoseLength['14, 13'] = length

    except:
        dict_PoseLength['14, 13'] = -1

    # 24번과 23번 사이 거리 구하기 (이범석)
    try:
        RightHip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                    landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
        LeftHip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                   landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]

        length = math.hypot(RightHip[0] - LeftHip[0], RightHip[1] - LeftHip[1]) * 100

        dict_PoseLength['24, 23'] = length

    except:
        dict_PoseLength['24, 23'] = -1

    # 26번과 25번 사이 거리 구하기 (이범석)
    try:
        RightKnee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                     landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
        LeftKnee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                      landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]


        length = math.hypot(RightKnee[0] - LeftKnee[0], RightKnee[1] - LeftKnee[1]) * 100

        dict_PoseLength['26, 25'] = length

    except:
        dict_PoseLength['26, 25'] = -1

    # 28번과 27번 사이 거리 구하기 (이범석)
    try:
        RightAnkle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                     landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
        LeftAnkle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                      landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]


        length = math.hypot(RightAnkle[0] - LeftAnkle[0], RightAnkle[1] - LeftAnkle[1]) * 100

        dict_PoseLength['28, 27'] = length

    except:
        dict_PoseLength['28, 27'] = -1

    # 26번과 16번 사이 거리 구하기 (이범석)
    try:
        RightKnee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                     landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
        RightWrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                      landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]


        length = math.hypot(RightKnee[0] - RightWrist[0], RightKnee[1] - RightWrist[1]) * 100

        dict_PoseLength['26, 16'] = length

    except:
        dict_PoseLength['26, 16'] = -1

    # 26번과 15번 사이 거리 구하기 (이범석)
    try:
        RightKnee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                     landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
        LeftWrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                      landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]


        length = math.hypot(RightKnee[0] - LeftWrist[0], RightKnee[1] - LeftWrist[1]) * 100

        dict_PoseLength['26, 15'] = length

    except:
        dict_PoseLength['26, 15'] = -1

    # 25번과 16번 사이 거리 구하기 (이범석)
    try:
        LeftKnee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
        RightWrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                      landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]


        length = math.hypot(LeftKnee[0] - RightWrist[0], LeftKnee[1] - RightWrist[1]) * 100

        dict_PoseLength['25, 16'] = length

    except:
        dict_PoseLength['25, 16'] = -1

    # 25번과 15번 사이 거리 구하기 (이범석)
    try:
        LeftKnee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
        LeftWrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                      landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]


        length = math.hypot(LeftKnee[0] - LeftWrist[0], LeftKnee[1] - LeftWrist[1]) * 100

        dict_PoseLength['25, 15'] = length

    except:
        dict_PoseLength['25, 15'] = -1

    # 23번과 15번 사이 거리 구하기 (이범석)
    try:
        LeftHip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
        LeftWrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                      landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]


        length = math.hypot(LeftHip[0] - LeftWrist[0], LeftHip[1] - LeftWrist[1]) * 100

        dict_PoseLength['23, 15'] = length

    except:
        dict_PoseLength['23, 15'] = -1

    # 24번과 16번 사이 거리 구하기 (이범석)
    try:
        RightHip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
        RightWrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                      landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]


        length = math.hypot(RightHip[0] - RightWrist[0], RightHip[1] - RightWrist[1]) * 100

        dict_PoseLength['24, 16'] = length

    except:
        dict_PoseLength['24, 16'] = -1

    # 25번과 13번 사이 거리 구하기 (이범석)
    try:
        LeftElbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
        LeftKnee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                    landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]

        length = math.hypot(LeftElbow[0] - LeftKnee[0], LeftElbow[1] - LeftKnee[1]) * 100

        dict_PoseLength['25, 13'] = length

    except:
        dict_PoseLength['25, 13'] = -1

    # 26번과 14번 사이 거리 구하기 (이범석)
    try:
        RightElbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                      landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
        RightKnee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                     landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]

        length = math.hypot(RightElbow[0] - RightKnee[0], RightElbow[1] - RightKnee[1]) * 100
        
        dict_PoseLength['26, 14'] = length

    except:
        dict_PoseLength['26, 14'] = -1

    #완전히 허리를 숙였는지 인식(05.15 이범석)
    try:
        Shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y,
                    landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
        Hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y,
                    landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
        if Shoulder[0] <= Hip[0] or Shoulder[0] <= Hip[1] or Shoulder[1] <= Hip[0] or Shoulder[1] <= Hip[1]:
            dict_PoseLower['Waist'] = 1
        else:
            dict_PoseLower['Waist'] = 0
    except:
        dict_PoseLower['Waist'] = -1

    #양손이 어깨보다 위인지 인식(05.15 이범석)
    try:
        Wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y,
                    landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
        Shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y,
                    landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
        #양손이 어깨 위
        if Wrist[0] <= Shoulder[0] and Wrist[0] <= Shoulder[1] and Wrist[1] <= Shoulder[0] and Wrist[1] <= Shoulder[1]:
            dict_PoseLower['Wrist'] = 0
        #양손이 어깨 아래
        else:
            dict_PoseLower['Wrist'] = 1
    except:
        dict_PoseLower['Wrist'] = -1



    return image, white_img
