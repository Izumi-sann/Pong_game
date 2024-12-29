import pygame
import math

class Pad():
    def __init__(self, X, Y, screen:tuple) -> None:
        self.texture = pygame.image.load(r"assets\Pad (Custom).png")
        self.screen = screen
        self.dimensioni = (18, 100)
        
        self.start_position = [X, Y]
        self.position = self.start_position[:]
        self.position_2 = [X+self.dimensioni[0], Y+self.dimensioni[1]]
        
        self.speed = 3
        self.movement = [False, False] #[-y, +y] [UP, DOWN]
        
        self.punteggio = 0
    
    def changeY(self) -> None:
        if not self.position[1] > 0:
            self.movement[0] = False
        elif not self.position_2[1] < self.screen[1]:
            self.movement[1] = False
        
        self.position[1] += ((self.movement[1]) - (self.movement[0])) * self.speed
        self.position_2[1] = self.position[1] + 100
    
    def reset(self) -> None:
        self.position = self.start_position[:]
        self.position_2 = [self.position[0] + self.dimensioni[0], self.position[1] + self.dimensioni[1]]

class Ball():
    def __init__(self, heigth, width, move) -> None:
        self.screen = (width, heigth)
        self.dimensioni = (40, 40)
        
        self.start_position = [(self.screen[0]/2)-self.dimensioni[0]/2, (self.screen[1]/2)-self.dimensioni[1]/2]#[X, Y] centrata
        self.position = self.start_position[:]
        self.position_2 = [self.position[0] + 40, self.position[1] + 40]
        
        self.X_movement = [False, move] #LEFT, RIGHT
        self.Y_movement = [False, move] #UP, DOWN
        
        self.speed = 3
        self.acceleration = 0.001
        
        self.texture = pygame.image.load(r"assets\Ball (Custom).png")
        
        self.bounce = 0 #rimbalzi fatti
    
    def check_collision(self, pad_A:Pad, pad_B:Pad) -> None:
        #collisione PAD A
        if self.position[0] <= pad_A.position_2[0] and (pad_A.position[1] <= self.position[1] <= pad_A.position_2[1] or pad_A.position[1] <= self.position_2[1] <= pad_A.position_2[1]):
            self.X_movement = [False, True]
            
            #rimbalzo palla y
            if not pad_A.movement == [True, True] and not pad_A.movement == [False, False]:
                self.Y_movement[0] = pad_A.movement[0]
                self.Y_movement[1] = pad_A.movement[1]
            
            self.acceleration += 0.00001
            self.bounce += 1
        
        #collisione PAD B
        if self.position_2[0] >= pad_B.position[0] and (pad_B.position[1] <= self.position[1] <= pad_B.position_2[1] or pad_B.position[1] <= self.position_2[1] <= pad_B.position_2[1]):
            self.X_movement = [True, False]
            
            #rimbalzo palla y
            if not pad_B.movement == [True, True] and not pad_B.movement == [False, False]:
                self.Y_movement[0] = pad_B.movement[0]
                self.Y_movement[1] = pad_B.movement[1]
            
            self.acceleration += 0.00001
            self.bounce += 1

    def move(self, pad_A:Pad, pad_B:Pad) -> bool:
        
        if self.position[0] + 40 >= self.screen[0]:#rimbalzo lati
            pad_A.punteggio += 1
            return True
        if self.position[0] <= 0:
            pad_B.punteggio += 1
            return True
        
        if self.position_2[1] >= self.screen[1]:
            self.Y_movement = [True, False]
        if self.position[1] <= 0:
            self.Y_movement = [False, True]
        
        self.check_collision(pad_A=pad_A, pad_B=pad_B)
        
        self.position[0] += ((self.X_movement[1]) - (self.X_movement[0])) * self.speed
        self.position[1] += ((self.Y_movement[1]) - (self.Y_movement[0])) * self.speed
        self.position_2 = [self.position[0] + 40, self.position[1] + 40]
        
        self.speed += self.acceleration
        print(self.speed)
        
        return False

    def change_XY(self) -> None:
        if not self.position[1] > 0:
            self.Y_movement[0] = False
        elif not self.position_2[1] < self.screen[1]:
            self.Y_movement[1] = False
        
        if not self.position[0] > 0:
            self.X_movement[0] = False
        elif not self.position_2[0] < self.screen[0]:
            self.X_movement[1] = False
        
        self.position[0] += ((self.X_movement[1]) - (self.X_movement[0])) * self.speed
        self.position_2[0] = self.position[0] + 40
        
        self.position[1] += ((self.Y_movement[1]) - (self.Y_movement[0])) * self.speed
        self.position_2[1] = self.position[1] + 40

    def reset(self):
        self.position = self.start_position[:]
        self.position_2 = [self.position[0] + 40, self.position[1] + 40]
        self.X_movement = [False, True]
        self.Y_movement = [False, True]
        self.speed = 3
        self.bounce = 0