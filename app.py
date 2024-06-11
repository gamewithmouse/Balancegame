import random
import sys

import requests

import pygame
from resources import core

pygame.init()

DISPLAYWIDTH = 1280
DISPLAYHEIGHT = 720

FPS = 60

display = pygame.display.set_mode((DISPLAYWIDTH, DISPLAYHEIGHT))



basicfont = pygame.font.Font("./resources/fonts/NanumGothic-Bold.ttf", 50)

smallfont = pygame.font.Font("./resources/fonts/NanumGothic-Bold.ttf", 30)

MARGIN = 100

clock = pygame.time.Clock()

CHOOSE_RECT_WIDTH = (DISPLAYWIDTH - MARGIN * 3) / 2
CHOOSE_RECT_HEIGHT = (DISPLAYHEIGHT - MARGIN * 2)

SELECT_RECT_H_COUNT = 5
SELECT_RECT_H_MARGIN = 50
SELECT_RECT_V_MARGIN = 70
SELECT_RECT_WIDTH = (DISPLAYWIDTH - (SELECT_RECT_H_MARGIN * (SELECT_RECT_H_COUNT + 1))) // SELECT_RECT_H_COUNT
SELECT_RECT_HEIGHT = 200

background = pygame.transform.scale(pygame.image.load("resources/images/wood.jpg"), (DISPLAYWIDTH, DISPLAYHEIGHT))
play_button = pygame.transform.scale(pygame.image.load("resources/images/morden_play_button.png"), (SELECT_RECT_WIDTH - 20, (SELECT_RECT_WIDTH - 20) / 200 * 60))

def showtextscreencenter( pos, text, color, font):
    textsurf = font.render(text, True, color)
    textrect = textsurf.get_rect()
    textrect.center = pos

    display.blit(textsurf, textrect)

class Button:
    def __init__(self, x, y, w, h, image=None, text=None, color=(50, 50, 50, 0), font=None, ):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.image = pygame.transform.scale(image, (w, h))
        self.text = text
        self.font = font

        self.rect = pygame.Rect(x, y, w, h)
        assert image == None or text == None, "Image and text shouldn't None"

    def draw(self):

        if not self.image:

            showtextscreencenter(self.rect.center, self.text, self.color, self.font)
        else:
            display.blit(self.image, self.rect)

    def click(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:

            if self.rect.collidepoint(event.pos):
                return True

        return False

def gettextsurf(pos, text, font, color):
    textsurf = font.render(text, True, color)
    textrect = textsurf.get_rect()
    textrect.center = pos
    return textsurf, textrect


def rungame(choice):
    _core = core.BalanceCore(choice)

    show_surf = pygame.Surface((DISPLAYWIDTH, DISPLAYHEIGHT)).convert_alpha()
    rect1 = pygame.draw.rect(show_surf, (200, 200, 200), (MARGIN, MARGIN, CHOOSE_RECT_WIDTH, CHOOSE_RECT_HEIGHT))
    rect2 = pygame.draw.rect(show_surf, (200, 200, 200),
                             (MARGIN + CHOOSE_RECT_WIDTH + MARGIN, MARGIN, CHOOSE_RECT_WIDTH, CHOOSE_RECT_HEIGHT))
    text1, text2 = processchoice(_core)
    alpha = 255
    while True:
        display.blit(background, (0, 0))
        show_surf.blit(background, (0, 0))
        pygame.draw.rect(show_surf, (200, 200, 200), (MARGIN, MARGIN, CHOOSE_RECT_WIDTH, CHOOSE_RECT_HEIGHT))
        pygame.draw.rect(show_surf, (200, 200, 200),

                         (MARGIN + CHOOSE_RECT_WIDTH + MARGIN, MARGIN, CHOOSE_RECT_WIDTH, CHOOSE_RECT_HEIGHT))
        show_surf.blit(*gettextsurf(rect1.center, text1, basicfont, (50, 50, 50)))
        show_surf.blit(*gettextsurf(rect2.center, text2, basicfont, (50, 50, 50)))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if rect1.collidepoint(event.pos):
                    _core.choose(0)

                    text1, text2 = processchoice(_core)

                    alpha = 0
                if rect2.collidepoint(event.pos):
                    _core.choose(1)
                    text1, text2 = processchoice(_core)
                    alpha = 0

        show_surf.set_alpha(alpha)
        if alpha < 255:
            alpha += 15
        display.blit(show_surf, (0, 0))
        clock.tick(FPS)
        pygame.display.update()


def quit():
    pygame.quit()
    sys.exit()


def processchoice(core_: core.BalanceCore):
    choice = core_.get_choice()
    if choice["stats"] == "won":
        print(choice["result"][0] + "이김")
        quit()
    return choice["result"]


choice_list = ["마플", "운터", "꾸몽", "유성", "파크모", "아이리스", "김만덕", "잠뜰", "덕개", "티티", "소피", "만두민", "코마", "뚜뚜형", "꼬예유", "깔수"]

def main():
    response = requests.get("http://127.0.0.1:5000/get_choice_list").json()
    print(response)

    buttons = []


    for i in range(len(response["result"])):
        x = (SELECT_RECT_WIDTH + SELECT_RECT_H_MARGIN) * (i % SELECT_RECT_H_COUNT) + SELECT_RECT_H_MARGIN
        y = (SELECT_RECT_HEIGHT + SELECT_RECT_V_MARGIN) * (i // SELECT_RECT_H_COUNT) + SELECT_RECT_V_MARGIN
        buttons.append(Button(x + 10, y + SELECT_RECT_HEIGHT - 70, play_button.get_width(), play_button.get_height(), play_button))




    while True:
        display.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            for i, button in enumerate(buttons):
                if button.click(event):
                    params = {"id" : response["result"][i]["id"]}
                    response2 = requests.get("http://127.0.0.1:5000/get_choice", params=params).json()
                    choices = response2["result"]
                    random.shuffle(choices)
                    rungame(choices )
        for i, item in enumerate(response["result"]):
            x = (SELECT_RECT_WIDTH + SELECT_RECT_H_MARGIN) * (i % SELECT_RECT_H_COUNT) + SELECT_RECT_H_MARGIN
            y = (SELECT_RECT_HEIGHT + SELECT_RECT_V_MARGIN) * (i // SELECT_RECT_H_COUNT) + SELECT_RECT_V_MARGIN

            pygame.draw.rect(display, (230, 230, 230), (x, y, SELECT_RECT_WIDTH, SELECT_RECT_HEIGHT))
            showtextscreencenter((x + SELECT_RECT_WIDTH // 2, y + 40), item["name"], (50, 50, 50), smallfont)

        for button in buttons:

            button.draw()
        pygame.display.update()

random.shuffle(choice_list)
# rungame(choice_list)
main()
