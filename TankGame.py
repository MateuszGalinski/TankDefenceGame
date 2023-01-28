'''
Game made by: Mateusz Galiński
All photos used are self made
Game is about defending your tank from oncoming objects
'''
import sys
import pygame
import math
from pygame.math import Vector2
import random

# Global constants
WINDOW_SIZE = (1024, 768)
SPRITE_SIZE = (90, 90)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
P_STEP = 2
# Global variables
game = False
Lost = False
score = 0


def draw_welcome_menu(scr, win, cursor_img_surf, cursor_img_rect):
    '''
    function draws welcome menu
    '''
    global msg_box_start
    global msg_box_quit
    menufont = pygame.font.Font('introrustg-base2line.ttf', 44)
    startfont = pygame.font.Font('introrustg-base2line.ttf', 30)
    scr.fill(WHITE)

    menu = menufont.render("WELCOME TO TANK DEFENCE", True, BLACK, None)
    msg_box_menu = menu.get_rect()
    msg_box_menu.center = (win.w/2, win.h/3)
    start_button = startfont.render("START", True, BLACK)
    quit_button = startfont.render("QUIT", True, BLACK)
    msg_box_start = start_button.get_rect()
    msg_box_quit = quit_button.get_rect()
    msg_box_start.center = (1/3*win.w, 2/3*win.h)
    msg_box_quit.center = (2/3*win.w, 2/3*win.h)

    cursor_img_rect.center = pygame.mouse.get_pos()
    scr.blit(cursor_img_surf, cursor_img_rect)
    scr.blit(menu, msg_box_menu)
    scr.blit(start_button, msg_box_start)
    scr.blit(quit_button, msg_box_quit)
    pygame.display.flip()


def end(win, scr, cursor_img_surf, cursor_img_rect):
    '''
    function draws menu with player's score and buttons
    to restart or quit
    '''
    global score
    global msg_restart_box
    global msg_quit_box

    myfont = pygame.font.Font('introrustg-base2line.ttf', 48)
    scorefont = pygame.font.Font('introrustg-base2line.ttf', 38)
    msg = myfont.render("SUCCESS", True, BLACK)
    msg_score_text = scorefont.render("nr of survived cycles:", True, BLACK)
    msg_score = scorefont.render(str(score), True, BLACK)
    msg_restart = scorefont.render("RESTART", True, BLACK)
    msg_quit = scorefont.render("QUIT", True, BLACK)
    msg_restart_box = msg_restart.get_rect()
    msg_quit_box = msg_quit.get_rect()
    msg_box = msg.get_rect()
    msg_score_text_box = msg_score_text.get_rect()
    msg_score_box = msg_score.get_rect()
    msg_box.center = (1/2*win.w, 1/6*win.h)
    msg_score_text_box.center = (1/2*win.w, 1/3*win.h)
    msg_score_box.center = (1/2*win.w, 3/6*win.h)
    msg_restart_box.center = (1/3*win.w, 4/6*win.h)
    msg_quit_box.center = (2/3*win.w, 4/6*win.h)

    cursor_img_rect.center = pygame.mouse.get_pos()
    scr.fill(WHITE)
    scr.blit(msg_score, msg_score_box)
    scr.blit(msg_score_text, msg_score_text_box)
    scr.blit(msg, msg_box)
    scr.blit(msg_quit, msg_quit_box)
    scr.blit(msg_restart, msg_restart_box)
    scr.blit(cursor_img_surf, cursor_img_rect)
    pygame.display.flip()


class Bullet(pygame.sprite.Sprite):
    '''
    class handling bullets movement and creation
    '''
    def __init__(self, player, angle, win):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("rocket.png")
        self.rect = self.image.get_rect()
        self.rect.center = player.center
        self.image = pygame.transform.rotate(self.image, -angle)
        self.win = win
        # vector
        rot = Vector2(10, 0). rotate(angle)
        self.pos = Vector2(self.rect.center) + rot
        self.vel = Vector2(1, 0).rotate(angle - 90) * 4

    def update(self):
        self.pos += self.vel
        self.rect.center = self.pos
        if not self.win.contains(self.rect):
            self.kill()


class Enemy(pygame.sprite.Sprite):
    '''
    class handling enemies behaviour
    '''
    def __init__(self, player, win):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("mina.png")
        self.rect = self.image.get_rect()
        spawn = random.randrange(WINDOW_SIZE[0])
        self.rect.center = (spawn, 0)
        angle = 90
        # Rotation
        mx = self.rect.x
        my = self.rect.y
        mx = mx - player.centerx
        my = (my - player.centery)*-1
        # first quarter
        if mx > 0 and my > 0:
            angle = math.degrees(math.atan(mx/my))
        # second quarter
        elif mx < 0 and my > 0:
            angle = 360 - abs(math.degrees(math.atan(mx/my)))
        # third quarter
        elif mx < 0 and my < 0:
            angle = 180 + math.degrees(math.atan(mx/my))
        # fourth quarter
        elif mx > 0 and my < 0:
            angle = 180 - abs(math.degrees(math.atan(mx/my)))

        self.win = win
        self.image = pygame.transform.rotate(self.image, -angle)
        # vector
        rot = Vector2(10, 0). rotate(angle)
        self.pos = Vector2(self.rect.center) + rot
        self.vel = Vector2(1, 0).rotate(angle - 90) * 4

    def update(self, player):
        global Lost
        self.pos -= self.vel
        self.rect.center = self.pos
        if player.colliderect(self.rect):
            Lost = True
            self.kill()
        if self.rect.y > WINDOW_SIZE[1]+100:
            self.kill()


def main():
    '''
    main function
    '''
    # implementing globals
    global game
    global Lost
    global score
    pygame.init()

    # screen setup
    scr = pygame.display.set_mode(WINDOW_SIZE)
    win = scr.get_rect()
    background_surf = pygame.image.load("background.png").convert_alpha()
    background = background_surf.get_rect()
    background.center = win.center

    # creating pygame.srpite.Groups for enemies and bullets
    bulletgroup = pygame.sprite.Group()
    enemygroup = pygame.sprite.Group()

    # custom cursor implementation
    pygame.mouse.set_visible(False)
    cursor_img_surf = pygame.image.load("cursor.png")
    cursor_img_rect = cursor_img_surf.get_rect()

    # creating reference player model for later rotation
    img_surf = pygame.image.load("tank.png")
    img = img_surf.get_rect()
    img.center = win.center
    model_surf = img_surf
    model = model_surf.get_rect()
    model.center = win.center

    # creating local variables
    angle = 0
    time = 0
    diff = 0

    # limiting fps
    fpsClock = pygame.time.Clock()
    # Menu loop
    while not game:
        draw_welcome_menu(scr, win, cursor_img_surf, cursor_img_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if msg_box_start.collidepoint(pygame.mouse.get_pos()):
                    game = True
                if msg_box_quit.collidepoint(pygame.mouse.get_pos()):
                    sys.exit()
    # Main loop
    while not Lost:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Bullets firing
                if (pygame.mouse.get_pressed(num_buttons=3) ==
                   (True, False, False)):
                    bullet = Bullet(model, angle, win)
                    bulletgroup.add(bullet)

        # Custom cursor handling
        cursor_img_rect.center = pygame.mouse.get_pos()

        # Model rotation according to cursor rotation
        model_surf = pygame.transform.rotate(img_surf, -angle)

        # Enemy and bullet collision
        for bullet in bulletgroup:
            for enemy in enemygroup:
                if enemy.rect.colliderect(bullet.rect):
                    bullet.kill()
                    enemy.kill()

        # Dynamic difficulty implementation
        if (200-diff) < 20:
            diff = 180
        if time % (200 - diff) == 0:
            enemy = Enemy(model, win)
            enemygroup.add(enemy)
            diff += 5
            score += 1
            time = 0
        time += 1

        # Cursor in accordance to player position detection
        mx, my = list(pygame.mouse.get_pos())
        mx = mx - model.centerx
        my = (my - model.centery)*-1
        # first quarter
        if mx > 0 and my > 0:
            angle = math.degrees(math.atan(mx/my))
        # second quarter
        elif mx < 0 and my > 0:
            angle = 360 - abs(math.degrees(math.atan(mx/my)))
        # third quarter
        elif mx < 0 and my < 0:
            angle = 180 + math.degrees(math.atan(mx/my))
        # fourth quarter
        elif mx > 0 and my < 0:
            angle = 180 - abs(math.degrees(math.atan(mx/my)))

        # Player collision
        if model.left < win.left:
            model = model.move(P_STEP, 0)
        if model.top < win.top:
            model = model.move(0, P_STEP)
        if model.bottom > win.bottom:
            model = model.move(0, -P_STEP)
        if model.right > win.right:
            model = model.move(-P_STEP, 0)

        # Player movement
        all_keys = pygame.key.get_pressed()
        if all_keys[ord("w")]:
            model = model.move(0, -P_STEP)
        if all_keys[ord("a")]:
            model = model.move(-P_STEP, 0)
        if all_keys[ord("s")]:
            model = model.move(0, P_STEP)
        if all_keys[ord("d")]:
            model = model.move(P_STEP, 0)

        # Screen visuals
        scr.blit(background_surf, background)
        scr.blit(model_surf, model)
        bulletgroup.update()
        bulletgroup.draw(scr)
        enemygroup.update(model)
        enemygroup.draw(scr)
        scr.blit(cursor_img_surf, cursor_img_rect)
        pygame.display.flip()
        fpsClock.tick(120)

        # End menu screen
        while Lost:
            end(win, scr, cursor_img_surf, cursor_img_rect)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if msg_restart_box.collidepoint(pygame.mouse.get_pos()):
                        Lost = False
                        time = 0
                        score = 0
                        diff = 0
                        pygame.sprite.Group.empty(bulletgroup)
                        pygame.sprite.Group.empty(enemygroup)
                    if msg_quit_box.collidepoint(pygame.mouse.get_pos()):
                        sys.exit()


if __name__ == "__main__":
    main()
