import pygame
import random
import sys


from settings import *
from sprites import Dinosaur, Obstacle, Background, Sun




class Game:
    def __init__(self):
        pygame.init()


        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("T-Rex Runner Clone - Cordel Style")


        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 24)


        self.obstacle_timer = pygame.USEREVENT + 1


    def reset_game(self):
        self.score = 0
        self.playing = True


        self.all_sprites = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()


        # Instancia o fundo, sol e jogador
        self.background = Background()
        self.sun = Sun()
        self.player = Dinosaur()


        # Adiciona à lista de renderização na ordem (Sun -> Player)
        self.all_sprites.add(self.sun)
        self.all_sprites.add(self.player)


        pygame.time.set_timer(self.obstacle_timer, 1500)


    def run(self):
        while True:
            self.reset_game()
            self.game_loop()
            self.game_over_screen()


    def game_loop(self):
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()


    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_UP):
                    self.player.jump()


            if event.type == self.obstacle_timer:
                if random.random() > 0.3:
                    obstacle = Obstacle()
                    self.all_sprites.add(obstacle)
                    self.obstacles.add(obstacle)


    def update(self):
        self.background.update()
        self.all_sprites.update()
        self.score += 1


        if pygame.sprite.spritecollide(self.player, self.obstacles, False):
            pygame.time.set_timer(self.obstacle_timer, 0)
            self.playing = False


    def draw(self):
        # 1. Desenha o fundo em rolagem
        self.background.draw(self.screen)


        # 2. Desenha todos os sprites (Sol, Dinossauro e Fogueiras)
        self.all_sprites.draw(self.screen)


        # 3. Desenha a pontuação (canto superior esquerdo)
        score_surface = self.font.render(
            f"Score: {self.score // 5}",
            True,
            BLACK
        )
        self.screen.blit(score_surface, (20, 20))


        pygame.display.flip()


    def game_over_screen(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            self.screen.fill(WHITE)


            text = self.font.render(
                "GAME OVER - Pressione ESPAÇO para reiniciar",
                True,
                BLACK
            )
            rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            self.screen.blit(text, rect)
            pygame.display.flip()


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()


                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_SPACE, pygame.K_UP):
                        waiting = False
