# copyright : 최문형
'''
2021-05-27  14:00 ~ 21:38  튜토리얼 완성

앞으로 추가 계획
 - 방해 노드에 대한 튜토리얼
'''

import cv2
import pygame
import mediapipe as mp
import GetPose as GP


textAlignLeft = 0
textAlignRight = 1
textAlignCenter = 2
textAlignBlock = 3


# copyright : https://stackoverflow.com/questions/42014195/rendering-text-with-multiple-lines-in-pygame
def drawText(surface, text, color, rect, font, align=textAlignLeft, aa=False, bkg=None):
    lineSpacing = -2
    spaceWidth, fontHeight = font.size(" ")[0], font.size("Tg")[1]

    listOfWords = text.split(" ")
    if bkg:
        imageList = [font.render(word, 1, color, bkg) for word in listOfWords]
        for image in imageList: image.set_colorkey(bkg)
    else:
        imageList = [font.render(word, aa, color) for word in listOfWords]

    maxLen = rect[2]
    lineLenList = [0]
    lineList = [[]]
    for image in imageList:
        width = image.get_width()
        lineLen = lineLenList[-1] + len(lineList[-1]) * spaceWidth + width
        if len(lineList[-1]) == 0 or lineLen <= maxLen:
            lineLenList[-1] += width
            lineList[-1].append(image)
        else:
            lineLenList.append(width)
            lineList.append([image])

    lineBottom = rect[1]
    lastLine = 0
    for lineLen, lineImages in zip(lineLenList, lineList):
        lineLeft = rect[0]
        if align == textAlignRight:
            lineLeft += + rect[2] - lineLen - spaceWidth * (len(lineImages)-1)
        elif align == textAlignCenter:
            lineLeft += (rect[2] - lineLen - spaceWidth * (len(lineImages)-1)) // 2
        elif align == textAlignBlock and len(lineImages) > 1:
            spaceWidth = (rect[2] - lineLen) // (len(lineImages)-1)
        if lineBottom + fontHeight > rect[1] + rect[3]:
            break
        lastLine += 1
        for i, image in enumerate(lineImages):
            x, y = lineLeft + i*spaceWidth, lineBottom
            surface.blit(image, (round(x), y))
            lineLeft += image.get_width()
        lineBottom += fontHeight + lineSpacing

    if lastLine < len(lineList):
        drawWords = sum([len(lineList[i]) for i in range(lastLine)])
        remainingText = ""
        for text in listOfWords[drawWords:]: remainingText += text + " "
        return remainingText
    return ""


def Func_Tutorial(Screen):
    # 프로그램 정보 지정
    Screen_Width = 1280  # 가로 크기
    Screen_Height = 720  # 세로 크기

    py_clock = pygame.time.Clock()


    ####################배경 관련#############################
    # 배경 왼/오른쪽/가운데 이미지 불러오기
    Background_Middle = pygame.image.load("Rhythm/Screen/Smartphone.png").convert_alpha()
    Background_Middle = pygame.transform.scale(Background_Middle, (545, 808))

    Background_Laft = pygame.image.load("Rhythm/Screen/SmartphoneLeftScreen.png").convert_alpha()
    Background_Laft = pygame.transform.scale(Background_Laft, (405, 650))

    Background_Right = pygame.image.load("Tutorial/RightScreen.png").convert_alpha()
    Background_Right = pygame.transform.scale(Background_Right, (610, 650))

    # Fadein을 구현하기 위한 코드
    fade = pygame.Surface((Screen_Width, Screen_Height))
    fade.fill((0, 0, 0))

    alpha = 300

    # 배경 위쪽의 그림자 생성
    ShadowRect = pygame.image.load("Rhythm/Screen/BlackScreen.png")
    ShadowRect = pygame.transform.scale(ShadowRect, (Screen_Width, 6))

    WhiteScreen = pygame.image.load("Rhythm/Screen/WhiteScreen.png")
    WhiteScreen = pygame.transform.scale(WhiteScreen, (478, 771))
    ########################################################


    ##################### 튜토리얼 남자 ######################
    Man = [pygame.image.load("Tutorial/defaultMan.png"),
           pygame.image.load("Tutorial/happyMan.png"),
           pygame.image.load("Tutorial/upsetMan.png")]

    Man_xPos = Screen_Width - Man[0].get_width()
    Man_yPos = Screen_Height - Man[0].get_height() + 10
    ########################################################


    ##################### 텍스트 출력하기 ######################
    textDelay = 21
    textTime = 0
    strIndex = 0
    textNum = 0

    Title_Font = pygame.font.Font("Rhythm/Font/CookieRun Bold.ttf", 32)
    Tutorial_Font = pygame.font.Font("Rhythm/Font/CookieRun Bold.ttf", 25)
    next_Font = pygame.font.Font("Rhythm/Font/CookieRun Bold.ttf", 15)
    textRect = pygame.Rect(Man_xPos - 345, Man_yPos - 150, 500, 300)

    msg = ["안녕하세요! 만나서 반갑습니다.                   저는 튜토리얼을 안내할 방구서기입니다!    ",
           "리듬 게임을 실행시키면, 오른쪽이나 왼쪽에서    운동동작이 나오게 됩니다.                     ",
           "당신은 이 운동동작이 핸드폰과 가까워졌을 때, 그것과 같은 동작을 취해주시면 됩니다.               ",
           "한번 테스트 해볼까요?              ",
           "",
           "잘 하셨습니다!                                                  이것으로 튜토리얼을 마치도록 하겠습니다.       "]
    ########################################################
    isNext = True
    nextDelay = 350
    nextTime = 0
    startTime = pygame.time.get_ticks() + 6500

    nextMsg = next_Font.render("튜토리얼을 계속 진행하시려면 아무 키나 눌러주세요", True, (166, 166, 166))
    ########################################################


    ########## 튜토리얼을 위한 운동 동작과 관련한 변수 ###########
    # 운동 동작과 관련된 변수
    isAppend = False
    isFail = False

    node = pygame.image.load("Rhythm/Body_Pose/lfb_legraise.png")
    node = pygame.transform.scale(node, (int(node.get_rect().width / 1.5), int(node.get_rect().height / 1.5)))
    nodeRect = node.get_rect()
    nodeRect.top = 150

    nodeSpeed = 40

    # 텍스트 관련
    node_MsgIndex = 0
    nodeMsg = [".....",
               "이것도 못하세요?                         ",
               "노드의 스피드를 줄여드릴테니                       ",
               "운동동작이 핸드폰과 닿았을 때,                        운동동작을 취해보세요.                 "]
    ########################################################


    cap = cv2.VideoCapture(0)
    textTime = startTime

    isFadein = True
    Crashed = False
    ######################################################################
    with mp.solutions.holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        while not Crashed:
            # pygame 이벤트
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 718 in range(nodeRect.left, nodeRect.left + node.get_width()):
                        strIndex = 5

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_t:
                        strIndex = 5
                    
                    if strIndex < 4:
                        if textNum > len(msg[strIndex]):
                            strIndex += 1
                            textNum = 0

                    if isFail:
                        if textNum > len(nodeMsg[node_MsgIndex]):
                            if node_MsgIndex == 3:
                                isFail = False
                                isAppend = False
                                node_MsgIndex = 0
                                nodeSpeed -= 5
                            else:
                                node_MsgIndex += 1

                            textNum = 0

                    if textNum > len(msg[strIndex]):
                        if strIndex == 5:
                            Crashed = True



                if event.type == pygame.QUIT:
                    Crashed = True

            Screen.fill((0, 199, 254))

            # 그림자 생성
            ShadowRect.set_alpha(70)
            Screen.blit(ShadowRect, (0, 77))
            ShadowRect.set_alpha(50)
            Screen.blit(ShadowRect, (0, 75))
            ShadowRect.set_alpha(30)
            Screen.blit(ShadowRect, (0, 72))

            # 배경 추가
            Screen.blit(Background_Laft, (-175, 82))
            Screen.blit(Background_Right, (695, 82))

            # 화면 위의 tutorial 문구 출력하기
            Screen.blit(Title_Font.render("Tutorial", True, (0, 0, 0)), (10, 30))


            # 튜토리얼을 도와주는 남자 띄우기
            Screen.blit(Man[0], (Man_xPos, Man_yPos))

            # 튜토리얼 문구
            Now_Time = pygame.time.get_ticks()

            if Now_Time >= startTime:
                if strIndex < 4 or strIndex > 4:
                    if Now_Time > textTime + textDelay:
                        textTime = Now_Time

                        if (textNum <= len(msg[strIndex])):
                            textNum += 1

                    if (textNum > len(msg[strIndex])):
                        if (Now_Time > nextTime + nextDelay):
                            nextTime = Now_Time
                            isNext = not isNext

                        if isNext:
                            Screen.blit(nextMsg, (Man_xPos - 260, Man_yPos - 65))

                    drawTextRect = textRect.inflate(-5, -5)
                    drawText(Screen, msg[strIndex][:textNum], (0, 0, 0), drawTextRect, Tutorial_Font, textAlignBlock, True)

                elif strIndex == 4:
                    if not isFail:
                        if not isAppend:
                            isAppend = True
                            nodeRect.right = int(Screen_Width + node.get_width())

                        else:
                            nodeRect.right -= nodeSpeed
                            Screen.blit(node, nodeRect)

                            if nodeRect.right <= 376 + (node.get_rect().width / 2):
                                nextTime = Now_Time
                                isFail = True

                            elif 718 in range(nodeRect.left, nodeRect.left + node.get_width()):
                                try:
                                    if (GP.Func_GetPose(Screen, holistic, 3) == "FBM 4-L" or GP.Func_GetPose(Screen, holistic, 3) == "FBM 4-R"):
                                        strIndex = 5

                                except:
                                    pass

                    else:
                        if Now_Time > textTime + textDelay:
                            textTime = Now_Time

                            if (textNum <= len(nodeMsg[node_MsgIndex])):
                                textNum += 1

                        if (textNum > len(nodeMsg[node_MsgIndex])):
                            if (Now_Time > nextTime + nextDelay):
                                nextTime = Now_Time
                                isNext = not isNext

                            if isNext:
                                Screen.blit(nextMsg, (Man_xPos - 260, Man_yPos - 65))

                        drawTextRect = textRect.inflate(-5, -5)
                        drawText(Screen, nodeMsg[node_MsgIndex][:textNum], (0, 0, 0), drawTextRect, Tutorial_Font, textAlignBlock, True)


            #사용자의 캠 인식받기
            _, frame = cap.read()
            frame = cv2.flip(frame, 1)

            frame = frame[0:480, 153:486]
            cv2.imwrite('Frame.png', frame)

            py_Frame = pygame.image.load("Frame.png").convert_alpha()
            py_Frame = pygame.transform.scale(py_Frame, (478, 700))
            Screen.blit(py_Frame, (224, 80))
            Screen.blit(Background_Middle, (188, 43))

            if isFadein:
                alpha -= 3

                fade.set_alpha(alpha)
                Screen.blit(fade, (0, 0))

                if (alpha <= 0):
                    isFadein = False


            py_clock.tick(30)

            pygame.display.flip()
            pygame.display.update()
