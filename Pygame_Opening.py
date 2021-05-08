from pygame.locals import *
import sys
import pygame


# 프로그램 정보 지정
py_size = (1280, 720)

py_clock = pygame.time.Clock()

# 이미지 불러오기
py_openingImage0 = pygame.image.load('opening/starting screen_1.PNG')
py_openingImage0 = pygame.transform.scale(py_openingImage0, py_size)

py_openingImage1 = pygame.image.load('opening/starting_screen_2.PNG')
py_openingImage1 = pygame.transform.scale(py_openingImage1, py_size)

py_TitleImage = pygame.image.load('opening/logo.PNG')
py_TitleImage = pygame.transform.scale(py_TitleImage, py_size)

def Func_Openning(Screen):
    fade = pygame.Surface(py_size)
    fade.fill((0,0,0))

    isFadein = True
    alpha = 300

    openingScreen = 0

    running = True
    while running:
        # pygame 이벤트 조사
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    openingScreen += 1
                    isFadein = True
                    alpha = 300

        # 오프닝 화면 출력
        if openingScreen == 0:
            Screen.blit(py_openingImage0, (0, 0))
        elif openingScreen == 1:
            Screen.blit(py_openingImage1, (0, 0))
        else:
            running = False


        # 검정색이고 투명도가 alpha인 화면 세팅
        fade.set_alpha(alpha)
        Screen.blit(fade, (0, 0))

        # 투명도를 낮추거나 높임
        if isFadein:
            alpha -= 3
        else:
            alpha += 3

        # fade in, 또는 fade out인지 설정
        if alpha == 0:
            isFadein = False

        elif alpha == 300:
            isFadein = True
            openingScreen += 1

        py_clock.tick(60)

        pygame.display.flip()
        pygame.display.update()


def Func_Title(Screen):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                running = False

        else:
            Screen.blit(py_TitleImage, (0, 0))

        py_clock.tick(60)

        pygame.display.flip()
        pygame.display.update()
