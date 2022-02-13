import pygame
import os
import sys
import math
import random
pygame.init()

WIDTH, HEIGHT = 900, 800
BIRD_WIDTH, BIRD_HEIGHT = 80, 80
JUMP_HEIGHT = 200
JUMP_SPEED = 1
OBSTACLE_WIDTH = 80
WINDOW = 300
GRAVITY = 1
SCORE_HEIGHT = 40
FPS = 100
BROWN = (200, 150, 100)
WHITE = (255, 255, 255)
high_score = 0


COLLISION = pygame.USEREVENT + 1
SPAWN_PIPE = pygame.USEREVENT + 2
BIRDFLAP = pygame.USEREVENT + 3

pygame.time.set_timer(SPAWN_PIPE, 2000)
pygame.time.set_timer(BIRDFLAP, 200)

GAMEOVER_TEXT = pygame.font.SysFont('comicsans', 80)

pipe_list = []

WHITE = (255, 255, 255)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

BG_SURFACE = pygame.image.load(os.path.join('Assets', 'background-day.png')).convert()
BG_SURFACE = pygame.transform.scale(BG_SURFACE, (2 * WIDTH, HEIGHT - 50))

START_SURFACE = pygame.transform.scale2x(pygame.image.load(os.path.join('Assets', 'message.png')).convert_alpha())
START_SURFACE = pygame.transform.scale(START_SURFACE, (300, 600))

FLOOR_SURFACE = pygame.image.load(os.path.join('Assets', 'base.png')).convert()
FLOOR_SURFACE = pygame.transform.scale(FLOOR_SURFACE, (2 * WIDTH, 50))
win_x_pos = 0

BIRD_UPFLAP = pygame.transform.scale2x(pygame.image.load(os.path.join('Assets', 'bluebird-upflap.png')).convert_alpha())
BIRD_MIDFLAP = pygame.transform.scale2x(pygame.image.load(os.path.join('Assets', 'bluebird-midflap.png')).convert_alpha())
BIRD_DOWNFLAP = pygame.transform.scale2x(pygame.image.load(os.path.join('Assets', 'bluebird-downflap.png')).convert_alpha())

BIRD_FRAMES = [BIRD_UPFLAP, BIRD_MIDFLAP, BIRD_DOWNFLAP]
bird_index = 0
bird_surface = BIRD_FRAMES[bird_index]
bird_rect = bird_surface.get_rect(center = (100, 100))

LOWER_PIPE = pygame.image.load(os.path.join('Assets', 'green-pipe1.png')).convert()
LOWER_PIPE = pygame.transform.scale(LOWER_PIPE, (OBSTACLE_WIDTH, HEIGHT))
UPPER_PIPE = pygame.image.load(os.path.join('Assets', 'green-pipe1.png')).convert()
UPPER_PIPE = pygame.transform.scale(UPPER_PIPE, (OBSTACLE_WIDTH, HEIGHT))
UPPER_PIPE = pygame.transform.rotate(UPPER_PIPE, 180)

flap_sound = pygame.mixer.Sound(os.path.join('sound', 'sfx_wing.wav'))
death_sound = pygame.mixer.Sound(os.path.join('sound', 'sfx_hit.wav'))
score_sound = pygame.mixer.Sound(os.path.join('sound', 'sfx_point.wav'))
fall_sound = pygame.mixer.Sound(os.path.join('sound', 'sfx_swooshing.wav'))

SCORE_TEXT = pygame.font.SysFont('comicsans', SCORE_HEIGHT)

def draw_window(game_active, score = 0):
    global UPPER_PIPE
    global LOWER_PIPE
    global win_x_pos

    WIN.blit(BG_SURFACE, (0, 0))
    WIN.blit(FLOOR_SURFACE, (win_x_pos, HEIGHT - 50))

    win_x_pos -= 1
    if win_x_pos < -WIDTH:
        win_x_pos = 0

    HIGH_SCORE = SCORE_TEXT.render("HIGH SCORE = {:.0f}".format(high_score), 1, WHITE)
    WIN.blit(HIGH_SCORE, (20, 20))

    if game_active:

        WIN.blit(bird_surface, bird_rect)
        for pipe in pipe_list:
            if pipe.y == 0:
                WIN.blit(UPPER_PIPE, (pipe.x, pipe.height - HEIGHT))
            else:
                WIN.blit(LOWER_PIPE, (pipe.x, HEIGHT - pipe.height))




        SCORE = SCORE_TEXT.render("SCORE = {:.0f}".format(score), 1, WHITE)
        WIN.blit(SCORE, (WIDTH - SCORE.get_width() -20, 20))

    else:
        WIN.blit(START_SURFACE, (WIDTH // 2 - 150, HEIGHT // 2 - 300))



    pygame.display.update()

def create_pipe():
    global UPPER_PIPE
    global LOWER_PIPE
    upper_pipe_height = random.randint(0, HEIGHT - WINDOW)
    pipe = pygame.Rect(WIDTH, 0, OBSTACLE_WIDTH, upper_pipe_height)
    pipe_list.append(pipe)


    lower_pipe_height = HEIGHT - upper_pipe_height - WINDOW
    pipe = pygame.Rect(WIDTH, HEIGHT - lower_pipe_height, OBSTACLE_WIDTH, lower_pipe_height)
    pipe_list.append(pipe)

def move_pipe():
    for pipe in pipe_list:
        pipe.x -= 1
        if pipe.x < 0 - OBSTACLE_WIDTH:
            pipe_list.remove(pipe)



def bird_animation():
    global bird_index
    global bird_surface
    global bird_rect
    bird_index += 1
    if bird_index == 3:
        bird_index = 0

    bird_surface = BIRD_FRAMES[bird_index]

    bird_rect = bird_surface.get_rect(center = (100, bird_rect.centery))

def rotate_bird(bird):
	new_bird = pygame.transform.rotozoom(bird, -bird_rect.y, 1)
	return new_bird

def bird_movement(jump_pos):
    global is_jump
    if is_jump:
        bird_rect.y -= JUMP_SPEED

        if bird_rect.y < jump_pos - JUMP_HEIGHT or bird_rect.y < 0:
            is_jump = False


    else:
        bird_rect.y += GRAVITY




def check_collision():
    for pipe in pipe_list:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            pygame.event.post(pygame.event.Event(COLLISION))

    if bird_rect.y < 0 or bird_rect.y > HEIGHT:
        pygame.event.post(pygame.event.Event(COLLISION))
        fall_sound.play()


def update_score(score):
    global high_score

    for pipe in pipe_list:
        if bird_rect.x == pipe.x:
            score += 0.5
            score_sound.play()


    if score > high_score:
        high_score = score


    return score

def game_over():
    GAMEOVER = GAMEOVER_TEXT.render("KHATAM TATA BYE BYE", 1 , WHITE)
    WIN.blit(GAMEOVER, (WIDTH // 2 - GAMEOVER.get_width() // 2, HEIGHT // 2 - GAMEOVER.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(2000)

def game_pause():
    is_pause = True
    while is_pause:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    is_pause = False



def main():
    game_active = False
    run = True
    is_pause = False

    global is_jump
    global bird_index
    global pipe_list


    while run:
        if game_active:
            jump_pos = None
            pipe_list = []
            is_jump = False
            bird_rect.y = 100
            score = 0
            clock = pygame.time.Clock()
            clock.tick(FPS)
            while True:
                draw_window(game_active, score)

                for event in pygame.event.get():

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP and is_jump == False:
                            is_jump = True
                            flap_sound.play()
                            jump_pos = bird_rect.y
                        if event.key == pygame.K_SPACE and is_pause == False:
                            is_pause = True
                            game_pause()
                            is_pause = False

                    if event.type == COLLISION:
                        game_active = False
                        game_over()
                    if event.type == BIRDFLAP:
                        bird_animation()

                    if event.type == SPAWN_PIPE:
                        create_pipe()


                bird_movement(jump_pos)
                check_collision()
                move_pipe()
                score = update_score(score)

                if not game_active:
                    break


        draw_window(game_active)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                game_active = True
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()


main()
