import pygame 
import sys 
import random 
import json 
import os 
import time 
from datetime import datetime

pygame.init()
running = True
clock = pygame.time.Clock()

game_state = "menu"

WHITE = (255, 255, 255)
BLACK = (0,0,0)
GREEN = (1, 50, 33)

font = pygame.font.SysFont('Verdana', 60)  
screen = pygame.display.set_mode((800, 600))
title_text = font.render('Maze Escape', True, WHITE)
title_pos = title_text.get_rect(center=(400, 180)) 

class Button:
    def __init__(self, x, y, w, h, text, action=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.font = pygame.font.Font(None, 32)
        self.btn_color = GREEN
        self.text_color = WHITE
        self.action  = action
        
    def draw(self, surface):
        pygame.draw.rect(surface, self.btn_color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)  # border
        
        txt_surface = self.font.render(self.text, True, self.text_color)
        txt_rect = txt_surface.get_rect(center=self.rect.center)
        surface.blit(txt_surface, txt_rect)
        
    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            if self.action:
                self.action()
            return True
        return False

class help_button():
    def draw(self, surface):
        pygame.draw.circle(surface, GREEN, (50, 45), 20 )
        surface.blit(pygame.font.Font(None, 32).render("?", True, WHITE), (43, 35))


class pause_button():
    def draw(self, surface):
        pygame.draw.circle(surface, GREEN, (150, 45), 20 )
        surface.blit(pygame.font.Font(None, 32).render("||", True, WHITE), (144, 32))

    

help = help_button()
pause = pause_button()


def start_function():
    if checkClick((320, 300)) == True:
        screen.fill(WHITE)
    print("start game ")



class MazeLayout():
    def __init__(self, rows=5, cols=5):
        self.rows = rows
        self.cols = cols 
        self.maze = []

        for i in range (rows):
            row = []
            for j in range(cols):
                cell = random.choice([0, 1])
                row.append(cell)
            self.maze.append(row)

        for row in self.maze:
            print(row)

    def dfs(row, col, end, visited, path):
        if (row, col) == end:
            path = row, col 



start_btn = Button(320, 300, 160, 60, "START", start_function)



def checkClick(mouse_pos):
    mouse_pos = pygame.mouse.get_pos()
    if start_btn.rect.collidepoint(mouse_pos):
        return(WHITE)



while running:
    mouse_pos = pygame.mouse.get_pos()

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 


        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            start_btn.check_click(mouse_pos)


    screen.fill((0, 0, 0))
        
    screen.blit(title_text, title_pos)
    start_btn.draw(screen)
    help.draw(screen)
    pause.draw(screen)
    


    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
            
            
