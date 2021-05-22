'''
2021.05.15  17:15 애니메이션 코드 작성 - 김수영
2021.05.15  19:56 Pygame_MainMenu.py와 병합 - 최문형
2021.05.15  19:56 fadeout 추가 - 김수영
2021.05.15  20:32 마우스 및 버튼 추가 - 최문형
2021.05.15  21:24 위에서 추가한 fadeout 기능 병합 - 최문형
2021.05.22  03:12 ~ 07:56  Song_Image 제작 및 코드 삽입
'''

import Rhythm as Game
import pygame
import sys

# 프로그램 정보 지정
Screen_Width = 1280  # 가로 크기
Screen_Height = 720  # 세로 크기

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

def Func_Separation(Screen, Count, Cursor):
    Clock = pygame.time.Clock()
    OpacityLevel = -255

    Back_Button = pygame.Rect(36 - 53, 48 - 63, 85, 88)
    Left_Button = pygame.Rect(158 - 53, 254 - 63, 135, 88)
    Middle_Button = pygame.Rect(541 - 53, 152 - 63, 300, 310)
    Right_Button = pygame.Rect(1036 - 53, 254 - 63, 135, 88)
    BUTTON = [Back_Button, Left_Button, Middle_Button, Right_Button]

    ############################################################

    # 배경 이미지 불러오기
    BackScreen = pygame.image.load("MenuScreen/mainmenu/morning.png").convert_alpha()
    BackScreen = pygame.transform.scale(BackScreen, (1280, 720))

    UpBlue = pygame.image.load("MenuScreen/Choose/Block1.png").convert_alpha()
    UpBlue = pygame.transform.scale(UpBlue, (769, 750))

    DownBlue = pygame.image.load("MenuScreen/Choose/Block2.png").convert_alpha()
    DownBlue = pygame.transform.scale(DownBlue, (1330, 253))

    Crowd = pygame.image.load("MenuScreen/Choose/Crowd.png").convert_alpha()
    Crowd = pygame.transform.scale(Crowd, (886, 550))

    SongBlock = pygame.image.load("MenuScreen/Choose/SongBlock.png").convert_alpha()
    SongBlock = pygame.transform.scale(SongBlock, (360, 360))

    Prev = pygame.image.load("MenuScreen/Choose/PrevButton.png").convert_alpha()
    Prev = pygame.transform.scale(Prev, (150, 97))

    Next = pygame.image.load("MenuScreen/Choose/NextButton.png").convert_alpha()
    Next = pygame.transform.scale(Next, (150, 97))

    Exit = pygame.image.load("MenuScreen/Choose/ExitButton.png").convert_alpha()
    Exit = pygame.transform.scale(Exit, (84, 86))

    BodyFont = pygame.image.load("MenuScreen/Choose/BodyFont.png").convert_alpha()
    BodyFont = pygame.transform.scale(BodyFont, (326, 225))

    TopFont = pygame.image.load("MenuScreen/Choose/TopFont.png").convert_alpha()
    TopFont = pygame.transform.scale(TopFont, (326, 225))

    BottomFont = pygame.image.load("MenuScreen/Choose/BottomFont.png").convert_alpha()
    BottomFont = pygame.transform.scale(BottomFont, (326, 225))

    ############################################################
    # Song_Image (copyright 최문형)
    ImageSize = (258, 258)

    Daytime_Moon1 = pygame.image.load("MenuScreen/Choose/Song_Image/Daytime_Moon1.png").convert_alpha()
    Daytime_Moon1 = pygame.transform.scale(Daytime_Moon1, ImageSize)

    Daytime_Moon2 = pygame.image.load("MenuScreen/Choose/Song_Image/Daytime_Moon2.png").convert_alpha()
    Daytime_Moon2 = pygame.transform.scale(Daytime_Moon2, ImageSize)

    dreamer1 = pygame.image.load("MenuScreen/Choose/Song_Image/dreamer1.png").convert_alpha()
    dreamer1 = pygame.transform.scale(dreamer1, ImageSize)

    dreamer2 = pygame.image.load("MenuScreen/Choose/Song_Image/dreamer2.png").convert_alpha()
    dreamer2 = pygame.transform.scale(dreamer2, ImageSize)

    FilmClash1 = pygame.image.load("MenuScreen/Choose/Song_Image/FilmClash1.png").convert_alpha()
    FilmClash1 = pygame.transform.scale(FilmClash1, ImageSize)

    FilmClash2 = pygame.image.load("MenuScreen/Choose/Song_Image/FilmClash2.png").convert_alpha()
    FilmClash2 = pygame.transform.scale(FilmClash2, ImageSize)

    Fota1 = pygame.image.load("MenuScreen/Choose/Song_Image/FOTA1.png").convert_alpha()
    Fota1 = pygame.transform.scale(Fota1, ImageSize)

    Fota2 = pygame.image.load("MenuScreen/Choose/Song_Image/FOTA2.png").convert_alpha()
    Fota2 = pygame.transform.scale(Fota2, ImageSize)

    FunkyJunky1 = pygame.image.load("MenuScreen/Choose/Song_Image/FunkyJunky1.png").convert_alpha()
    FunkyJunky1 = pygame.transform.scale(FunkyJunky1, ImageSize)

    FunkyJunky2 = pygame.image.load("MenuScreen/Choose/Song_Image/FunkyJunky2.png").convert_alpha()
    FunkyJunky2 = pygame.transform.scale(FunkyJunky2, ImageSize)

    NewFuture1 = pygame.image.load("MenuScreen/Choose/Song_Image/NewFuture1.png").convert_alpha()
    NewFuture1 = pygame.transform.scale(NewFuture1, ImageSize)

    NewFuture2 = pygame.image.load("MenuScreen/Choose/Song_Image/NewFuture2.png").convert_alpha()
    NewFuture2 = pygame.transform.scale(NewFuture2, ImageSize)

    SpaceTown1 = pygame.image.load("MenuScreen/Choose/Song_Image/SpaceTown1.png").convert_alpha()
    SpaceTown1 = pygame.transform.scale(SpaceTown1, ImageSize)

    SpaceTown2 = pygame.image.load("MenuScreen/Choose/Song_Image/SpaceTown2.png").convert_alpha()
    SpaceTown2 = pygame.transform.scale(SpaceTown2, ImageSize)

    Tracker1 = pygame.image.load("MenuScreen/Choose/Song_Image/Tracker1.png").convert_alpha()
    Tracker1 = pygame.transform.scale(Tracker1, ImageSize)

    Tracker2 = pygame.image.load("MenuScreen/Choose/Song_Image/Tracker2.png").convert_alpha()
    Tracker2 = pygame.transform.scale(Tracker2, ImageSize)

    SwingSwing1 = pygame.image.load("MenuScreen/Choose/Song_Image/SwingSwing1.png").convert_alpha()
    SwingSwing1 = pygame.transform.scale(SwingSwing1, ImageSize)

    SwingSwing2 = pygame.image.load("MenuScreen/Choose/Song_Image/SwingSwing2.png").convert_alpha()
    SwingSwing2 = pygame.transform.scale(SwingSwing2, ImageSize)


    SongImage = [[Daytime_Moon1, Daytime_Moon2], [SwingSwing1, SwingSwing2], [Tracker1, Tracker2], [Fota1, Fota2], [NewFuture1, NewFuture2],
                 [dreamer1, dreamer2], [FilmClash1, FilmClash2], [FunkyJunky1, FunkyJunky2], [SpaceTown1, SpaceTown2]]

    SongImage_Index = 0
    SongImage_MAX = 9

    ############################################################

    # DB = DownBlue, UB = UpBlue, SB = SongBlock
    DB_Level_1_x = -20
    DB_Level_1_y = 1.2*Screen_Height + 120
    DB_Level_2_x = -20
    DB_Level_2_y = Screen_Height/2 + 170

    UB_Level_1_x = Screen_Width/2 - 365
    UB_Level_1_y = Screen_Height
    UB_Level_2_x = Screen_Width/2 - 365
    UB_Level_2_y = Screen_Height/70 - 20

    Crowd_Level_1_x = Screen_Width/2 - 420
    Crowd_Level_1_y = Screen_Height
    Crowd_Level_2_x = Screen_Width/2 - 420
    Crowd_Level_2_y = Screen_Height/2 - 20

    SB_x = Screen_Width/2 - 154
    SB_y = Screen_Height/2 - 275

    Prev_x = UB_Level_1_x - 150
    Prev_y = Screen_Height/2 - 150

    Next_x = UB_Level_1_x + 750
    Next_y = Screen_Height/2 - 150

    Exit_x = Screen_Width/2 - 630
    Exit_y = Screen_Height/2 - 360

    Font_x = Crowd_Level_2_x + 280
    Font_y = 1.5*Crowd_Level_2_y + 30

    Move_y = 3.5

    # 이벤트
    Crashed = False
    while not Crashed:
        isButton = False
        Click = False

        dt = Clock.tick(30)
        for event in pygame.event.get():  # 어떤 이벤트가 발생하였는가?
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(pygame.mouse.get_pos())
                Click = True

            if event.type == pygame.QUIT:  # 창이 닫히는 이벤트가 발생하였는가?
                pygame.quit()
                sys.exit()

        Screen.blit(BackScreen, (0, 0))
        Screen.blit(DownBlue, (DB_Level_1_x, DB_Level_1_y))
        Screen.blit(UpBlue, (UB_Level_1_x, UB_Level_1_y))
        Screen.blit(Crowd, (Crowd_Level_1_x, Crowd_Level_1_y))

        SongBlock.set_alpha(OpacityLevel)
        Screen.blit(SongBlock, (SB_x, SB_y))
        Prev.set_alpha(OpacityLevel)
        Screen.blit(Prev, (Prev_x, Prev_y))
        Next.set_alpha(OpacityLevel)
        Screen.blit(Next, (Next_x, Next_y))
        Exit.set_alpha(OpacityLevel)
        Screen.blit(Exit, (Exit_x, Exit_y))

        if Count == 0:
            TopFont.set_alpha(OpacityLevel)
            Screen.blit(TopFont, (Font_x, Font_y))

        if Count == 1:
            Screen.blit(BottomFont, (Font_x, Font_y))
            BottomFont.set_alpha(OpacityLevel)

        if Count == 2:
            BodyFont.set_alpha(OpacityLevel)
            Screen.blit(BodyFont, (Font_x, Font_y))

        if OpacityLevel <= 250:
            OpacityLevel += 18.5

        Move_y += 3.5
        if DB_Level_1_y > DB_Level_2_y:
            DB_Level_1_y -= 0.9*Move_y

        if UB_Level_1_y > UB_Level_2_y:
            UB_Level_1_y -= 1.4*Move_y

        if Crowd_Level_1_y > Crowd_Level_2_y:
            Crowd_Level_1_y -= 0.46*Move_y

        # 가운데에 들어갈 썸네일 보여주기
        SongImage_Position = (Screen_Width/2 - 103, Screen_Height/2 - 223)

        SongImage[SongImage_Index][0].set_alpha(OpacityLevel)
        Screen.blit(SongImage[SongImage_Index][0], SongImage_Position)


        # 커서의 위치 및 수정하기
        Cursor_x, Cursor_y = pygame.mouse.get_pos()  # (Screen_Width / 2 + Cursor_x, Screen_Height / 2 + Cursor_y)
        Cursor_x = Cursor_x - (Cursor[0].get_width() / 2)
        Cursor_y = Cursor_y - (Cursor[1].get_height() / 2)

        if OpacityLevel >= 250:
            for i in range(len(BUTTON)):
                if BUTTON[i].collidepoint((Cursor_x, Cursor_y)):
                    if i == 2:
                        Screen.blit(SongImage[SongImage_Index][1], SongImage_Position)

                    Screen.blit(Cursor[1], (Cursor_x, Cursor_y))
                    isButton = True

                    if Click:
                        if i == 0: # 뒤로가기 버튼 클릭
                            while True:
                                pygame.time.Clock().tick(30)

                                Screen.blit(BackScreen, (0, 0))

                                # 요소들 fade out 시키기
                                DownBlue.set_alpha(OpacityLevel)
                                Screen.blit(DownBlue, (DB_Level_1_x, DB_Level_1_y))
                                UpBlue.set_alpha(OpacityLevel)
                                Screen.blit(UpBlue, (UB_Level_1_x, UB_Level_1_y))
                                Crowd.set_alpha(OpacityLevel)
                                Screen.blit(Crowd, (Crowd_Level_1_x, Crowd_Level_1_y))
                                SongBlock.set_alpha(OpacityLevel)
                                Screen.blit(SongBlock, (SB_x, SB_y))
                                Prev.set_alpha(OpacityLevel)
                                Screen.blit(Prev, (Prev_x, Prev_y))
                                Next.set_alpha(OpacityLevel)
                                Screen.blit(Next, (Next_x, Next_y))
                                Exit.set_alpha(OpacityLevel)
                                Screen.blit(Exit, (Exit_x, Exit_y))
                                SongImage[SongImage_Index][0].set_alpha(OpacityLevel)
                                Screen.blit(SongImage[SongImage_Index][0], SongImage_Position)

                                if OpacityLevel > 0:
                                    OpacityLevel -= 18.5

                                else:
                                    break

                                pygame.display.update()

                            #MainMenu_Pose 종료
                            Crashed = True

                        if i == 2: # 가운데 클릭
                            Func_FadeOut(Screen)
                            Game.start(Screen, Count + 1, SongImage_Index + 1)
                            Crashed = True

                        if i == 1: # 왼쪽 버튼 클릭
                            SongImage_Index -= 1

                            if SongImage_Index < 0:
                                SongImage_Index = 8

                        if i == 3: # 오른쪽 버튼 클릭
                            SongImage_Index += 1

                            if SongImage_Index >= SongImage_MAX:
                                SongImage_Index = 0

        if not isButton:
            Screen.blit(Cursor[0], (Cursor_x, Cursor_y))


        pygame.display.flip()
        pygame.display.update()


