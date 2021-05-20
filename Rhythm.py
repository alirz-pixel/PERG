'''
2021-05-08  16:21  리듬게임 도중에 치어리더와 같은 effect 나오는 소스코드 작성 - 김수영 (아직 병합되지 않음)
2021-05-13  14:41  Rhythm.py 모듈화 (소스코드 분할) - 최문형
2021-05-15  11:32  정확도 계산 코드 작성 - 김창현
2021-05-15  11:57  노드 타이밍 및 음악 가져오는 소스코드 병합 - 최문형
2021-05-15  14:48  combo 시스템 구현 - 김창현
2021-05-17  02:23  동작인식 이미지 추가와 동작인식을 할 수 있도록 코드 추가 - 최문형
2021-05-17  10:23  도전과제 출력 시스템 병합 - 최문형
2021-05-17  21:05  도전과제 출력 타이밍 개선 - 김창현 
'''

import GetPose as GP
import mediapipe as mp
import SongLoad as SL
import cv2 as cv
import pygame
import random
import sys

def start(Screen, musicIndex = 1):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BLUE = (0, 199, 254)
    GREEN = (35, 226, 11)
    PINK = (251, 64, 174)

    COLORS = [BLUE, GREEN, PINK]


    ######################################################################
    # 화면 크기
    Screen_Width = 1280  # 가로 크기
    Screen_Height = 720  # 세로 크기

    ######################################################################
    # 포즈 관련
    Standing = pygame.image.load('Rhythm/Upper_Pose/Standing.png').convert_alpha()
    Standing = pygame.transform.scale(Standing, (int(Standing.get_rect().width / 1.5), int(Standing.get_rect().height / 1.5)))

    LFB_RAISE = pygame.image.load('Rhythm/Upper_Pose/LFB-RAISE.png').convert_alpha()
    LFB_RAISE = pygame.transform.scale(LFB_RAISE, (int(LFB_RAISE.get_rect().width / 1.5), int(LFB_RAISE.get_rect().height / 1.5)))

    RFB_RAISE = pygame.image.load('Rhythm/Upper_Pose/RFB-RAISE.png').convert_alpha()
    RFB_RAISE = pygame.transform.scale(RFB_RAISE, (int(RFB_RAISE.get_rect().width / 1.5), int(RFB_RAISE.get_rect().height / 1.5)))

    chestfly1 = pygame.image.load('Rhythm/Upper_Pose/chestfly1.png').convert_alpha()
    chestfly1 = pygame.transform.scale(chestfly1, (int(chestfly1.get_rect().width / 1.5), int(chestfly1.get_rect().height / 1.5)))

    chestfly2 = pygame.image.load('Rhythm/Upper_Pose/chestfly2.png').convert_alpha()
    chestfly2 = pygame.transform.scale(chestfly2, (int(chestfly2.get_rect().width / 1.5), int(chestfly2.get_rect().height / 1.5)))

    bigclap1 = pygame.image.load('Rhythm/Upper_Pose/bigclap1.png').convert_alpha()
    bigclap1 = pygame.transform.scale(bigclap1, (int(bigclap1.get_rect().width / 1.5), int(bigclap1.get_rect().height / 1.5)))

    bigclap2 = pygame.image.load('Rhythm/Upper_Pose/bigclap2.png').convert_alpha()
    bigclap2 = pygame.transform.scale(bigclap2, (int(bigclap2.get_rect().width / 1.5), int(bigclap2.get_rect().height / 1.5)))

    list_Node = [[RFB_RAISE, Standing],
                 [LFB_RAISE, Standing],
                 [chestfly1, chestfly2],
                 [bigclap1, bigclap2]]

    MAX_POSE = 4

    Pose_Index = -1
    Node_Index = -1
    ######################################################################
    # copyright : 최문형
    def Func_PoseSame(GetPose, Index1, Index2):
        if (Index1 == 0 or Index1 == 1) and Index2 == 1 and GetPose == 'standing':
            return True
        if Index1 == 0 and Index2 == 0 and GetPose == 'Left-Front&BackRaise':
            return True
        if Index1 == 1 and Index2 == 0 and GetPose == 'Right-Front&BackRaise':
            return True
        if Index1 == 2 and Index2 == 0 and GetPose == 'chestfly-1':
            return True
        if Index1 == 2 and Index2 == 1 and GetPose == 'chestfly-2':
            return True
        if Index1 == 3 and Index2 == 0 and GetPose == 'big clap-1':
            return True
        if Index1 == 3 and Index2 == 1 and GetPose == 'big clap-2':
            return True

        return False
    ######################################################################

    def MakeNode(isLeft, Index1 = 0, Index2 = 0):
        NodeRect = list_Node[Index1][Index2].get_rect()
        NodeRect.top = 150

        NodeRect.right = Screen_Width + list_Node[Index1][Index2].get_width()
        if isLeft:
            NodeRect.left = 0 - list_Node[Index1][Index2].get_width()

        return [list_Node[Index1][Index2], NodeRect, isLeft, Index1, Index2]


    def Func_ChangeBackground(Color):
        # Bg == Blue
        BgColor[3] += 1

        if Color == 0:
            BgColor[0] -= int(abs((PINK[0] - BLUE[0]) / 13))
            BgColor[1] += int(abs((PINK[1] - BLUE[1]) / 13))
            BgColor[2] += int(abs((PINK[2] - BLUE[2]) / 13))


        # Bg == GREEN
        elif Color == 1:
            BgColor[0] += int(abs((BLUE[0] - GREEN[0]) / 13))
            BgColor[1] += int(abs((BLUE[1] - GREEN[1]) / 13))
            BgColor[2] -= int(abs((BLUE[2] - GREEN[2]) / 13))


        # Bg == PINK
        elif Color == 2:
            BgColor[0] += int(abs((GREEN[0] - PINK[0]) / 13))
            BgColor[1] -= int(abs((GREEN[1] - PINK[1]) / 13))
            BgColor[2] += int(abs((GREEN[2] - PINK[2]) / 13))



        if BgColor[3] >= 12:
            for i in range(3):
                BgColor[i] = COLORS[Color][i]
            BgColor[3] = 0
            return 0

        return 1

    # OpenCV 기본 초기화
    cap = cv.VideoCapture(0)

    # 동작 인식을 위한 변수
    Motion_Delay = 125
    Motion_Time = 0
    ######################################################################
    # FPS
    Clock = pygame.time.Clock()
    ######################################################################
    # 배경 색상 관련 변수 및 상수
    Background_Delay = 3000
    Background_Time = 0
    Background_Color = 0
    Background_MAX = 3
    Background_Change = 0
    BgColor = [0, 199, 254, 0]

    GameOn = 1
    NodeOn = 1
    # 배경 왼/오른쪽/가운데 이미지 불러오기
    Background_Middle = pygame.image.load("Rhythm/Screen/Smartphone.png").convert_alpha()
    Background_Middle = pygame.transform.scale(Background_Middle, (545, 808))

    Background_Laft = pygame.image.load("Rhythm/Screen/SmartphoneLeftScreen.png").convert_alpha()
    Background_Laft = pygame.transform.scale(Background_Laft, (405, 607))

    Background_Right = pygame.image.load("Rhythm/Screen/SmartphoneRightScreen.png").convert_alpha()
    Background_Right = pygame.transform.scale(Background_Right, (410, 607))

    # Fadein을 구현하기 위한 코드
    FadeIn = pygame.image.load("Rhythm/Screen/BlackScreen.png").convert_alpha()
    FadeIn = pygame.transform.scale(FadeIn, (1700, Screen_Height))

    OpacityLevel = 255
    # 배경 위쪽의 그림자 생성
    ShadowRect = pygame.image.load("Rhythm/Screen/BlackScreen.png")
    ShadowRect = pygame.transform.scale(ShadowRect, (Screen_Width, 6))

    WhiteScreen = pygame.image.load("Rhythm/Screen/WhiteScreen.png")
    WhiteScreen = pygame.transform.scale(WhiteScreen, (478, 771))
    

    ######################################################################
    # 도전과제 이미지 불러오기

    # 시작이 반이다
    # 첫 곡을 끝마침
    achievement1 = pygame.image.load("Rhythm/achievement/achievement1.png")
    achievement1_Size = achievement1.get_rect().size  # 이미지의 사이즈
    achievement1_Width = achievement1_Size[0]  # 이미지의 너비
    achievement1_Height = achievement1_Size[1]  # 이미지의 높이
    achievement1 = pygame.transform.scale(achievement1, (int(achievement1_Width / 1.5), int(achievement1_Height / 1.5)))

    # 의지박약
    # 정확도 0%로 게임을 끝마침
    achievement2 = pygame.image.load("Rhythm/achievement/achievement2.png")
    achievement2_Width = achievement2.get_rect().width  # 이미지의 너비
    achievement2 = pygame.transform.scale(achievement2, (400, 600))

    # 리듬천재
    # 정확도 100%로 게임을 끝마침
    achievement3 = pygame.image.load("Rhythm/achievement/achievement3.png")
    achievement3_Width = achievement3.get_rect().width  # 이미지의 너비
    achievement3 = pygame.transform.scale(achievement3, (482, 600))

    # 단 한 곡
    # 한 곡을 50번 플레이함
    achievement4 = pygame.image.load("Rhythm/achievement/achievement4.png")
    achievement4_Width = achievement4.get_rect().width  # 이미지의 너비
    achievement4 = pygame.transform.scale(achievement4, (463, 600))

    # 에어로빅 강사
    # 게임을 50번 이상 플레이함
    achievement5 = pygame.image.load("Rhythm/achievement/achievement5.png")
    achievement5_Width = achievement5.get_rect().width  # 이미지의 너비
    achievement5 = pygame.transform.scale(achievement5, (495, 600))

    # 3대 500
    # 게임을 500번 이상 플레이함
    achievement6 = pygame.image.load("Rhythm/achievement/achievement6.png")
    achievement6_Width = achievement6.get_rect().width  # 이미지의 너비
    achievement6 = pygame.transform.scale(achievement6, (472, 600))

    # 헬창
    # 1년 동안 하루도 빠짐없이 게임에 접속함
    achievement7 = pygame.image.load("Rhythm/achievement/achievement7.png")
    achievement7_Width = achievement7.get_rect().width # 이미지의 너비
    achievement7 = pygame.transform.scale(achievement7, (443, 600))

    list_Achievement = [[achievement1, achievement1_Width, 871],
                        [achievement2, achievement2_Width, 871],
                        [achievement3, achievement3_Width, 871],
                        [achievement4, achievement4_Width, 871],
                        [achievement5, achievement5_Width, 871],
                        [achievement6, achievement6_Width, 871],
                        [achievement7, achievement7_Width, 871]]
    
    #도전과제 변수
    # 짜쟌 효과음
    Tada = pygame.mixer.Sound("Rhythm/BGM/ジャジャーン.mp3")
    NodeBGM = pygame.mixer.Sound("Rhythm/BGM/決定、ボタン押下2.mp3")
    count = 1  # 룰렛 돈 횟수
    PlayOn = 0  # 배경음악이 켜져있는 확인하는 척도
    a = 0  # 룰렛의 가속도

    index = 0
    c_index = 2  # 도전과제 달성 인덱스
    ##########################################################################################
    # 배경음악
    SectionNum = 1
    Song_Time = 0

    music, SongSection, SongName, SongTime = SL.LoadSong(musicIndex)
    ######################################################################
    # 시간 계산
    Start_Ticks = pygame.time.get_ticks()
    ######################################################################
    Timer_Font = pygame.font.Font("Rhythm/Font/CookieRun Regular.ttf", 30) # 폰트 객체 생성(폰트, 크기)
    Music_Font = pygame.font.Font("Rhythm/Font/CookieRun Bold.ttf", 40)
    Percentage_Font = pygame.font.Font("Rhythm/Font/CookieRun Bold.ttf", 40)
    ######################################################################
    # 리듬게임의 노드 관련
    PlusScore = 0    # 사용자가 얼마나 맞췄는지 판단하는 변수
    NodeCount = 0    # 현재 까지 나온 노드의 수를 담는 변수
    Percentage = 100 # 정확도를 화면에 출력하기 위한 변수
    queue_Node = []  # 화면에 나온 노드들을 담는 배열 -> 자료구조의 queue 이용

    # 콤보 관련
    Combo_FontSize = 0
    ComboNum = 0
    ComboMax = 0

    x = 1
    Crashed = False
    ######################################################################
    with mp.solutions.holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        while not Crashed:
            Elapsed_Time = (pygame.time.get_ticks() - Start_Ticks) / 1000
            for event in pygame.event.get(): # 어떤 이벤트가 발생하였는가?
                if event.type == pygame.QUIT: # 창이 닫히는 이벤트가 발생하였는가?
                    Crashed = True

                if event.type == pygame.MOUSEBUTTONDOWN:
                    #print(pygame.mouse.get_pos())
                    
                    if Pose_Index == -1:
                        Pose_Index = random.randrange(0, MAX_POSE)
                        Node_Index = 0

                    # 왼쪽 노드 추가하기
                    if random.randrange(0, 2):
                        queue_Node.append(MakeNode(1, Pose_Index, Node_Index))

                    # 오른쪽 노드 추가하기
                    else:
                        queue_Node.append(MakeNode(0, Pose_Index, Node_Index))

                    Node_Index += 1
                    if Node_Index == 2:
                        Pose_Index = -1

                if event.type == pygame.KEYDOWN:  # 키가 눌렸는지 확인
                    if event.key == pygame.K_DOWN:  # 아래 방향키
                        try:
                            if queue_Node[0][2] == 0:  # 오른쪽에서 노드가 나옸다면
                                if 895 in range(queue_Node[0][1].left, queue_Node[0][1].left + queue_Node[0][1].width):
                                    queue_Node.pop(0)
                                    print("Right_Yes!")
                                    Combo_FontSize = 60
                                    PlusScore += 1
                                    ComboNum += 1

                                    if NodeCount != 0:
                                        Percentage = round(PlusScore / NodeCount * 100)  # 정확도
                        except:
                            pass

                    if event.key == pygame.K_UP: # 위쪽 방향키
                        try:
                            if queue_Node[0][2] == 1: # 왼쪽에서 노드가 나옸다면
                                if 372 in range(queue_Node[0][1].left, queue_Node[0][1].left + queue_Node[0][1].width):
                                    queue_Node.pop(0)
                                    print("Left_Yes!")
                                    Combo_FontSize = 60
                                    PlusScore += 1
                                    ComboNum += 1

                                    if NodeCount != 0:
                                        Percentage = round(PlusScore / NodeCount * 100)  # 정확도
                        except:
                            pass

        ######################################################################
            # 화면 색깔 변환
            Now_Time = pygame.time.get_ticks()
            if (Now_Time > Background_Time + Background_Delay):
                Background_Time = Now_Time
                Background_Color += 1
                Background_Change = 1
                if (Background_Color >= Background_MAX):
                    Background_Color = 0

            if Background_Change:
                Background_Change = Func_ChangeBackground(Background_Color)

            Screen.fill((BgColor[0], BgColor[1], BgColor[2]))
            # 그림자 생성
            ShadowRect.set_alpha(70)
            Screen.blit(ShadowRect, (0, 107))
            ShadowRect.set_alpha(50)
            Screen.blit(ShadowRect, (0, 105))
            ShadowRect.set_alpha(30)

            Screen.blit(ShadowRect, (0, 102))
            Screen.blit(Background_Laft, (0, 112))
            Screen.blit(Background_Right, (870, 112))


        ######################################################################
            if PlayOn == 1:
                # 노드를 중앙으로 움직이기
                for i in range(len(queue_Node)):
                    # 만약 왼쪽 노드라면
                    if queue_Node[i][2] == 1:
                        queue_Node[i][1].left += 15
    
                    # 만약 오른쪽 노드라면
                    else:
                        queue_Node[i][1].right -= 15
    
                # 노드를 화면에 출력하기
                for temp, tempRect, _, _, _ in queue_Node:
                    Screen.blit(temp, tempRect)

        ######################################################################
            # 배경음악
            if PlayOn == 0 and GameOn == 1:
                pygame.mixer.music.load(music)
                pygame.mixer.music.play()
                PlayOn += 1

            if not pygame.mixer.music.get_busy(): # 음악 재생이 끝나면
                NodeOn = 0 
                # 경과 시간(ms)을 1000으로 나누어서 초(s) 단위로 표시
                Elapsed_Time = (pygame.time.get_ticks() - Start_Ticks) / 1000
                if (Elapsed_Time > SongTime + 10):
                    GameOn = 0

            if GameOn == 1:
                # 사용자 캠 불러오기
                _, frame = cap.read()
                frame = cv.flip(frame, 1)

                # 동작 인식 받기
                # 동작인식을 계속 받아오면 프레임이 끊기는 문제가 발생하여
                # 일정 딜레이(Motion_Delay)가 지나야 동작을 인식받도록 함
            
                Now_Time = pygame.time.get_ticks()
                if (Now_Time > Motion_Time + Motion_Delay):
                    Motion_Time = Now_Time
                    GetPose = GP.Func_GetUpperPose(frame, holistic)

                    # 현재의 노드와 GetPose가 같은지 확인하는 코드
                    try:
                        Bool_Same = Func_PoseSame(GetPose, queue_Node[0][-2], queue_Node[0][-1])

                        # 노드의 타이밍에 맞게 동작을 취했는지 확인하는 코드
                        if Bool_Same:
                            if queue_Node[0][2] == 0:  # 오른쪽에서 노드가 나옸다면
                                if 895 in range(queue_Node[0][1].left, queue_Node[0][1].left + queue_Node[0][1].width):
                                    queue_Node.pop(0)
                                    print("Right_Yes!")
                                    Combo_FontSize = 60
                                    PlusScore += 1
                                    ComboNum += 1

                                    if NodeCount != 0:
                                        Percentage = round(PlusScore / NodeCount * 100)  # 정확도

                            if queue_Node[0][2] == 1:  # 왼쪽에서 노드가 나옸다면
                                if 372 in range(queue_Node[0][1].left, queue_Node[0][1].left + queue_Node[0][1].width):
                                    queue_Node.pop(0)
                                    print("Left_Yes!")
                                    Combo_FontSize = 60
                                    PlusScore += 1
                                    ComboNum += 1

                                    if NodeCount != 0:
                                        Percentage = round(PlusScore / NodeCount * 100)  # 정확도

                    except:
                        pass

                # 사용자의 캠을 스마트폰 화면 안에 넣기위해 인식받은 사용자의 캠의 크기를 원하는 크기만큼 자른다.
                frame = frame[0:480, 153:486]
                cv.imwrite('Frame.png', frame)
    
                py_Frame = pygame.image.load("Frame.png").convert_alpha()
                py_Frame = pygame.transform.scale(py_Frame, (478, 771))
                Screen.blit(py_Frame, (399, 111))
                Screen.blit(Background_Middle, (363, 43))

            elif GameOn == 0:  # 게임 온이 0이 되면
                if PlayOn == 1:
                        pygame.mixer.music.load("Rhythm/BGM/379240__westington__slot-machine.wav")
                        pygame.mixer.music.play(-1)
                        PlayOn -= 1
                        
                Screen.blit(WhiteScreen, (391, 68))
                    # 밑에 코드가 다 룰렛
                if count < 4:
                    if count == 0:
                        if a < 50:
                            a += 1
    
                    elif count == 1:
                        if a < 100:
                            a += 1
    
                    elif count == 2:
                        if a > 50:
                            a -= 1
                    elif count == 3:
                        if a > 25:
                            a -= 1
    
                    if count < 3:
                        if index <= 6:
                            Screen.blit(list_Achievement[index][0], (list_Achievement[index][2], 100))
    
                            if list_Achievement[index][2] > 403 - list_Achievement[index][1]:
                                list_Achievement[index][2] -= a
                            else:
                                list_Achievement[index][2] = 871
                                index += 1
                                if index == 7:
                                    index = 0
                                    count += 1
                    else:
                        if index <= c_index:
                            Screen.blit(list_Achievement[index][0], (list_Achievement[index][2], 100))
    
                            if index < c_index:
    
                                if list_Achievement[index][2] > 403 - list_Achievement[index][1]:
                                    list_Achievement[index][2] -= a
                                else:
                                    index += 1
                            else:
                                if list_Achievement[index][2] > 403:
                                    list_Achievement[index][2] -= a
                                else:
                                    if pygame.mixer.music.get_busy():  # like this!
                                        pygame.mixer.music.stop()
                                        Tada.play()
                                        count += 1

                Screen.blit(list_Achievement[c_index][0], (list_Achievement[c_index][2], 100))
                Screen.blit(Background_Laft, (0, 112))
                Screen.blit(Background_Right, (870, 112))
                Screen.blit(Background_Middle, (363, 43))
        ######################################################################
            for temp, tempRect, isLeft, _, _ in queue_Node:
                # 왼쪽 노드라면
                if isLeft:
                    if tempRect.left >= (1280 / 2) - (temp.get_rect().width / 2):
                        queue_Node.pop(0)
                        if NodeCount != 0:
                            Percentage = round(PlusScore / NodeCount * 100)  # 정확도

                        # 콤보가 끊겼을 때, Max콤보를 업데이트하는 코드
                        if ComboMax < ComboNum:
                            ComboMax = ComboNum
                        Combo_FontSize = 0
                        ComboNum = 0

                # 오른쪽 노드라면
                else:
                    if tempRect.right <= (1280 / 2) + (temp.get_rect().width / 2):
                        queue_Node.pop(0)
                        if NodeCount != 0:
                            Percentage = round(PlusScore / NodeCount * 100)  # 정확도

                        # 콤보가 끊겼을 때, Max콤보를 업데이트하는 코드
                        if ComboMax < ComboNum:
                            ComboMax = ComboNum
                        Combo_FontSize = 0
                        ComboNum = 0
        ######################################################################
            # 경과 시간(ms)을 1000으로 나누어서 초(s) 단위로 표시
            Elapsed_Time = (pygame.time.get_ticks() - Start_Ticks) / 1000
            # 출력할 글자, True, 글자 색상

            Minutes = int(Elapsed_Time / 60)
            Seconds = int(Elapsed_Time % 60)

            if Seconds < 10:
                timer = Timer_Font.render(str(Minutes) + ":0" + str(Seconds), True, BLACK)
            else:
                timer = Timer_Font.render(str(Minutes) + ":" + str(Seconds), True, BLACK)
            

            MusicName = Music_Font.render(SongName, True, BLACK) # 음악 제목
            ScoreNum = Percentage_Font.render(str(Percentage) + " %", True, BLACK) # 점수

            Screen.blit(MusicName, (10, 45))
            Screen.blit(timer, (265, 55))
            Screen.blit(ScoreNum, (1160, 45))

            # 콤보수가 1이상일 경우, 화면에 나오게하는 코드
            if ComboNum >= 1:  # 콤보가 1 이상일 경우
                if (Combo_FontSize != 100):  # 폰트 크기 설정
                    Combo_FontSize += 20
                ComboNum_Font = pygame.font.Font("Rhythm/Font/CookieRun Black.ttf", Combo_FontSize)
                Combo = ComboNum_Font.render(str(ComboNum) + " COMBO", True, WHITE)
                ComboRect = Combo.get_rect(center=(Screen_Width / 2, Screen_Height / 2 + 300))  # 콤보 폰트의 센터 설정
                Screen.blit(Combo, ComboRect)

            pygame.draw.rect(Screen, (0, 0, 0), [12, 10, 1256, 25], 3) # 타이머바 틀
            pygame.draw.rect(Screen, (255, 255, 255), [15, 13, Elapsed_Time * 7.70, 19]) # 타이머바

        ######################################################################
            # 노드가 나오는 간격을 잡아주는 코드
            Elapsed_Time = (pygame.time.get_ticks() - Start_Ticks) / 1000

            if (SectionNum == 1):
                if (Elapsed_Time < SongSection[0][0]):
                    Song_DelaySec = SongSection[0][1]
                    SectionNum += 1


            elif (1 < SectionNum < len(SongSection) + 1):
                if (SongSection[SectionNum - 2][0] < Elapsed_Time < SongSection[SectionNum - 1][0]):
                    Song_DelaySec = SongSection[SectionNum - 1][1]
                elif (Elapsed_Time == SongSection[SectionNum - 1][0]):
                    SectionNum += 1
                    #################################

                # 그 간격에 따라서 노드가 나오도록 설정
                if PlayOn == 1 and NodeOn == 1:
                    Now_Time = pygame.time.get_ticks()
                    if (Now_Time > Song_Time + Song_DelaySec):
                        Song_Time = Now_Time
                        ###################### 노드 추가 ##########################
                        if Pose_Index == -1:
                            Pose_Index = random.randrange(0, MAX_POSE)
                            Node_Index = 0
    
                        NodeCount += 1 # 노드가 추가되었으니 현재까지 나온 노드 수를 1 더해준다.
                        # 왼쪽 노드 추가하기
                        if random.randrange(0, 2):
                            queue_Node.append(MakeNode(1, Pose_Index, Node_Index))
                            NodeBGM.play()
    
                        # 오른쪽 노드 추가하기
                        else:
                            queue_Node.append(MakeNode(0, Pose_Index, Node_Index))
                            NodeBGM.play()
    
                        Node_Index += 1
                        if Node_Index == 2:
                            Pose_Index = -1


            # fade in
            FadeIn.set_alpha(OpacityLevel)
            Screen.blit(FadeIn, (0, 0))

            if (OpacityLevel > 0):
                OpacityLevel -= 3

            Clock.tick(30)
            
            pygame.display.flip()
            pygame.display.update()

        cap.release()
        cv.destroyAllWindows()
        pygame.mixer.music.stop()
