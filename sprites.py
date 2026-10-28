import pygame
import random
from settings import *




class Sun(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        sprite_sheet = pygame.image.load("sun.png").convert_alpha()


        self.frames = []
        num_frames = 8
        frame_width = sprite_sheet.get_width() // num_frames
        frame_height = sprite_sheet.get_height()


        for i in range(num_frames):
            sub_surface = sprite_sheet.subsurface(
                (i * frame_width, 0, frame_width, frame_height)
            )
            scaled_surface = pygame.transform.scale(sub_surface, (70, 70))
            self.frames.append(scaled_surface)


        self.current_frame = 0
        self.animation_speed = 0.15


        self.image = self.frames[int(self.current_frame)]
        self.rect = self.image.get_rect()
        self.rect.topright = (WIDTH - 20, 20)


    def update(self):
        self.current_frame += self.animation_speed
        if self.current_frame >= len(self.frames):
            self.current_frame = 0
        self.image = self.frames[int(self.current_frame)]




class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image_raw = pygame.image.load("background.png").convert()
        self.image = pygame.transform.scale(self.image_raw, (WIDTH, HEIGHT))
        
        self.rect1 = self.image.get_rect(topleft=(0, 0))
        self.rect2 = self.image.get_rect(topleft=(WIDTH, 0))


    def update(self):
        self.rect1.x -= GAME_SPEED
        self.rect2.x -= GAME_SPEED


        if self.rect1.right <= 0:
            self.rect1.x = self.rect2.right
        if self.rect2.right <= 0:
            self.rect2.x = self.rect1.right


    def draw(self, surface):
        surface.blit(self.image, self.rect1)
        surface.blit(self.image, self.rect2)




class Dinosaur(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        sprite_sheet = pygame.image.load("dino_run.png").convert_alpha()


        self.frames = []
        num_frames = 8
        frame_width = sprite_sheet.get_width() // num_frames
        frame_height = sprite_sheet.get_height()


        for i in range(num_frames):
            sub_surface = sprite_sheet.subsurface(
                (i * frame_width, 0, frame_width, frame_height)
            )
            scaled_surface = pygame.transform.scale(sub_surface, (60, 60))
            self.frames.append(scaled_surface)


        self.current_frame = 0
        self.animation_speed = 0.2


        self.image = self.frames[int(self.current_frame)]
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.bottom = HEIGHT - 50


        self.velocity_y = 0
        self.is_jumping = False


    def jump(self):
        if not self.is_jumping:
            self.velocity_y = JUMP_SPEED
            self.is_jumping = True


    def animate(self):
        if not self.is_jumping:
            self.current_frame += self.animation_speed
            if self.current_frame >= len(self.frames):
                self.current_frame = 0
            self.image = self.frames[int(self.current_frame)]
        else:
            self.image = self.frames[0]


    def update(self):
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y


        if self.rect.bottom >= HEIGHT - 50:
            self.rect.bottom = HEIGHT - 50
            self.velocity_y = 0
            self.is_jumping = False


        self.animate()




class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()


        sprite_sheet = pygame.image.load("campfire.png").convert_alpha()


        self.frames = []
        num_frames = 8
        frame_width = sprite_sheet.get_width() // num_frames
        frame_height = sprite_sheet.get_height()


        for i in range(num_frames):
            sub_surface = sprite_sheet.subsurface(
                (i * frame_width, 0, frame_width, frame_height)
            )
            scaled_surface = pygame.transform.scale(sub_surface, (45, 55))
            self.frames.append(scaled_surface)


        self.current_frame = 0
        self.animation_speed = 0.25


        self.image = self.frames[int(self.current_frame)]
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH + random.randint(0, 200)
        self.rect.bottom = HEIGHT - 50


    def animate(self):
        self.current_frame += self.animation_speed
        if self.current_frame >= len(self.frames):
            self.current_frame = 0
        self.image = self.frames[int(self.current_frame)]


    def update(self):
        self.rect.x -= GAME_SPEED
        self.animate()


        if self.rect.right < 0:
            self.kill()
