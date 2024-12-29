import pygame
import sys
import math

# Inizializza Pygame
pygame.init()

# Costanti
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (30, 30, 30)
TEXT_COLOR = (255, 255, 255)
FPS = 60
MAX_SIZE = 100
MIN_SIZE = 50
SPEED = 0.05  # Velocità della transizione

# Crea la finestra
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lampeggio del testo")

# Imposta il font
font = pygame.font.Font(None, MIN_SIZE)

# Loop principale
clock = pygame.time.Clock()
scale = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Calcola la dimensione del testo
    size = MIN_SIZE + (MAX_SIZE - MIN_SIZE) * (0.5 + 0.5 * math.sin(scale))
    scale += SPEED

    # Aggiorna il font con la nuova dimensione
    font = pygame.font.Font(None, int(size))

    # Crea il testo
    text_surface = font.render("Lampeggia!", True, TEXT_COLOR)

    # Ottieni il rettangolo del testo e posizionalo al centro dello schermo
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    # Disegna lo sfondo
    screen.fill(BACKGROUND_COLOR)

    # Disegna il testo
    screen.blit(text_surface, text_rect)

    # Aggiorna lo schermo
    pygame.display.flip()

    # Controlla il frame rate
    clock.tick(FPS)