from math import sin
import random
import os
import pathlib

def main_goose():

    import pygame
    from pygame.constants import QUIT, K_DOWN, K_UP, K_RIGHT, K_LEFT, USEREVENT

    pygame.init()
    FPS = pygame.time.Clock()
    screen = width, heigth = 1300, 800
    main_surface = pygame.display.set_mode(screen)

    CREATE_ENEMY = pygame.USEREVENT + 1
    pygame.time.set_timer(CREATE_ENEMY, 1500)

    CREATE_BONUS = pygame.USEREVENT + 2
    pygame.time.set_timer(CREATE_BONUS, 2500)

    CHANGE_IMG = pygame.USEREVENT + 3
    pygame.time.set_timer(CHANGE_IMG, 125)

    CURRENT_PATH = pathlib.Path(__file__).parent

    BG_PATH = os.path.join(CURRENT_PATH, 'image', 'background')

    BG_images = [
        pygame.image.load(os.path.join(BG_PATH, file)).convert() for file in os.listdir(BG_PATH)
    ]
    bg = pygame.transform.scale(BG_images[0], screen)

    heart_img = pygame.image.load(os.path.join(CURRENT_PATH, 'image', 'heart.svg')).convert_alpha()
    heart_img = pygame.transform.scale(heart_img, (50, 50)) 

    box_img = pygame.image.load(os.path.join(CURRENT_PATH, 'image', 'box.png')).convert_alpha()
    box_img = pygame.transform.scale(box_img, (50, 50))

    enemies = []
    bonuses = []

    IMGS_PATH = os.path.join(CURRENT_PATH, 'image', 'Goose')

    goose_images = [
        pygame.image.load(os.path.join(IMGS_PATH, file)).convert_alpha()
        for file in os.listdir(IMGS_PATH)
    ]
    goose = goose_images[0]
    lifes_goose = 3
    N = 3
    bgX = 0
    bgX2 = bg.get_width()
    bg_speed = 3
    game_bonuses = 0
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255


    def exit(point):
        print(f"\033[032mYour score is: {point}\033[0m")
        return False


    def creat_enemy():
        enemy = pygame.image.load(os.path.join(CURRENT_PATH, 'image', 'enemy.png')).convert_alpha()
        e = enemy.get_size()
        enemy_rect = pygame.Rect(
            width, random.randint(e[1], heigth - e[1]), *enemy.get_size()
        )
        enemy_speed = random.randint(1, 7)
        return [enemy, enemy_rect, enemy_speed]
    




    def creat_bonus():
        bonus = pygame.image.load(os.path.join(CURRENT_PATH, 'image', 'bonus.png')).convert_alpha()
        b = bonus.get_size()
        bonus_rect = pygame.Rect(
            random.randint(b[0], width - b[0]), -bonus.get_height(), *bonus.get_size()
        )
        bonus_speed = random.randint(1, 5)
        return [bonus, bonus_rect, bonus_speed]


    def display_boom():
        boom = pygame.image.load(os.path.join(CURRENT_PATH, 'image', 'boom.png')).convert_alpha()
        main_surface.blit(boom, goose_rect)
        pygame.time.set_timer(USEREVENT + 4, 10000)


    def game_over():
        game_over = pygame.image.load(os.path.join(CURRENT_PATH, 'image', 'gameover.png')).convert_alpha()
        main_surface.blit(game_over, (width / 2 - 250, heigth / 2 - 300))
        pygame.display.flip()
        pygame.time.wait(2000)


    goose_rect = goose.get_rect()
    goose_speed = 6
    image_index = 0
    is_working = True

    while is_working:
        FPS.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                is_working = exit(game_bonuses)
            if event.type == CREATE_ENEMY:
                enemies.append(creat_enemy())
            if event.type == CREATE_BONUS:
                bonuses.append(creat_bonus())
            if event.type == CHANGE_IMG:
                image_index += 1

        Pressed_key = pygame.key.get_pressed()
        bgX -= bg_speed
        bgX2 -= bg_speed

        if bgX < -bg.get_width():
            bgX = bg.get_width()
        if bgX2 < -bg.get_width():
            bgX2 = bg.get_width()

        main_surface.blit(bg, (bgX, 0))
        main_surface.blit(bg, (bgX2, 0))

        if N <= game_bonuses < 3 * N:
            bg = pygame.transform.scale(BG_images[1], screen)
        if 3 * N <= game_bonuses:
            bg = pygame.transform.scale(BG_images[2], screen)

            bg_speed = 0
            bgX = 0
            bgX2 = bg.get_width()

        if image_index == len(goose_images):
            image_index = 0

        goose = goose_images[image_index]
        main_surface.blit(goose, goose_rect)

        for enemy in enemies:
            enemy[1] = enemy[1].move(-enemy[2], sin(enemy[1][0] / 40) * 3)
            main_surface.blit(enemy[0], enemy[1])

            if enemy[1].left < 0:
                enemies.pop(enemies.index(enemy))

            if goose_rect.colliderect(enemy[1]):
                enemies.pop(enemies.index(enemy))
                display_boom()
                lifes_goose -= 1
                for i in range(lifes_goose):
                    main_surface.blit(heart_img, (10 + i*30, 10))
                if lifes_goose == 0:
                    game_over()
                    is_working = exit(game_bonuses)

        for bonus in bonuses:
            bonus[1] = bonus[1].move(0, bonus[2])
            main_surface.blit(bonus[0], bonus[1])

            if goose_rect.colliderect(bonus[1]):
                game_bonuses += 1
                bonuses.pop(bonuses.index(bonus))
            else:
                if bonus[1].bottom > heigth:
                    bonuses.pop(bonuses.index(bonus))

        # print result
        my_font = pygame.font.Font(os.path.join(CURRENT_PATH, 'font', 'Candal.ttf'), 35)
        if 3 * N <= game_bonuses:
            main_surface.blit(
                my_font.render(str(game_bonuses), 1, WHITE),
                (width - 110, 10),
            )
        else:
            main_surface.blit(
                my_font.render(str(game_bonuses), 1, BLACK),
                (width - 110, 10),
            )

        for i in range(lifes_goose):
            main_surface.blit(heart_img, (10 + i*50, 10))
        main_surface.blit(box_img, (width - 170, 10)) 

        if Pressed_key[K_DOWN] and goose_rect.bottom < heigth:
            goose_rect = goose_rect.move(0, goose_speed)
        if Pressed_key[K_UP] and goose_rect.top > 0:
            goose_rect = goose_rect.move(0, -goose_speed)
        if Pressed_key[K_LEFT] and goose_rect.left > 0:
            goose_rect = goose_rect.move(-goose_speed, 0)
        if Pressed_key[K_RIGHT] and goose_rect.right < width:
            goose_rect = goose_rect.move(goose_speed, 0)
        main_surface.blit(goose, goose_rect)
        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()


def start_goose():
    main_goose()
    return '\033[32mThank you for using the goose killer game'


if __name__ == '__main__':
    start_goose()