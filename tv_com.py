import pygame
from pygame.math import Vector2
import random
import socket
import threading

stop = False

def manage_stop():
    global stop
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('192.168.34.12', 8080))
    while True:
        data, addr = server_socket.recvfrom(1024)
        message = data.decode()
        if message == 'stopgame':
            stop = True


threading.Thread(target=manage_stop).start()

pygame.init()

FPS = 60
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(SCREEN_SIZE, pygame.FULLSCREEN)
clock = pygame.time.Clock()
dansu = pygame.transform.scale(pygame.image.load('9163.png'), SCREEN_SIZE)


def dansu_open(*_):
    screen.blit(dansu, (0, 0))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            pass
        clock.tick(FPS)


def draw_text(text, *, center=None, size=None, color=None):
    font = pygame.font.Font("D2Coding.ttf", size or 24)
    text = font.render(text, True, color or (255, 255, 255))
    if center is None:
        text_rect = text.get_rect()
        text_rect.centerx = SCREEN_WIDTH // 2
        text_rect.centery = SCREEN_HEIGHT // 2
    else:
        text_rect = text.get_rect(center=center)
    screen.blit(text, text_rect)


speed = 2.5
tanmak_img = pygame.transform.scale(pygame.image.load('tanmak.png'), (25, 25))
tanmak_size = Vector2(tanmak_img.get_size())


class tanmak:
    def __init__(self):
        self.pos = Vector2(random.random() * SCREEN_WIDTH, -100) - tanmak_size / 2
        self.move = Vector2((random.random() - 0.5), speed)

    def go(self):
        self.pos += self.move

    def draw(self):
        screen.blit(tanmak_img, self.pos)

    def kill_player(self, pos):
        if (self.pos - pos).length() < 23:
            return True
        return False


player_img = pygame.transform.scale(pygame.image.load('player.png'), (25, 25))
player_size = Vector2(tanmak_img.get_size())


class player:
    def __init__(self):
        self.pos = Vector2(SCREEN_SIZE) / 2 - tanmak_size / 2
        self.movement=Vector2(0, 0)

    def go(self, movement:Vector2):
        movement_real=self.movement*0.85+movement*0.15
        self.movement=movement_real
        self.pos += movement_real
        if self.pos.x < 0:
            self.pos.x = 0
        if self.pos.x > SCREEN_WIDTH - player_size.x:
            self.pos.x = SCREEN_WIDTH - player_size.x
        if self.pos.y < 0:
            self.pos.y = 0
        if self.pos.y > SCREEN_HEIGHT - player_size.y:
            self.pos.y = SCREEN_HEIGHT - player_size.y

    def draw(self):
        screen.blit(player_img, self.pos)


def ending(point):
    music=pygame.mixer.Sound('mus_gameover.ogg')
    music.play()
    screen.fill('#000000')
    draw_text('게임 오버', center=Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 100), size=60)
    draw_text(f'점수 : {point}', center=Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), size=60)
    draw_text('X를 눌러서 다시 시작', center=Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 100), size=60)
    pygame.display.update()
    while True:
        if stop:
            music.stop()
            return dansu_open, ()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    music.stop()
                    return game, ()
        clock.tick(FPS)


def game(*_):
    sound = pygame.mixer.Sound('mus_zz_megalovania.ogg')
    sound.play(-1)
    move = [0, 0, 0, 0]
    tanmak_list = []
    start = int((SCREEN_HEIGHT + 100) / speed)
    tan_regen_speed = 0.1
    tann = 0
    play = player()
    point = 0
    while True:
        if stop:
            sound.stop()
            return dansu_open, ()
        point += 1
        screen.fill('#000000')
        tann += tan_regen_speed
        if tann >= 1:
            tanmak_list.insert(0, tanmak())
            tann -= 1
        for tan in tanmak_list:
            if tan.kill_player(play.pos):
                sound.stop()
                return ending, (point,)
            tan.draw()
            tan.go()
        if tanmak_list:
            if tanmak_list[-1].pos.y>SCREEN_HEIGHT+100:
                tanmak_list.pop()

        if point < 600 * 1:
            tan_regen_speed = 0.1
        elif point < 600 * 2:
            tan_regen_speed = 0.2
        elif point < 600 * 3:
            tan_regen_speed = 0.3
        elif point < 600 * 4:
            tan_regen_speed = 0.4
        elif point < 600 * 5:
            tan_regen_speed = 0.5
        elif point < 600 * 6:
            tan_regen_speed = 0.6
        elif point < 600 * 7:
            tan_regen_speed = 0.7
        elif point < 600 * 8:
            tan_regen_speed = 0.8
        elif point < 600 * 9:
            tan_regen_speed = 0.9
        elif point < 600 * 10:
            tan_regen_speed = 1

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    move[0] = 1
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    move[1] = 1
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    move[2] = 1
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    move[3] = 1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    move[0] = 0
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    move[1] = 0
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    move[2] = 0
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    move[3] = 0
        movement = Vector2((move[2] - move[3], move[1] - move[0]))
        if not (movement.x == 0 and movement.y == 0):
            movement = movement / movement.length() * 3.5
        play.go(movement)
        play.draw()
        pygame.display.update()
        clock.tick(FPS)


func = game

params = ()
while __name__ == "__main__":
    end = False
    result = func(*params)
    func, params = result
