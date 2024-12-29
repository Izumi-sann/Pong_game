import pygame
import sys
import time
import math
from Class import *

class HomePage():
    def __init__(self, width=600, heigth=600, move=False) -> None:
        pygame.init()
        pygame.display.set_caption("pong game")
        self.dimension = (width, heigth)
        self.screen = pygame.display.set_mode(self.dimension)
        self.clock = pygame.time.Clock()
        self.running = True
        self.ball = Ball(width=self.dimension[0], heigth=self.dimension[1], move=move)
        self.high_scores = self.load_high_scores()  # Carica i punteggi alti

    def load_high_scores(self):
        """Carica i punteggi più alti dal file."""
        try:
            with open("high_score.txt", "r") as file:
                scores = file.readlines()
                high_scores = {
                    "Player_A": int(scores[0].split(":")[1].strip()),
                    "Player_B": int(scores[1].split(":")[1].strip()),
                }
        except FileNotFoundError:
            high_scores = {"Player_A": 0, "Player_B": 0}  # Default in assenza di file
        return high_scores

    def get_events(self):  # Gestione eventi
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    self.running = False

    def lampeggio_testo(self, MAX, MIN, scale, speed):
        size = MIN + (MAX - MIN) * (0.5 + 0.5 * math.sin(scale))
        font = pygame.font.Font(None, int(size))
        text_surface = font.render("START GAME", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.dimension[0] // 2, self.dimension[1] // 2 - 30))
        self.screen.blit(text_surface, text_rect)
        scale += speed
        return scale

    def display_high_scores(self):
        """Mostra i punteggi più alti nel menu."""
        font = pygame.font.Font(None, 40)
        text = font.render(f"High Scores: {self.high_scores['Player_A']} - {self.high_scores['Player_B']}", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.dimension[0] // 2, self.dimension[1] // 2 + 30))
        self.screen.blit(text, text_rect)

    def home(self):
        # Definizione testo lampeggiante
        MAX_SIZE = 80
        MIN_SIZE = 50
        FONT_SPEED = 0.05
        scale = 0

        while self.running:
            self.clock.tick(60)
            pygame.display.update()
            self.get_events()
            self.screen.fill((0, 0, 0))

            # Scritta che lampeggia
            scale = self.lampeggio_testo(MAX_SIZE, MIN_SIZE, scale, FONT_SPEED)

            # Mostra i punteggi più alti
            self.display_high_scores()

class Game(HomePage):
    def __init__(self) -> None:
        super().__init__(900, 600, move=True)
        self.pad_A = Pad(X=30, Y=5, screen=(self.dimension))
        self.pad_B = Pad(X=self.dimension[0] - 48, Y=self.dimension[1] - 105, screen=(self.dimension))
        self.high_scores = self.load_high_scores()  # Carica i punteggi alti

    def save_high_scores(self):
        """Salva i punteggi più alti nel file."""
        with open("high_score.txt", "w") as file:
            file.write(f"Player_A: {self.high_scores['Player_A']}\n")
            file.write(f"Player_B: {self.high_scores['Player_B']}\n")

    def update_high_scores(self):
        """Aggiorna i punteggi più alti se necessario."""
        if self.pad_A.punteggio > self.high_scores["Player_A"]:
            self.high_scores["Player_A"] = self.pad_A.punteggio
        if self.pad_B.punteggio > self.high_scores["Player_B"]:
            self.high_scores["Player_B"] = self.pad_B.punteggio
        self.save_high_scores()

    def get_events(self):  # Gestione eventi
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_UP:
                        self.pad_B.movement[0] = True
                    case pygame.K_DOWN:
                        self.pad_B.movement[1] = True
                    case pygame.K_w:
                        self.pad_A.movement[0] = True
                    case pygame.K_s:
                        self.pad_A.movement[1] = True
                    case pygame.K_ESCAPE:
                        self.running = False
            if event.type == pygame.KEYUP:
                match event.key:
                    case pygame.K_UP:
                        self.pad_B.movement[0] = False
                    case pygame.K_DOWN:
                        self.pad_B.movement[1] = False
                    case pygame.K_w:
                        self.pad_A.movement[0] = False
                    case pygame.K_s:
                        self.pad_A.movement[1] = False

    def points(self):
        font = pygame.font.Font(None, 50)
        white = (255, 255, 255)

        # Write current points
        text = font.render(f"{self.pad_A.punteggio} - {self.pad_B.punteggio}", True, white)
        text_rect = text.get_rect(center=(self.dimension[0] / 2, 30))
        self.screen.blit(text, text_rect)

    def restart(self):
        self.ball.reset()
        self.pad_A.reset()
        self.pad_B.reset()

    def blit(self):
        """Blit game objects onto the screen."""
        self.screen.blit(self.ball.texture, (self.ball.position[0], self.ball.position[1]))
        self.screen.blit(self.pad_A.texture, (self.pad_A.position[0], self.pad_A.position[1]))
        self.screen.blit(self.pad_B.texture, (self.pad_B.position[0], self.pad_B.position[1]))

    def run_game(self) -> None:
        while self.running:
            self.get_events()
            pygame.display.update()
            self.screen.fill((0, 0, 0))
            self.clock.tick(60)

            self.pad_A.changeY()
            self.pad_B.changeY()

            reset = self.ball.move(self.pad_A, self.pad_B)
            if reset:
                self.update_high_scores()  # Aggiorna i punteggi alti
                self.restart()
                self.points()
                self.blit()
                pygame.display.update()
                time.sleep(1)

            self.points()
            self.blit()

def main():
    HomePage().home()
    Game().run_game()

if __name__ == "__main__":
    while True:
        main()
