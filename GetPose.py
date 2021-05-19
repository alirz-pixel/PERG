import mediapipe as mp
import PoseEstimationModule as pea
import cv2


dict_PoseAngle = {}
dict_PoseLength = {}
dict_PoseLower = {}
cap = cv2.VideoCapture(0)

#(상체, 하체, 전신 구분함수 05.15 이범석)
def UpperBody():
    # 기본 기립자세 인식
    if dict_PoseLength['23, 15'] <= 7.5 and dict_PoseLength['24, 16'] <= 7.5:
        if dict_PoseLength['12, 11'] >= dict_PoseLength['26, 25']:
            if dict_PoseAngle['LeftHip'] >= 165 and dict_PoseAngle['RightHip'] >= 165:
                if dict_PoseAngle['LeftKnee'] >= 165 and dict_PoseAngle['RightKnee'] >= 165:
                    print('standing')
                    return 'standing'

    # big clap 인식
    #print(dict_PoseLength['16, 15'] / dict_PoseLength['12, 11'])
    if (50 <= dict_PoseAngle['LeftShoulder'] <= 105 and 50 <= dict_PoseAngle['RightShoulder'] <= 105) and \
            (dict_PoseLength['16, 15'] / dict_PoseLength['12, 11'] >= 3.6):
        if 130 <= dict_PoseAngle['LeftElbow'] and 130 <= dict_PoseAngle['RightElbow']:
            print('big clap-1')
            return 'big clap-1'
    #if dict_PoseLower['Wrist'] == 1:
    if (dict_PoseAngle['LeftShoulder'] <= 50 and dict_PoseAngle['RightShoulder'] <= 50) and \
        (dict_PoseLength['16, 15'] / dict_PoseLength['12, 11'] <= 1.4):
        if dict_PoseLength['15, 11'] / dict_PoseLength['12, 11'] <= 0.5 and dict_PoseLength['16, 12'] / dict_PoseLength['12, 11'] <= 0.5:
            print('big clap-2')
            return 'big clap-2'

    # chest fly 인식
    if dict_PoseLower['Wrist'] == 0:
        if 70 <= dict_PoseAngle['LeftShoulder'] <= 110 and 70 <= dict_PoseAngle['RightShoulder'] <= 110:
            if 55 <= dict_PoseAngle['LeftElbow'] <= 105 and 55 <= dict_PoseAngle['RightElbow'] <= 105:
                print('chestfly-1')
                return('chestfly-1')

    if dict_PoseLength['14, 13'] / dict_PoseLength['12, 11'] <= 1.2 and dict_PoseLength['16, 15'] / \
            dict_PoseLength['12, 11'] >= 0.25:
        if dict_PoseLower['Wrist'] == 0:
            print('chestfly-2')
            return 'chestfly-2'

    # 프론트 & 백레이즈
    if dict_PoseLength['16, 15'] / dict_PoseLength['12, 11'] >= 2:
        if dict_PoseAngle['RightElbow'] >= 140 and dict_PoseAngle['LeftElbow'] >= 140:
            if dict_PoseAngle['RightShoulder'] >= 90 and 20 <= dict_PoseAngle['LeftShoulder'] <= 60:
                print('Right-Front&BackRaise')
                return 'Right-Front&BackRaise'

    if dict_PoseLength['16, 15'] / dict_PoseLength['12, 11'] >= 2:
        if dict_PoseAngle['LeftElbow'] >= 140 and dict_PoseAngle['RightElbow'] >= 140:
            if dict_PoseAngle['LeftShoulder'] >= 90 and 20 <= dict_PoseAngle['RightShoulder'] <= 60:
                print('Left-Front&BackRaise')
                return 'Left-Front&BackRaise'
def LowerBody():

    # 기본 기립자세 인식
    if dict_PoseLength['23, 15'] <= 5 and dict_PoseLength['24, 16'] <= 5:
        if dict_PoseAngle['LeftHip'] >= 160 and dict_PoseAngle['RightHip']:
            if dict_PoseAngle['LeftKnee'] >= 160 and dict_PoseAngle['RightKnee'] >= 160:
                print('standing')
                return 'standing'
    # 스쿼트 인식
    if 0.4 <= dict_PoseLength['26, 24'] / dict_PoseLength['28, 26'] <= 0.8 \
            and 0.4 <= dict_PoseLength['25, 23'] / dict_PoseLength['27, 25'] <= 0.8:
        print('squat-1')
        return 'squat-1'

    # 런지 인식
    if (dict_PoseAngle['LeftKnee'] <= 95 and dict_PoseAngle['RightKnee'] >= 105) or \
            (dict_PoseAngle['RightKnee'] <= 95 and dict_PoseAngle['LeftKnee'] >= 105):
        if dict_PoseAngle['LA-LK-RA'] >= 145 or dict_PoseAngle['RA-RK-LA'] >= 145:
            print('lunge')
            return 'lunge'

    # KneeLift 인식
    if ((dict_PoseAngle['LeftKnee'] <= 105 and dict_PoseAngle['RightKnee'] >= 160)
        or (dict_PoseAngle['RightKnee'] <= 105 and dict_PoseAngle['LeftKnee'] >= 160)) \
            and (dict_PoseAngle['LeftHip'] >= 160 or dict_PoseAngle['RightHip'] >= 160):
        print('KneeLift')
        return 'KneeLift'
def FullBody():
    # Full-Body Motion 1-R
    if dict_PoseAngle['LeftElbow'] <= 110 and dict_PoseAngle['RightElbow'] >= 150:
        if dict_PoseAngle['RightShoulder'] >= 80 and dict_PoseAngle['LeftShoulder'] <= 50:
            if 20 <= dict_PoseAngle['RA-RK-LA'] <= 70:
                print('Full-Body Motion 1-R')
                return 'Full-Body Motion 1-R'
    # Full-Body Motion 1-L
    if dict_PoseAngle['RightElbow'] <= 110 and dict_PoseAngle['LeftElbow'] >= 150:
        if dict_PoseAngle['LeftShoulder'] >= 80 and dict_PoseAngle['RightShoulder'] <= 50:
            if 20 <= dict_PoseAngle['LA-LK-RA'] <= 70:
                print('Full-Body Motion 1-L')
                return 'Full-Body Motion 1-L'

    # Full-Body Motion 2-R
    if 70 <= dict_PoseAngle['LeftKnee'] <= 110 and dict_PoseAngle['RightKnee'] >= 150:
        if 70 <= dict_PoseAngle['LeftHip'] <= 110 and dict_PoseAngle['RightHip'] >= 150 and \
                70 <= dict_PoseAngle['RightElbow'] <= 110:
            print('Full-Body Motion 2-R')
            return 'Full-Body Motion 2-R'
    # Full-Body Motion 2-L
    if 70 <= dict_PoseAngle['RightKnee'] <= 110 and dict_PoseAngle['LeftKnee'] >= 150:
        if 70 <= dict_PoseAngle['RightHip'] <= 110 and dict_PoseAngle['LeftHip'] >= 150 and \
                70 <= dict_PoseAngle['LeftElbow'] <= 110:
            print('Full-Body Motion 2-L')
            return 'Full-Body Motion 2-L'

    # Full-Body Motion 3
    if dict_PoseLower['Wrist'] == 0:
        if 2.25 <= dict_PoseLength['16, 15'] / dict_PoseLength['12, 11'] <= 3.5 and 1.75 <= dict_PoseLength['14, 13'] / \
                dict_PoseLength['12, 11'] <= 3:
            if 1.3 <= dict_PoseLength['28, 27'] / dict_PoseLength['12, 11'] <= 2.55 and 1.05 <= dict_PoseLength[
                '26, 25'] / dict_PoseLength['12, 11'] <= 2.3:
                if (dict_PoseAngle['LeftHip'] >= 150 and dict_PoseAngle['RightHip'] >= 150) and \
                        (dict_PoseAngle['LeftElbow'] >= 150 and dict_PoseAngle['RightElbow'] >= 150) and \
                        (dict_PoseAngle['LeftKnee'] >= 150 and dict_PoseAngle['RightKnee'] >= 150):
                    print('Full-Body Motion 3')
                    return 'Full-Body Motion 3'

    # Full-Body Motion 4-R
    if dict_PoseLength['26, 15'] > dict_PoseLength['25, 15'] and \
            (70 <= dict_PoseAngle['LeftShoulder'] <= 110 and 30 <= dict_PoseAngle['LK-LH-RK'] <= 110):
        if dict_PoseAngle['LeftElbow'] >= 155 and dict_PoseAngle['RightElbow'] >= 155:
            if 50 <= dict_PoseAngle['RK-RH-LK'] <= 120 and dict_PoseLength['28, 27'] / dict_PoseLength['26, 25'] >= 1.3:
                print('FBM 4-R')
                return 'FBM 4-R'
    # Full-Body Motion 4-L
    if dict_PoseLength['25, 16'] > dict_PoseLength['26, 16'] and \
            (70 <= dict_PoseAngle['RightShoulder'] <= 110 and 30 <= dict_PoseAngle['RK-RH-LK'] <= 110):
        if dict_PoseAngle['LeftElbow'] >= 155 and dict_PoseAngle['RightElbow'] >= 155:
            if 50 <= dict_PoseAngle['RK-RH-LK'] <= 120 and dict_PoseLength['28, 27'] / dict_PoseLength['26, 25'] >= 1.3:
                print('FBM 4-L')
                return 'FBM 4-L'

    # Full-Body Motion 5-R
    if dict_PoseLower['Waist'] == 0:
        if 80 <= dict_PoseAngle['LW-RW-LA'] <= 100 and 80 <= dict_PoseAngle['LW-RA-LA'] <= 100:
            if 50 <= dict_PoseAngle['RK-RH-LK'] <= 120 and dict_PoseLength['28, 27'] / dict_PoseLength['26, 25'] >= 1.3:
                print('FBM 5-R')
                return 'FBM 5-R'
    # Full-Body Motion 5-L
    if dict_PoseLower['Waist'] == 0:
        if 80 <= dict_PoseAngle['RW-LW-RA'] <= 100 and 80 <= dict_PoseAngle['RW-LA-RA'] <= 100:
            if 50 <= dict_PoseAngle['LK-LH-RK'] <= 120 and dict_PoseLength['28, 27'] / dict_PoseLength['26, 25'] >= 1.3:
                print('FBM 5-L')
                return 'FBM 5-L'

    # Full-Body Motion 6-R
    if dict_PoseLower['Waist'] == 0:
        if 80 <= dict_PoseAngle['RW-LW-LA'] <= 100 and 80 <= dict_PoseAngle['RW-RA-LA'] <= 100:
            if 50 <= dict_PoseAngle['LK-LH-RK'] <= 120 and dict_PoseLength['28, 27'] / dict_PoseLength['26, 25'] >= 1.3:
                print('FBM 6-R')
                return 'FBM 6-R'
    # Full-Body Motion 6-L
    if dict_PoseLower['Waist'] == 0:
        if 80 <= dict_PoseAngle['LW-RW-RA'] <= 100 and 80 <= dict_PoseAngle['LW-LA-RA'] <= 100:
            if 50 <= dict_PoseAngle['RK-RH-LK'] <= 120 and dict_PoseLength['28, 27'] / dict_PoseLength['26, 25'] >= 1.3:
                print('FBM 6-L')
                return 'FBM 6-L'

def Func_GetUpperPose(frame, holistic):
    pea.pose_estimation(frame, holistic, dict_PoseAngle, dict_PoseLength, dict_PoseLower)
    return UpperBody()


def main():
    with mp.solutions.holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        while cap.isOpened():
            _, frame = cap.read()
            white_img = cv2.imread('640x480-white-solid-color-background.jpg')

            image, white_img = pea.pose_estimation(frame, holistic, dict_PoseAngle, dict_PoseLength, dict_PoseLower, white_img)

            cv2.imshow('Cam Bg Pose Estimation', image)
            cv2.imshow('White Bg Pose Estimation', white_img)

            UpperBody()

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

