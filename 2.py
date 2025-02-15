import pygame
from sys import exit
from random import randint

enemy_speed = 8


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.player_walk_1 = pygame.image.load("images/cow_walk_1.png").convert_alpha()
        self.player_walk_2 = pygame.image.load("images/cow_walk_2_new.png").convert_alpha()
        self.player_jump = pygame.image.load("images/cow_jump_new.png").convert_alpha()

        self.player_down_1 = pygame.image.load("images/cow_down_1.png").convert_alpha()
        self.player_down_2 = pygame.image.load("images/cow_down_2.png").convert_alpha()
        self.player_down_3 = pygame.image.load("images/cow_jump_down.png").convert_alpha()

        self.image = self.player_walk_1
        self.rect = self.player_walk_1.get_rect(midbottom=(100, 400))
        self.gravity = 0
        self.counter = 0
        self.jump_sound = pygame.mixer.Sound("voices/jump.mp3")
        self.jump_sound.set_volume(0.4)
        self.was_in_the_air = 0
        self.lock = 0

    def player_input(self):

        keys = pygame.key.get_pressed()
        print(self.rect.bottom)
        if keys[pygame.K_SPACE] and 300 < self.rect.bottom < 400 and self.gravity > 0:
            self.lock = 1

        if keys[pygame.K_SPACE] and self.rect.bottom == 400 and self.lock == 0:
            self.gravity = -20
            self.jump_sound.play()
            self.was_in_the_air = 1

        if self.lock == 1 and self.rect.bottom == 400:
            self.gravity = -20
            self.jump_sound.play()
            self.was_in_the_air = 1
            self.lock = 0

        if keys[pygame.K_DOWN]:
            self.gravity += 3

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity

        if self.rect.bottom >= 400:
            self.rect.bottom = 400
            self.gravity = 0
            if self.was_in_the_air == 1:
                fall_sound = pygame.mixer.Sound("voices/fall.mp3")
                fall_sound.set_volume(0.3)
                fall_sound.play()
            self.was_in_the_air = 0

    def animation(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_DOWN]:

            if self.rect.bottom < 400:
                self.image = self.player_down_3

            else:
                self.counter += 1

                if self.counter % 20 < 10:
                    self.image = self.player_down_1

                else:
                    self.image = self.player_down_2

        else:
            
            if self.rect.bottom < 400:
                self.image = self.player_jump

            else:
                self.counter += 1

                if self.counter % 20 < 10:
                    self.image = self.player_walk_1

                else:
                    self.image = self.player_walk_2


    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        self.enemy = pygame.image.load("images/enemy.png").convert_alpha()
        self.flying_enemy_1 = pygame.image.load("images/flying_enemy_1.png").convert_alpha()
        self.flying_enemy_2 = pygame.image.load("images/flying_enemy_2.png").convert_alpha()
        self.book_sound = pygame.mixer.Sound("voices/book.mp3")
        self.book_sound.set_volume(0.5)

        if type == 0:
            self.image = self.enemy
            self.rect = self.enemy.get_rect(midbottom=(randint(810, 1200), 400))

        else:
            self.image = self.flying_enemy_1
            self.rect = self.image.get_rect(midbottom=(randint(810, 1200), 300))
            self.book_sound.play()
        self.flying_enemy_index = 0

    def enemy_animation(self):
        self.flying_enemy_index += 1
        if self.rect.bottom == 300:
            if self.flying_enemy_index % 50 < 25:
                self.image = self.flying_enemy_1

            else:
                self.image = self.flying_enemy_2

    def enemy_motion(self):
        self.rect.x -= enemy_speed

    def destroy(self):
        if self.rect.x < -100:
            self.kill()
            self.book_sound.stop()

    def update(self):
        self.enemy_animation()
        self.enemy_motion()
        self.destroy()

def cal_score(time, start_time):
    text = my_font.render(str(time - start_time), False, "black")
    text_rect = text.get_rect(topright=(800, 0))
    return (time - start_time), text, text_rect


def collision_sprite(background_music):
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        for obstacle in obstacle_group:
            obstacle.book_sound.stop()
        obstacle_group.empty()
        fail_sound = pygame.mixer.Sound("voices/fail.mp3")
        background_music.stop()
        fail_sound.play()
        return 0

    else:
        return 1

pygame.init()
screen = pygame.display.set_mode((800, 600))
bg_sound = pygame.mixer.Sound("voices/background.mp3")

pygame.display.set_caption("Blappy Fird")
clock = pygame.time.Clock()
my_font = pygame.font.Font("slkscr.ttf", 25)
bigger_font = pygame.font.Font("slkscr.ttf", 40)


bg1 = pygame.image.load("images/new_bg_1.png").convert()
bg2 = pygame.image.load("images/new_bg_3.png").convert()

text1 = my_font.render("Blappy Fird", False, "white")
text1_rect = text1.get_rect(center=(400, 50))

text2 = my_font.render("Mame Gover", False, "white")
text2_rect = text1.get_rect(center=(400, 150))

text3 = my_font.render("Start", False, "white")
text3_rect = text1.get_rect(center=(400, 300))

begin_text = bigger_font.render("Start", False, "white")
begin_text_rect = text1.get_rect(center=(400, 300))

return_text = my_font.render("Return", False, "white")
return_text_rect = return_text.get_rect(center=(400, 500))


big_cow = pygame.image.load("images/we.png").convert_alpha()
big_cow = pygame.transform.rotozoom(big_cow, 15, 3)
big_cow_rect = big_cow.get_rect(center=(200, 200))

score = 0
game_state = 2
start_time = 0

player = pygame.sprite.GroupSingle()
my_cow = Player()
player.add(my_cow)

obstacle_group = pygame.sprite.Group()

waiting = 1250
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, waiting)

while True:
    if score > 100 and score % 10000 < 10:
        print("waiting-")
        if waiting > 1000:
            waiting -= 50
            pygame.time.set_timer(obstacle_timer, waiting)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_state == 1:
            if event.type == obstacle_timer:
                rand_num = randint(0, 4)
                if rand_num == 0:
                    obstacle_group.add(Enemy(1))
                else:
                    obstacle_group.add(Enemy(0))

        if game_state == 0:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if text3_rect.collidepoint(event.pos):
                    game_state = 1
                    start_time = pygame.time.get_ticks()
                    bg_sound.play(loops=-1)

                if return_text_rect.collidepoint(event.pos):
                    game_state = 2

        if game_state == 2:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if begin_text_rect.collidepoint(event.pos):
                    game_state = 1
                    start_time = pygame.time.get_ticks()
                    bg_sound.play(loops=-1)

    if game_state == 1:
        screen.blit(bg1, (0, 0))
        screen.blit(bg2, (0, 400))

        score, text4, text4_rect = cal_score(pygame.time.get_ticks(), start_time)
        screen.blit(text4, text4_rect)
        if score % 5000 < 10 and enemy_speed < 35:
            enemy_speed += 1
            print("speed+")

        player.draw(screen)
        player.update()
        obstacle_group.draw(screen)
        obstacle_group.update()
        game_state = collision_sprite(bg_sound)

    if game_state == 0:
        screen.blit(bg1, (0, 0))
        screen.blit(bg2, (0, 400))
        screen.blit(text1, text1_rect)
        screen.blit(text2, text2_rect)
        screen.blit(text3, text3_rect)
        screen.blit(return_text, return_text_rect)

        my_cow.rect.midbottom = (100, 400)
        my_cow.gravity = 0
        my_cow.was_in_the_air = 0
        enemy_speed = 8
        waiting = 1250

        text5 = my_font.render(f"Your Score: {str(score)}", False, "white")
        text5_rect = text1.get_rect(bottomleft=(50, 400))
        screen.blit(text5, text5_rect)

    if game_state == 2:
        screen.fill("aquamarine2")
        screen.blit(begin_text, begin_text_rect)
        screen.blit(big_cow, big_cow_rect)

    pygame.display.update()
    clock.tick(60)
