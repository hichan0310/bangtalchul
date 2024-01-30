import pygame
import socket
from pygame.math import Vector2
from graphic_manager import motion_draw
pygame.init()
FPS=60
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(SCREEN_SIZE, pygame.FULLSCREEN)
clock = pygame.time.Clock()

def draw_text(scr, text, *, center=None, size=None, color=None):
    font = pygame.font.Font("D2Coding.ttf", size or 24)
    text = font.render(text, True, color or (255, 255, 255))
    if center is None:
        text_rect = text.get_rect()
        text_rect.centerx = SCREEN_WIDTH // 2
        text_rect.centery = SCREEN_HEIGHT // 2
    else:
        text_rect = text.get_rect(center=center)
    scr.blit(text, text_rect)


class button:
    def __init__(self, pos:Vector2, letter, letter_size):
        self.letter=letter
        self.img=pygame.transform.scale(pygame.image.load('button.png'), (100, 100))
        self.img_size=Vector2(self.img.get_size())
        self.pos=pos-self.img_size/2
        draw_text(self.img, letter, center=self.img_size/2, size=letter_size)


    def isclicked(self, click_pos:Vector2):
        if self.pos.x<click_pos.x<self.pos.x+100 and self.pos.y<click_pos.y<self.pos.y+100:
            return True
        return False

    def draw(self):
        screen.blit(self.img, self.pos)

class keyboard:
    def __init__(self):
        self.button_list=[
            button(Vector2(SCREEN_WIDTH/2-100, SCREEN_HEIGHT-420), '1', 60),
            button(Vector2(SCREEN_WIDTH/2, SCREEN_HEIGHT-420), '2', 60),
            button(Vector2(SCREEN_WIDTH/2+100, SCREEN_HEIGHT-420), '3', 60),
            button(Vector2(SCREEN_WIDTH/2-100, SCREEN_HEIGHT-320), '4', 60),
            button(Vector2(SCREEN_WIDTH/2, SCREEN_HEIGHT-320), '5', 60),
            button(Vector2(SCREEN_WIDTH/2+100, SCREEN_HEIGHT-320), '6', 60),
            button(Vector2(SCREEN_WIDTH/2-100, SCREEN_HEIGHT-220), '7', 60),
            button(Vector2(SCREEN_WIDTH/2, SCREEN_HEIGHT-220), '8', 60),
            button(Vector2(SCREEN_WIDTH/2+100, SCREEN_HEIGHT-220), '9', 60),
            button(Vector2(SCREEN_WIDTH/2-100, SCREEN_HEIGHT-120), '#', 50),
            button(Vector2(SCREEN_WIDTH/2, SCREEN_HEIGHT-120), '0', 60),
            button(Vector2(SCREEN_WIDTH/2+100, SCREEN_HEIGHT-120), '*', 50)
        ]

    def click_result(self, click_pos:Vector2):
        for b in self.button_list:
            if b.isclicked(click_pos):
                return b.letter
        return None

    def draw(self):
        for b in self.button_list:
            b.draw()


def success():
    socket.socket(socket.AF_INET, socket.SOCK_DGRAM).sendto('stopgame'.encode(), ('localhost', 8080))
    # 소켓통신



password='6436'
kboard=keyboard()
input_data=''

while True:
    screen.fill('#000000')
    kboard.draw()
    for event in pygame.event.get():
        if event.type==pygame.MOUSEBUTTONDOWN:
            res=kboard.click_result(Vector2(event.pos))
            if res is not None:
                if res=='*':
                    if password==input_data:
                        success()
                        for i in range(60):
                            motion_draw.add_motion(
                                lambda scr: draw_text(scr, '비밀번호가 일치합니다',
                                                      center=Vector2(SCREEN_WIDTH/2, 400), size=50),
                                i, ()
                            )
                        def tmp(scr):
                            global input_data
                            input_data=''
                        motion_draw.add_motion(tmp, 60, ())
                    else:
                        input_data=''
                        for i in range(60):
                            motion_draw.add_motion(
                                lambda scr: draw_text(scr, '비밀번호가 일치하지 않습니다',
                                                      center=Vector2(SCREEN_WIDTH / 2, 400), size=50),
                                i, ()
                            )
                elif res=='#':
                    input_data=''
                else:
                    input_data+=res
    draw_text(screen, input_data, center=Vector2(SCREEN_WIDTH/2, 230), size=80)
    motion_draw.draw(screen)
    pygame.display.update()
    clock.tick(FPS)






