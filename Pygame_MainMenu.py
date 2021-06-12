'''
copyright : 최문형
2021.05.13  03:48   -  메인메뉴 -> 리듬게임 실행 + 페이드 아웃 구현 - 최문형
2021.05.15  19:56   -  메인메뉴 -> MainMenu_Pose.py -> 리듬게임 실행으로 전환 -  최문형
'''


import Pygame_Opening as Opening
import MainMenu_Pose as MMP
import tutorial as Tu
from pygame.locals import *
import pygame
import sys

def Func_FadeOut(Screen):
    fade = pygame.Surface((Screen_Width, Screen_Height))
    fade.fill((0, 0, 0))

    alpha = 0
    while True:
        alpha += 3

        fade.set_alpha(alpha)
        Screen.blit(fade, (0, 0))

        pygame.display.flip()
        pygame.display.update()

        pygame.time.Clock().tick(60)

        if (alpha == 300):
            break

# 파이게임 시작하기
pygame.init()

# 프로그램 정보 지정
Screen_Width = 1280  # 가로 크기
Screen_Height = 720  # 세로 크기
Screen = pygame.display.set_mode((Screen_Width, Screen_Height))
pygame.display.set_caption("방구석 트레이너")
pygame.mouse.set_visible(False)

# 타이틀 이미지 불러오기
Menu_Morning = pygame.image.load("MenuScreen/mainmenu/morning.PNG")
Menu_Morning = pygame.transform.scale(Menu_Morning, (Screen_Width, Screen_Height))

# 버튼 위치 설정하기
Upper_Button = pygame.Rect(28, 512, 350, 166)
Lower_Button = pygame.Rect(447, 512, 350, 166)
Whole_Button = pygame.Rect(861, 512, 350, 166)
BUTTON = [Upper_Button, Lower_Button, Whole_Button]

# 마우스 커서 추가하기
Cursor = [pygame.image.load("MenuScreen/cursor/Cursor.png"),
          pygame.image.load("MenuScreen/cursor/Cursor_Click.png")]
Cursor[0] = pygame.transform.scale(Cursor[0], (80, 91))
Cursor[1] = pygame.transform.scale(Cursor[1], (80, 91))

Click = False
isButton = False
ClickBGM = pygame.mixer.Sound("MenuScreen/sound/決定、ボタン押下39.mp3")


# 텍스트 관련 변수
text_Xpos = 0
text_Count = 1
textDelay = 3500

textFont = pygame.font.Font("Rhythm/Font/CookieRun Bold.ttf", 23)


#################################################
py_clock = pygame.time.Clock()


Opening.Func_Openning(Screen)
pygame.mixer.music.load("MenuScreen/sound/In_Rejection.mp3")
pygame.mixer.music.play(-1)
Opening.Func_Title(Screen)
pygame.mixer.music.stop()

textTime = pygame.time.get_ticks()

PlayOn = 0 # 배경음악이 켜져있는가 유무 
running = True
while running:        
    isButton = False
    Click = False
    
    if PlayOn == 0:
        pygame.mixer.music.load("MenuScreen/sound/Cat_life.mp3")
        pygame.mixer.music.play(-1)
        PlayOn += 1
    # pygame 이벤트
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            Click = True
            ClickBGM.play()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_t:
                Func_FadeOut(Screen)
                Tu.Func_Tutorial(Screen)

                textTime = pygame.time.get_ticks()
                text_Xpos = 0
                text_Count = 1
                

        if event.type == pygame.QUIT:
            running = False


    Screen.blit(Menu_Morning, (0, 0))

#################################################
    # 커서의 위치 및 수정하기
    Cursor_x, Cursor_y = pygame.mouse.get_pos() #(Screen_Width / 2 + Cursor_x, Screen_Height / 2 + Cursor_y)
    Cursor_x = Cursor_x - (Cursor[0].get_width() / 2)
    Cursor_y = Cursor_y - (Cursor[1].get_height() / 2)

    # 버튼 위에 올라가 있다면
    for i in range(len(BUTTON)):
        if BUTTON[i].collidepoint((Cursor_x, Cursor_y)):
            Screen.blit(Cursor[1], (Cursor_x, Cursor_y))
            isButton = True
            
            # 상체, 하체, 전신 게임 시작
            if Click:
                MMP.Func_Separation(Screen, i, Cursor)


    if not isButton:
        Screen.blit(Cursor[0], (Cursor_x, Cursor_y))

    Screen.blit(textFont.render("튜토리얼을 해보시려면 T를 눌러주세요", True, (0, 0, 0)), (921 + text_Xpos, 45))


    if pygame.time.get_ticks() >= textTime + textDelay:
        if text_Xpos <= 360:
            text_Xpos += (2 * text_Count)
            text_Count += 1


    py_clock.tick(60)

    pygame.display.flip()
    pygame.display.update()

pygame.quit()
sys.exit()
