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
maze = None
player = None
start_time = 0
elapsed_time = 0
is_paused = False

WHITE = (255, 255, 255)
BLACK = (0,0,0)
GREEN = (1, 50, 33)

font = pygame.font.SysFont('Verdana', 60)  
screen = pygame.display.set_mode((800, 600))
title_text = font.render('Maze Escape', True, WHITE)
title_pos = title_text.get_rect(center=(400, 180)) 

class Button:
    def __init__(self, x, y, w, h, txt, action=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.txt = txt
        self.font = pygame.font.Font(None, 32)
        self.btn_colour = GREEN
        self.txt_colour = WHITE
        self.action  = action
        
    def draw(self, surface):
        pygame.draw.rect(surface, self.btn_colour, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)  # border
        
        txt_surface = self.font.render(self.txt, True, self.txt_colour)
        txt_rect = txt_surface.get_rect(center=self.rect.center)
        surface.blit(txt_surface, txt_rect)
        
    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            if self.action:
                self.action()
            return True
        return False


class help_button():

    def check_click(self, pos):
        dist = ((pos[0] - 50)**2 + (pos[1] - 45)**2)**0.5
        if dist <= 20:
            show_help()

    def draw(self, surface):
        pygame.draw.circle(surface, GREEN, (50, 45), 20 )
        surface.blit(pygame.font.Font(None, 32).render("?", True, WHITE), (43, 35))

    '''help_text = pygame.font.Font(None, 24).render("Use arrow keys or WASD to move ")'''

def show_help():
    global game_state
    game_state = "help"


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
    
def toggle_pause():
    global is_paused, elapsed_time, start_time, game_state
    if game_state == "playing":
        is_paused = True
        elapsed_time += pygame.time.get_ticks() - start_time
        game_state = "paused"
    elif game_state == "paused":
        is_paused = False
        start_time = pygame.time.get_ticks()
        game_state = "playing"
 
def back_to_menu():
    global game_state
    game_state = "menu"


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
help_btn = Button(43, 35, 20, 20, "?", show_help)
back_btn = Button(220, 290, 160, 50, "BACK", back_to_menu)



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
            help.check_click(mouse_pos)


            if game_state == "help":
                back_btn.check_click(mouse_pos)

    screen.fill((0, 0, 0))
    if game_state == "menu":    
        screen.blit(title_text, title_pos)
        start_btn.draw(screen)
        help.draw(screen)
        pause.draw(screen)

    elif game_state == "help":
        help_text = pygame.font.Font(None, 24).render("The aim is to complete these mazes as fast as possible \n The key controls are WASD and arrow keys \n Pausing the game pauses the timer", True, WHITE)
        screen.blit(help_text, (300 - help_text.get_width()//2, 200))
        back_btn.draw(screen)
    


    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
            
