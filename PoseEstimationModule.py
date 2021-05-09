import mediapipe as mp
import numpy as np
import math
import cv2

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

# opencv의 frame을 넘겨받아야 함.
def pose_estimation(frame, holistic, dict_PoseAngle, dict_PoseLength, white_img):
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = holistic.process(image)

    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=4),
                                  mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                                  )

    mp_drawing.draw_landmarks(white_img, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                              mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=4),
                              mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                              )

    try:
        landmarks = results.pose_landmarks.landmark

    except:
        pass


    # LeftElbow 각도 구하기
    try:
        LeftShoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        LeftElbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
        LeftWrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

        angle = calculate_angle(LeftShoulder, LeftElbow, LeftWrist)
        cv2.putText(image, str(int(angle)),
                    tuple(np.multiply(LeftElbow, [640, 480]).astype(int)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                    )

        dict_PoseAngle['LeftElbow'] = angle

    except:
        dict_PoseAngle['LeftElbow'] = -1


    # RightElbow 각도 구하기
    try:
        RightShoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                        landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
        RightElbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                        landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
        RightWrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                     landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

        angle = calculate_angle(RightShoulder, RightElbow, RightWrist)
        cv2.putText(image, str(int(angle)),
                    tuple(np.multiply(RightElbow, [640, 480]).astype(int)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                    )

        dict_PoseAngle['RightElbow'] = angle

    except:
        dict_PoseAngle['RightElbow'] = -1


    # Leftshoulder 각도 구하기
    try:
        LeftElbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
        LeftShoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        LeftHip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                   landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]

        angle = calculate_angle(LeftElbow, LeftShoulder, LeftHip)
        cv2.putText(image, str(int(angle)),
                    tuple(np.multiply(LeftShoulder, [640, 480]).astype(int)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                    )

        dict_PoseAngle['LeftShoulder'] = angle

    except:
        dict_PoseAngle['LeftShoulder'] = -1


    # Rightshoulder 각도 구하기
    try:
        RightElbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                     landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
        RightShoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                        landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
        RightHip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                   landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]

        angle = calculate_angle(RightElbow, RightShoulder, RightHip)
        cv2.putText(image, str(int(angle)),
                    tuple(np.multiply(RightShoulder, [640, 480]).astype(int)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                    )

        dict_PoseAngle['RightShoulder'] = angle

    except:
        dict_PoseAngle['RightShoulder'] = -1


    # LeftHip 각도 구하기
    try:
        LeftShoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        LeftHip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                   landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
        LeftKnee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                    landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]

        angle = calculate_angle(LeftShoulder, LeftHip, LeftKnee)
        cv2.putText(image, str(int(angle)),
                    tuple(np.multiply(LeftHip, [640, 480]).astype(int)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                    )

        dict_PoseAngle['LeftHip'] = angle

    except:
        dict_PoseAngle['LeftHip'] = -1


    # RightHip 각도 구하기
    try:
        RightShoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                        landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
        RightHip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                   landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
        RightKnee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                    landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]

        angle = calculate_angle(RightShoulder, RightHip, RightKnee)
        cv2.putText(image, str(int(angle)),
                    tuple(np.multiply(RightHip, [640, 480]).astype(int)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                    )

        dict_PoseAngle['RightHip'] = angle

    except:
        dict_PoseAngle['RightHip'] = -1


    # Right_Knee 각도 구하기
    try:
        RightHip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                   landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
        RightKnee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                    landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
        RightAnkle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                      landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

        angle = calculate_angle(RightHip, RightKnee, RightAnkle)
        cv2.putText(image, str(int(angle)),
                    tuple(np.multiply(RightKnee, [640, 480]).astype(int)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                    )

        dict_PoseAngle['RightKnee'] = angle

    except:
        dict_PoseAngle['RightKnee'] = -1


    # Left_Knee 각도 구하기
    try:
        LeftHip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                   landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
        LeftKnee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                    landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
        LeftAnkle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                      landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

        angle = calculate_angle(LeftHip, LeftKnee, LeftAnkle)
        cv2.putText(image, str(int(angle)),
                    tuple(np.multiply(LeftKnee, [640, 480]).astype(int)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                    )

        dict_PoseAngle['LeftKnee'] = angle

    except:
        dict_PoseAngle['LeftKnee'] = -1

    # LeftAnkle-Leftknee-RightAnkle 각도 구하기
    try:
        LeftAnkle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
        LeftKnee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                    landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
        RightAnkle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                   landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

        angle = calculate_angle(LeftAnkle, LeftKnee, RightAnkle)
        cv2.putText(image, str(int(angle)),
                    tuple(np.multiply(LeftKnee, [640, 480]).astype(int)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                    )

        dict_PoseAngle['LA-LK-RA'] = angle

    except:
        dict_PoseAngle['LA-LK-RA'] = -1

    # RightAnkle-Rightknee-LeftAnkle 각도 구하기
    try:
        RightAnkle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                     landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
        RightKnee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                    landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
        LeftAnkle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                   landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

        angle = calculate_angle(RightAnkle, RightKnee, LeftAnkle)
        cv2.putText(image, str(int(angle)),
                    tuple(np.multiply(RightKnee, [640, 480]).astype(int)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                    )

        dict_PoseAngle['RA-RK-LA'] = angle

    except:
        dict_PoseAngle['RA-RK-LA'] = -1

    # LeftKnee-LeftHip-RightKnee 각도 구하기
    try:
        LeftKnee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                   landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
        LeftHip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
        RightKnee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                   landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]

        angle = calculate_angle(LeftKnee, LeftHip, RightKnee)
        cv2.putText(image, str(int(angle)),
                    tuple(np.multiply(LeftHip   , [640, 480]).astype(int)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                    )

        dict_PoseAngle['LK-LH-RK'] = angle

    except:
        dict_PoseAngle['LK-LH-RK'] = -1

    # RightKnee-RightHip-LeftKnee 각도 구하기
    try:
        RightKnee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                   landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
        RightHip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                     landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
        LeftKnee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                   landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]

        angle = calculate_angle(RightKnee, RightHip, LeftKnee)
        cv2.putText(image, str(int(angle)),
                    tuple(np.multiply(RightHip   , [640, 480]).astype(int)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                    )

        dict_PoseAngle['RK-RH-LK'] = angle

    except:
        dict_PoseAngle['RK-RH-LK'] = -1

    # LeftAnkle-LeftKnee-RightAnkle 각도 구하기
    try:
        LeftAnkle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                   landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
        LeftKnee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
        RightAnkle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                   landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

        angle = calculate_angle(LeftAnkle, LeftKnee, RightAnkle)
        cv2.putText(image, str(int(angle)),
                    tuple(np.multiply(LeftKnee   , [640, 480]).astype(int)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                    )

        dict_PoseAngle['LA-LK-RA'] = angle

    except:
        dict_PoseAngle['LA-LK-RA'] = -1

    # RightAnkle-RightKnee-LeftAnkle 각도 구하기
    try:
        RightAnkle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                   landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
        RightKnee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                     landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
        LeftAnkle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                   landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

        angle = calculate_angle(RightAnkle, RightKnee, LeftAnkle)
        cv2.putText(image, str(int(angle)),
                    tuple(np.multiply(RightKnee   , [640, 480]).astype(int)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                    )

        dict_PoseAngle['RA-RK-LA'] = angle

    except:
        dict_PoseAngle['RA-RK-LA'] = -1


    # 16번과 14번 사이 거리 구하기
    try:
        RightWrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                      landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
        RightElbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                      landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]


        length = math.hypot(RightElbow[0] - RightWrist[0], RightElbow[1] - RightWrist[1]) * 100
        cv2.putText(image, str(length),
                    tuple(np.multiply(RightWrist, [640, 480]).astype(int)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA
                    )

        dict_PoseLength['16, 14'] = length

    except:
        dict_PoseLength['16, 14'] = -1


    # 14번과 12번 사이 거리 구하기
    try:
        RightElbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                      landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
        RightShoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                         landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]


        length = math.hypot(RightShoulder[0] - RightElbow[0], RightShoulder[1] - RightElbow[1]) * 100
        cv2.putText(image, str(length),
                    tuple(np.multiply(RightElbow, [640, 500]).astype(int)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA
                    )

        dict_PoseLength['14, 12'] = length

    except:
        dict_PoseLength['14, 12'] = -1


    # 24번과 12번 사이 거리 구하기
    try:
        RightShoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                         landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
        RightHip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                    landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]


        length = math.hypot(RightHip[0] - RightShoulder[0], RightHip[1] - RightShoulder[1]) * 100
        cv2.putText(image, str(length),
                    tuple(np.multiply(RightShoulder, [640, 500]).astype(int)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA
                    )

        dict_PoseLength['24, 12'] = length

    except:
        dict_PoseLength['24, 12'] = -1


    # 26번과 24번 사이 거리 구하기
    try:
        RightHip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                    landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
        RightKnee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                     landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]


        length = math.hypot(RightKnee[0] - RightHip[0], RightKnee[1] - RightHip[1]) * 100
        cv2.putText(image, str(length),
                    tuple(np.multiply(RightHip, [640, 500]).astype(int)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA
                    )

        dict_PoseLength['26, 24'] = length

    except:
        dict_PoseLength['26, 24'] = -1


    # 28번과 26번 사이 거리 구하기
    try:
        RightKnee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                     landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
        RightAnkle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                      landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]


        length = math.hypot(RightAnkle[0] - RightKnee[0], RightAnkle[1] - RightKnee[1]) * 100
        cv2.putText(image, str(length),
                    tuple(np.multiply(RightKnee, [640, 500]).astype(int)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA
                    )

        dict_PoseLength['28, 26'] = length

    except:
        dict_PoseLength['28, 26'] = -1



    # 15번과 13번 사이 거리 구하기
    try:
        LeftWrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
        LeftElbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                      landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]


        length = math.hypot(LeftElbow[0] - LeftWrist[0], LeftElbow[1] - LeftWrist[1]) * 100
        cv2.putText(image, str(length),
                    tuple(np.multiply(LeftWrist, [640, 500]).astype(int)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA
                    )

        dict_PoseLength['15, 13'] = length

    except:
        dict_PoseLength['15, 13'] = -1


    # 13번과 11번 사이 거리 구하기
    try:
        LeftElbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                      landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
        LeftShoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]


        length = math.hypot(LeftShoulder[0] - LeftElbow[0], LeftShoulder[1] - LeftElbow[1]) * 100
        cv2.putText(image, str(length),
                    tuple(np.multiply(LeftElbow, [640, 500]).astype(int)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA
                    )

        dict_PoseLength['13, 11'] = length

    except:
        dict_PoseLength['13, 11'] = -1


    # 23번과 11번 사이 거리 구하기
    try:
        LeftShoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        LeftHip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                   landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]


        length = math.hypot(LeftHip[0] - LeftShoulder[0], LeftHip[1] - LeftShoulder[1]) * 100
        cv2.putText(image, str(length),
                    tuple(np.multiply(LeftShoulder, [640, 500]).astype(int)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA
                    )

        dict_PoseLength['23, 11'] = length

    except:
        dict_PoseLength['23, 11'] = -1


    # 25번과 23번 사이 거리 구하기
    try:
        LeftHip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                   landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
        LeftKnee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                    landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]


        length = math.hypot(LeftKnee[0] - LeftHip[0], LeftKnee[1] - LeftHip[1]) * 100
        cv2.putText(image, str(length),
                    tuple(np.multiply(LeftHip, [640, 500]).astype(int)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA
                    )

        dict_PoseLength['25, 23'] = length

    except:
        dict_PoseLength['25, 23'] = -1

    # 27번과 25번 사이 거리 구하기
    try:
        LeftKnee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
        LeftAnkle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                      landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]


        length = math.hypot(LeftAnkle[0] - LeftKnee[0], LeftAnkle[1] - LeftKnee[1]) * 100
        cv2.putText(image, str(length),
                    tuple(np.multiply(LeftKnee, [640, 500]).astype(int)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA
                    )

        dict_PoseLength['27, 25'] = length

    except:
        dict_PoseLength['27, 25'] = -1

    # 15번과 11번 사이 거리 구하기
    try:
        LeftWrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
        LeftShoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                      landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]


        length = math.hypot(LeftShoulder[0] - LeftWrist[0], LeftShoulder[1] - LeftWrist[1]) * 100
        cv2.putText(image, str(length),
                    tuple(np.multiply(LeftWrist, [640, 500]).astype(int)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA
                    )

        dict_PoseLength['15, 11'] = length

    except:
        dict_PoseLength['15, 11'] = -1

    # 16번과 12번 사이 거리 구하기
    try:
        RightWrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                     landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
        RightShoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                      landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]


        length = math.hypot(RightShoulder[0] - RightWrist[0], RightShoulder[1] - RightWrist[1]) * 100
        cv2.putText(image, str(length),
                    tuple(np.multiply(RightWrist, [640, 500]).astype(int)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA
                    )

        dict_PoseLength['16, 12'] = length

    except:
        dict_PoseLength['16, 12'] = -1

    # 12번과 11번 사이 거리 구하기
    try:
        LeftShoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        RightShoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                      landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]


        length = math.hypot(RightShoulder[0] - LeftShoulder[0], RightShoulder[1] - LeftShoulder[1]) * 100
        cv2.putText(image, str(length),
                    tuple(np.multiply(LeftShoulder, [640, 500]).astype(int)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA
                    )

        dict_PoseLength['12, 11'] = length

    except:
        dict_PoseLength['12, 11'] = -1

    # 16번과 15번 사이 거리 구하기
    try:
        LeftWrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
        RightWrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                      landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]


        length = math.hypot(RightWrist[0] - LeftWrist[0], RightWrist[1] - LeftWrist[1]) * 100
        cv2.putText(image, str(length),
                    tuple(np.multiply(LeftWrist, [640, 500]).astype(int)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA
                    )

        dict_PoseLength['16, 15'] = length

    except:
        dict_PoseLength['16, 15'] = -1

    # 14번과 13번 사이 거리 구하기
    try:
        LeftElbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
        RightElbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                      landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]


        length = math.hypot(RightElbow[0] - LeftElbow[0], RightElbow[1] - LeftElbow[1]) * 100
        cv2.putText(image, str(length),
                    tuple(np.multiply(LeftElbow, [640, 500]).astype(int)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA
                    )

        dict_PoseLength['14, 13'] = length

    except:
        dict_PoseLength['14, 13'] = -1

    # 26번과 25번 사이 거리 구하기
    try:
        RightKnee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                     landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
        LeftKnee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                      landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]


        length = math.hypot(RightKnee[0] - LeftKnee[0], RightKnee[1] - LeftKnee[1]) * 100
        cv2.putText(image, str(length),
                    tuple(np.multiply(RightKnee, [640, 500]).astype(int)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA
                    )

        dict_PoseLength['26, 25'] = length

    except:
        dict_PoseLength['26, 25'] = -1

    # 28번과 27번 사이 거리 구하기
    try:
        RightAnkle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                     landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
        LeftAnkle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                      landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]


        length = math.hypot(RightAnkle[0] - LeftAnkle[0], RightAnkle[1] - LeftAnkle[1]) * 100
        cv2.putText(image, str(length),
                    tuple(np.multiply(RightAnkle, [640, 500]).astype(int)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA
                    )

        dict_PoseLength['28, 27'] = length

    except:
        dict_PoseLength['28, 27'] = -1

    return image, white_img
