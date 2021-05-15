'''
copyright : 최문형
2021.05.13  3:48   -  메인메뉴 -> 리듬게임 실행 + 페이드 아웃 구현
'''

import Pygame_Opening as Opening
import Rhythm as Game
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

        py_clock.tick(60)

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

#################################################
py_clock = pygame.time.Clock()

Opening.Func_Openning(Screen)
Opening.Func_Title(Screen)
running = True
while running:
    isButton = False
    Click = False

    # pygame 이벤트
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            Click = True

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
                if i == 1:
                    Func_FadeOut(Screen)

                    Game.start(Screen)

                print(i)

    if not isButton:
        Screen.blit(Cursor[0], (Cursor_x, Cursor_y))


    py_clock.tick(60)

    pygame.display.flip()
    pygame.display.update()

pygame.quit()
sys.exit()
