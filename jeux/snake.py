import pygame
import random
from .base_game import BaseGame
from utils.mouvements import detect_open_hand

class SnakeGame(BaseGame):
    def __init__(self, screen):
        super().__init__(screen)
        self.cell_size = 20
        self.width, self.height = screen.get_size()
        self.reset()

    def reset(self):
        self.snake = [(100, 100)]
        self.direction = (self.cell_size, 0)
        self.food = (200, 200)
        self.game_over = False
        self.move_delay = 6
        self.frame_count = 0

    def update(self, gesture):
        if self.game_over:
            return

        if gesture == "LEFT" and self.direction != (self.cell_size, 0):
            self.direction = (-self.cell_size, 0)
        elif gesture == "RIGHT" and self.direction != (-self.cell_size, 0):
            self.direction = (self.cell_size, 0)
        elif gesture == "UP" and self.direction != (0, self.cell_size):
            self.direction = (0, -self.cell_size)
        elif gesture == "DOWN" and self.direction != (0, -self.cell_size):
            self.direction = (0, self.cell_size)

        self.frame_count += 1
        if self.frame_count < self.move_delay:
            return
        self.frame_count = 0

        head = (self.snake[0][0] + self.direction[0],
                self.snake[0][1] + self.direction[1])

        # Si touche le mur: fin du jeu
        if head[0] < 0 or head[0] >= self.width or head[1] < 0 or head[1] >= self.height:
            self.game_over = True
            return

        if head in self.snake:
            self.game_over = True
            return

        self.snake.insert(0, head)

        if head == self.food:
            self.food = (random.randrange(0, self.width, self.cell_size),
                         random.randrange(0, self.height, self.cell_size))
        else:
            self.snake.pop()

    def draw_grid(self):
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, (40, 40, 40), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, (40, 40, 40), (0, y), (self.width, y))

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.draw_grid()

        if self.game_over:
            font = pygame.font.Font(None, 72)
            msg = font.render("FIN DU JEU", True, (255, 0, 0))
            sub_font = pygame.font.Font(None, 48)
            sub_msg = sub_font.render("Ouvrez votre main pour recommencer", True, (255, 255, 255))
            self.screen.blit(msg, (self.width // 4, self.height // 2 - 40))
            self.screen.blit(sub_msg, (self.width // 5, self.height // 2 + 20))
            pygame.display.flip()
            return

        for segment in self.snake:
            pygame.draw.rect(self.screen, (0, 255, 0), (*segment, self.cell_size, self.cell_size))

        pygame.draw.rect(self.screen, (255, 0, 0), (*self.food, self.cell_size, self.cell_size))

    def check_restart(self, landmarks):
        if self.game_over and detect_open_hand(landmarks):
            self.reset()
