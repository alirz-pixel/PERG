# -*- coding: utf-8 -*-
"""
Created on Sat May  1 20:28:14 2021

@author: USER
"""

# -*- coding: utf-8 -*-
"""
Created on Sat May  1 16:37:11 2021
@author: USER
"""
import cv2 as cv
import pygame
import random
import sys

BLACK = (0, 0, 0)

list_NodeColor = ['node/RedNode.png', 'node/YellowNode.png', 'node/BlueNode.png', 'node/PurpleNode.png']

def MakeNode(isLeft = True, ColorNum = 0):
    NodeColor = list_NodeColor[ColorNum]
    Node = pygame.image.load(NodeColor).convert_alpha()
    
        
    Node = pygame.transform.scale(Node, (60, 180))
    NodeRect = Node.get_rect()
    NodeRect.top = 540

    NodeRect.right = 1280
    if isLeft:
        NodeRect.left = 0

    return Node, NodeRect


# OpenCV 기본 초기화
#cap = cv.VideoCapture(0)

# 기본 초기화 (반드시 해야 하는 것들)
pygame.init()
######################################################################
# 화면 크기 설정
Screen_Width = 1280 # 가로 크기
Screen_Height = 720 # 세로 크기
Screen = pygame.display.set_mode((Screen_Width, Screen_Height))
    
# 화면 타이틀 설정
pygame.display.set_caption("방구석 트레이너") # 게임 이름
######################################################################
# FPS
Clock = pygame.time.Clock()
######################################################################
# 배경 이미지 불러오기
Background_Delay = 3000
Background_Time = 0
Background_Index = 0
list_Background = [pygame.image.load("Rhythm/ScreenBlue.PNG").convert_alpha(),
                   pygame.image.load("Rhythm/ScreenSkyblue.PNG").convert_alpha(),
                   pygame.image.load("Rhythm/ScreenOrange.PNG").convert_alpha(),
                   pygame.image.load("Rhythm/ScreenPurple.PNG").convert_alpha(),
                   pygame.image.load("Rhythm/ScreenPink.PNG").convert_alpha(),
                   pygame.image.load("Rhythm/ScreenYellow.PNG").convert_alpha(),
                   pygame.image.load("Rhythm/ScreenGreen.PNG").convert_alpha()]

for i in range(len(list_Background)):
    list_Background[i] = pygame.transform.scale(list_Background[i], (Screen_Width, Screen_Height))

# 배경 왼/오른쪽 이미지 불러오기
Background_Laft = pygame.image.load("Rhythm/SmartphoneLeftScreen.png").convert_alpha()
Background_Laft = pygame.transform.scale(Background_Laft, (405, 605))

Background_Right = pygame.image.load("Rhythm/SmartphoneRightScreen.png").convert_alpha()
Background_Right = pygame.transform.scale(Background_Right, (377, 605))


BlackScreen = pygame.image.load("Rhythm/BlackScreen.png").convert_alpha()
BlackScreen = pygame.transform.scale(BlackScreen, (Screen_Width, Screen_Height))

# 배경음악
pygame.mixer.music.load("node/Funky Souls.mp3")
# 효과음
ScratchLongBGM = pygame.mixer.Sound('node/djscratch_long.mp3')
ScratchShortBGM = pygame.mixer.Sound('node/djscratch_short.mp3')
######################################################################
# 시간 계산
Start_Ticks = pygame.time.get_ticks()
######################################################################
Timer_Font = pygame.font.Font("Rhythm/CookieRun Regular.ttf", 30) # 폰트 객체 생성(폰트, 크기)
Music_Font = pygame.font.Font("Rhythm/CookieRun Bold.ttf", 40)
Artist_Font = pygame.font.Font("Rhythm/CookieRun Regular.ttf", 30)
Percentage_Font = pygame.font.Font("Rhythm/CookieRun Bold.ttf", 40)
######################################################################
Minus_Score = 0
Percentage = 100
queue1 = []
queue2 = []


PlayOn = 1
TurnOn = 0
BeatHeart = 1
OpacityLevel = 255
Crashed = False
######################################################################
while not Crashed: 
    dt = Clock.tick(30)
    Elapsed_Time = (pygame.time.get_ticks() - Start_Ticks) / 1000
    for event in pygame.event.get(): # 어떤 이벤트가 발생하였는가?
        if event.type == pygame.QUIT: # 창이 닫히는 이벤트가 발생하였는가?
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(pygame.mouse.get_pos())
        if event.type == pygame.KEYDOWN: # 키가 눌렸는지 확인
            if event.key == pygame.K_UP: # 위쪽 방향키
                print(float(Elapsed_Time))
                for temp, tempRect in queue1:
                    if tempRect.left >= (1280 / 2) - 100 and tempRect.left <= (1280 / 2) + 100:
                        ScratchLongBGM.play()
                        queue1.pop(0)
                        queue2.pop(0)
                    else:
                        Minus_Score += 1

######################################################################
                        
#    _, frame = cap.read()
#    frame = frame[0:480, 183:456]
#    cv.imwrite('Frame.png', frame)


#    py_Frame = pygame.image.load("Frame.png").convert_alpha()
#    py_Frame = pygame.transform.scale(py_Frame, (478, 771))
#    Screen.blit(py_Frame, (399, 111))

######################################################################
    # 화면 색깔 변환
    Now_Time = pygame.time.get_ticks()
    if (Now_Time > Background_Time + Background_Delay):
        Background_Time = Now_Time
        Background_Index += 1
        if (Background_Index >= len(list_Background)):
            Background_Index = 0
    Screen.blit(list_Background[Background_Index], (0, 0)) # 배경 그리기

    Screen.blit(Background_Laft, (0, 112))
    Screen.blit(Background_Right, (870, 112))
######################################################################
    for temp, tempRect in queue1:
        if tempRect.left >= (1280 / 2) - 60 and tempRect.left <= (1280 / 2) + 60:
            queue1.pop(0)
            queue2.pop(0)
            
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
    MusicName = Music_Font.render("Funky Souls", True, BLACK) # 음악 제목
    ArtistName = Artist_Font.render("Amaria", True, BLACK) # 작곡가 제목
    ScoreNum = Percentage_Font.render(str(Percentage) + " %", True, BLACK) # 점수
    
    Screen.blit(MusicName, (10, 45))
    Screen.blit(ArtistName, (10, 105))
    Screen.blit(timer, (130, 106))
    Screen.blit(ScoreNum, (10, 155)) 
    

    pygame.draw.rect(Screen, (0, 0, 0), [12, 10, 1256, 25], 3) # 타이머바 틀
    pygame.draw.rect(Screen, (255, 255, 255), [15, 13, Elapsed_Time * 7.70, 19]) # 타이머바
######################################################################    
    # 노래에 따른 노드 타이밍 설정
    ColorNum = random.randrange(0, 4)

    # 화면에 노드 추가하기
    if (float(Elapsed_Time) >= 2.8 and float(Elapsed_Time) <= 3):
        if TurnOn == 0:
            queue1.append(MakeNode(True, ColorNum))
            queue2.append(MakeNode(False, ColorNum))
            ScratchShortBGM.play()
            TurnOn += 1
    
    # 노드를 중앙으로 움직이기
    for i in range(0, len(queue1)):
        queue1[i][1].left += 30
        queue2[i][1].right -= 30
    
    # 노드를 화면에 출력하기
    for temp, tempRect in queue1:
        Screen.blit(temp, tempRect)
        
    for temp, tempRect in queue2:
        Screen.blit(temp, tempRect)

######################################################################

######################################################################

   
    # fade out
    BlackScreen.set_alpha(OpacityLevel)
    Screen.blit(BlackScreen, (0, 0))
    
    if (OpacityLevel > 0):
        OpacityLevel -= 3
    
    pygame.display.flip()
    pygame.display.update()
    

pygame.quit()
sys.exit()
