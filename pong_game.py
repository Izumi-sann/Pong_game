#pong game
import pygame
import sys
import time
import math
from Class import *

class HomePage():
    def __init__(self, width = 400, heigth = 600, move = False) -> None:
        pygame.init()
        pygame.display.set_caption("pong game")
        self.dimension = (width, heigth)
        self.screen = pygame.display.set_mode(self.dimension)
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.ball = Ball(width=self.dimension[0], heigth=self.dimension[1], move = move)
    
    def get_events(self):#gestione eventi
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_w:
                        self.ball.Y_movement[0] = True
                    case pygame.K_s:
                        self.ball.Y_movement[1] = True
                    case pygame.K_a:
                        self.ball.X_movement[0] = True
                    case pygame.K_d:
                        self.ball.X_movement[1] = True
                    case pygame.K_RETURN | pygame.K_KP_ENTER:
                        self.running = False
            
            if event.type == pygame.KEYUP:
                match event.key:
                    case pygame.K_w:
                        self.ball.Y_movement[0] = False
                    case pygame.K_s:
                        self.ball.Y_movement[1] = False
                    case pygame.K_a:
                        self.ball.X_movement[0] = False
                    case pygame.K_d:
                        self.ball.X_movement[1] = False
    
    def blit(self):
        self.screen.blit(self.ball.texture, (self.ball.position[0], self.ball.position[1]))
        try:
            self.screen.blit(self.pad_A.texture, (self.pad_A.position[0], self.pad_A.position[1]))
            self.screen.blit(self.pad_B.texture, (self.pad_B.position[0], self.pad_B.position[1]))
        except AttributeError:
            pass
    
    def lampeggio_testo(self, MAX, MIN, scale, speed):
        size = MIN + (MAX - MIN) * (0.5 + 0.5 * math.sin(scale))
        font = pygame.font.Font(None, int(size))
        
        text_surface = font.render("PRESS ENTER", True, (255, 255, 255))
        # Ottieni il rettangolo del testo e posizionalo al centro dello schermo
        text_rect = text_surface.get_rect(center=(self.dimension[0] // 2, self.dimension[1] // 2))
        self.screen.blit(text_surface, text_rect)
        scale += speed
        
        return scale
    
    def home(self):
        #definizione testo lampeggiante
        MAX_SIZE = 80
        MIN_SIZE = 50
        FONT_SPEED = 0.05
        scale = 0
        
        while self.running:
            #set iniziale
            self.clock.tick(60)
            pygame.display.update()
            self.get_events()
            self.screen.fill((0, 0, 0))
            
            #gestione
            self.ball.change_XY()
            
            #scritta che lampeggia
            scale = self.lampeggio_testo(MAX_SIZE, MIN_SIZE, scale, FONT_SPEED)
            
            #set finale
            self.blit()


class Game(HomePage):
    def __init__(self) -> None:
        super().__init__(640, 480, move=True)
        
        self.pad_A = Pad(X = 30, Y = 5, screen=(self.dimension))
        self.pad_B = Pad(X = self.dimension[0]-48, Y = self.dimension[1]-105, screen=(self.dimension)) #dimensioni pad = 100*18 px; per posizionare correttamente bisonga tenere conto delle dimensioni
    
    def get_events(self):#gestione eventi
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
        
        #write points
        text = font.render(f"{self.pad_A.punteggio} - {self.pad_B.punteggio}", True, white)
        text_rect = text.get_rect(center=(self.dimension[0]/2, 30))
        self.screen.blit(text, text_rect)
        
        #write bounce
        text = font.render(f"bouce: {self.ball.bounce}", True, white)
        text_rect = text.get_rect(center = (self.dimension[0]-100, 30))
        self.screen.blit(text, text_rect)

    def restart(self):
        self.ball.reset()
        self.pad_A.reset()
        self.pad_B.reset()
    
    def run_game(self) -> None:
        while self.running:
            #set iniziale
            self.get_events()
            pygame.display.update()
            self.screen.fill((0, 0, 0))
            self.clock.tick(60)
            
            #game
            self.pad_A.changeY()
            self.pad_B.changeY()
            
            #verifica se un giocatore ha fatto punto e resetta le posizioni di tutto 
            reset = self.ball.move(self.pad_A, self.pad_B)
            if reset == True:
                self.restart()
                self.points()
                
                self.blit()
                pygame.display.update()
                time.sleep(1)
            
            #set finale
            self.points()
            self.blit()

def main():
    HomePage().home()
    
    Game().run_game()

while __name__ == "__main__":
    main()