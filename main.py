import pygame
import random

pygame.init()

window_width = 800
window_height = 600

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

snake_size = 10
apple_size = 10
snake_speed = 15

font_style = pygame.font.SysFont(None, 50)
score_font = pygame.font.SysFont(None, 35)

game_window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Snake Game')

def display_score(score):
    value = score_font.render("Score: " + str(score), True, white)
    game_window.blit(value, [0, 0])

def draw_snake(snake_size, snake_pixels):
    for pixel in snake_pixels:
        pygame.draw.rect(game_window, white, [pixel[0], pixel[1], snake_size, snake_size])

def game_loop():
    game_over = False
    game_exit = False

    x1 = window_width / 2
    y1 = window_height / 2
    x1_change = 0
    y1_change = 0
    snake_pixels = []
    snake_length = 1

    apple_x = round(random.randrange(0, window_width - apple_size) / 10.0) * 10.0
    apple_y = round(random.randrange(0, window_height - apple_size) / 10.0) * 10.0

    pygame.joystick.init()
    init = pygame.joystick.get_count() > 0
    if init:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()

    while not game_exit:
        while game_over:
            game_window.fill(black)
            message = font_style.render(f"Game Over!", True, red)
            game_window.blit(message, [window_width / 3, window_height / 3])
            display_score(snake_length - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = False
                    game_exit = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = False
                        game_exit = True
                    if event.key == pygame.K_r:
                        game_loop()
                if pygame.joystick.get_count() > 0:
                    if event.type == pygame.JOYBUTTONDOWN:
                        if event.button == 0:  # A button
                            game_over = False
                            game_exit = False
                            game_loop()
                        elif event.button == 1: # B button
                            game_over = False
                            game_exit = True
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
            if pygame.joystick.get_count() > 0:
                if event.type == pygame.JOYBUTTONDOWN:
                    if event.button == 1: # B button
                        game_over = False
                        game_exit = True

        if pygame.joystick.get_count() > 0:
            axes = joystick.get_numaxes()
            for i in range(axes):
                axis = joystick.get_axis(i)
                if i == 0:  # X-axis
                    if axis < -0.5:
                        x1_change = -snake_size
                        y1_change = 0
                    elif axis > 0.5:
                        x1_change = snake_size
                        y1_change = 0
                elif i == 1:  # Y-axis
                    if axis < -0.5:
                        y1_change = -snake_size
                        x1_change = 0
                    elif axis > 0.5:
                        y1_change = snake_size
                        x1_change = 0

        if x1 >= window_width or x1 < 0 or y1 >= window_height or y1 < 0:
            game_over = True

        x1 += x1_change
        y1 += y1_change
        game_window.fill(black)

        pygame.draw.rect(game_window, red, [apple_x, apple_y, apple_size, apple_size])

        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_pixels.append(snake_head)
        if len(snake_pixels) > snake_length:
            del snake_pixels[0]

        for pixel in snake_pixels[:-1]:
            if pixel == snake_head:
                game_over = True

        draw_snake(snake_size, snake_pixels)

        if x1 == apple_x and y1 == apple_y:
            apple_x = round(random.randrange(0, window_width - apple_size) / 10.0) * 10.0
            apple_y = round(random.randrange(0, window_height - apple_size) / 10.0) * 10.0
            snake_length += 1

        display_score(snake_length - 1)

        pygame.display.update()
        pygame.time.Clock().tick(snake_speed)

    pygame.quit()

game_loop()
