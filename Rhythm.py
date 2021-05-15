'''
2021-05-13  14:41  Rhythm.py 모듈화 (소스코드 분할) - 최문형
2021-05-15  11:32  정확도 계산 코드 작성 - 김창현
2021-05-15  11:57  노드 타이밍 및 음악 가져오는 소스코드 병합 - 최문형
'''

import SongLoad as SL
import cv2 as cv
import pygame
import random
import sys

def start(Screen):
    BLACK = (0, 0, 0)
    BLUE = (0, 199, 254)
    GREEN = (35, 226, 11)
    PINK = (251, 64, 174)

    COLORS = [BLUE, GREEN, PINK]


    ######################################################################
    # 화면 크기
    Screen_Width = 1280  # 가로 크기
    Screen_Height = 720  # 세로 크기

    ######################################################################
    # 노드 관련
    lunge1 = pygame.image.load('Rhythm/Upper_Pose/lunge2.png').convert_alpha()
    lunge1 = pygame.transform.scale(lunge1, (int(lunge1.get_rect().width / 1.5), int(lunge1.get_rect().height / 1.5)))

    lunge2 = pygame.image.load('Rhythm/Upper_Pose/lunge1.png').convert_alpha()
    lunge2 = pygame.transform.scale(lunge2, (int(lunge2.get_rect().width / 1.5), int(lunge2.get_rect().height / 1.5)))

    bigclap1 = pygame.image.load('Rhythm/Upper_Pose/bigclap1.png').convert_alpha()
    bigclap1 = pygame.transform.scale(bigclap1, (int(bigclap1.get_rect().width / 1.5), int(bigclap1.get_rect().height / 1.5)))

    bigclap2 = pygame.image.load('Rhythm/Upper_Pose/bigclap2.png').convert_alpha()
    bigclap2 = pygame.transform.scale(bigclap2, (int(bigclap2.get_rect().width / 1.5), int(bigclap2.get_rect().height / 1.5)))

    list_Node = [[lunge1, lunge2],
                 [bigclap1, bigclap2]]
    ######################################################################

    Pose_Index = -1
    Node_Index = -1

    def MakeNode(isLeft, Index1 = 0, Index2 = 0):
        NodeRect = list_Node[Index1][Index2].get_rect()
        NodeRect.top = 150

        NodeRect.right = Screen_Width + list_Node[Index1][Index2].get_width()
        if isLeft:
            NodeRect.left = 0 - list_Node[Index1][Index2].get_width()

        return [list_Node[Index1][Index2], NodeRect, isLeft]


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

    # 배경 왼/오른쪽/가운데 이미지 불러오기
    Background_Middle = pygame.image.load("Rhythm/Screen/Smartphone.png").convert_alpha()
    Background_Middle = pygame.transform.scale(Background_Middle, (545, 808))

    Background_Laft = pygame.image.load("Rhythm/Screen/SmartphoneLeftScreen.png").convert_alpha()
    Background_Laft = pygame.transform.scale(Background_Laft, (405, 607))

    Background_Right = pygame.image.load("Rhythm/Screen/SmartphoneRightScreen.png").convert_alpha()
    Background_Right = pygame.transform.scale(Background_Right, (410, 607))


    BlackScreen = pygame.image.load("Rhythm/Screen/BlackScreen.png").convert_alpha()
    BlackScreen = pygame.transform.scale(BlackScreen, (1700, Screen_Height))

    #배경 위쪽의 그림자 생성
    ShadowRect = pygame.image.load("Rhythm/Screen/BlackScreen.png")
    ShadowRect = pygame.transform.scale(ShadowRect, (Screen_Width, 6))

    ######################################################################
    # 배경음악
    SectionNum = 1
    Song_Time = 0

    musicIndex = 2
    music, SongSection, SongName = SL.LoadSong(musicIndex)

    pygame.mixer.music.load(music)
    ######################################################################
    # 시간 계산
    Start_Ticks = pygame.time.get_ticks()
    ######################################################################
    Timer_Font = pygame.font.Font("Rhythm/Font/CookieRun Regular.ttf", 30) # 폰트 객체 생성(폰트, 크기)
    Music_Font = pygame.font.Font("Rhythm/Font/CookieRun Bold.ttf", 40)
    Percentage_Font = pygame.font.Font("Rhythm/Font/CookieRun Bold.ttf", 40)
    ######################################################################
    Minus_Score = 0
    Percentage = 100
    queue_Node = []

    x = 1
    PlayOn = 1
    OpacityLevel = 255
    Crashed = False
    ######################################################################
    while not Crashed:
        dt = Clock.tick(30)
        Elapsed_Time = (pygame.time.get_ticks() - Start_Ticks) / 1000
        for event in pygame.event.get(): # 어떤 이벤트가 발생하였는가?
            if event.type == pygame.QUIT: # 창이 닫히는 이벤트가 발생하였는가?
                Crashed = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                #print(pygame.mouse.get_pos())

                if Pose_Index == -1:
                    Pose_Index = random.randrange(0, 2)
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
                    except:
                        pass

            if event.type == pygame.KEYDOWN: # 키가 눌렸는지 확인
                if event.key == pygame.K_UP: # 위쪽 방향키
                    try:
                        if queue_Node[0][2] == 1: # 왼쪽에서 노드가 나옸다면
                            if 372 in range(queue_Node[0][1].left, queue_Node[0][1].left + queue_Node[0][1].width):
                                queue_Node.pop(0)
                                print("Left_Yes!")
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

        # 노드를 중앙으로 움직이기
        for i in range(len(queue_Node)):
            # 만약 왼쪽 노드라면
            if queue_Node[i][2] == 1:
                queue_Node[i][1].left += 20

            # 만약 오른쪽 노드라면
            else:
                queue_Node[i][1].right -= 20

        # 노드를 화면에 출력하기
        for temp, tempRect, _ in queue_Node:
            Screen.blit(temp, tempRect)

    ######################################################################

        # 사용자 캠 불러오기
        _, frame = cap.read()
        frame = frame[0:480, 153:486]
        cv.imwrite('Frame.png', frame)

        py_Frame = pygame.image.load("Frame.png").convert_alpha()
        py_Frame = pygame.transform.scale(py_Frame, (478, 771))
        Screen.blit(py_Frame, (399, 111))
        Screen.blit(Background_Middle, (363, 43))

    ######################################################################
        for temp, tempRect, isLeft in queue_Node:
            # 왼쪽 노드라면
            if isLeft:
                if tempRect.left >= (1280 / 2) - (temp.get_rect().width / 2):
                    queue_Node.pop(0)

            # 오른쪽 노드라면
            else:
                if tempRect.right <= (1280 / 2) + (temp.get_rect().width / 2):
                    queue_Node.pop(0)

        if not pygame.mixer.music.get_busy(): #like this!
            if PlayOn == 1:
                pygame.mixer.music.play()
                PlayOn -= 1
            else:
                Crashed = True
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



        Percentage = round((3 - Minus_Score) / 3 * 100) # 정확도
        MusicName = Music_Font.render(SongName, True, BLACK) # 음악 제목
        ScoreNum = Percentage_Font.render(str(Percentage) + " %", True, BLACK) # 점수

        Screen.blit(MusicName, (10, 45))
        Screen.blit(timer, (265, 55))
        Screen.blit(ScoreNum, (1160, 45))


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
            Now_Time = pygame.time.get_ticks()
            if (Now_Time > Song_Time + Song_DelaySec):
                Song_Time = Now_Time
                ###################### 노드 추가 ##########################
                if Pose_Index == -1:
                    Pose_Index = random.randrange(0, 2)
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


        # fade out
        BlackScreen.set_alpha(OpacityLevel)
        Screen.blit(BlackScreen, (0, 0))

        if (OpacityLevel > 0):
            OpacityLevel -= 3

        pygame.display.flip()
        pygame.display.update()

    pygame.mixer.music.stop()