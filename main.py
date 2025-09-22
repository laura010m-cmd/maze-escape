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

# colors
WHITE = (255, 255, 255)
BLACK = (0,0,0)
GREEN = (1, 50, 33)

font = pygame.font.SysFont('Verdana', 60)  
screen = pygame.display.set_mode((800, 600))
title_text = font.render('Maze Escape', True, WHITE)
title_pos = title_text.get_rect(center=(400, 180)) 

class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.font = pygame.font.Font(None, 32)
        self.btn_color = GREEN
        self.text_color = WHITE
        self.clicked = False
        
    def draw(self, surface):
        pygame.draw.rect(surface, self.btn_color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)  # border
        
        txt_surface = self.font.render(self.text, True, self.text_color)
        txt_rect = txt_surface.get_rect(center=self.rect.center)
        surface.blit(txt_surface, txt_rect)
        
    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            return True
        return False
    

class MazeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Maze Game")
        self.clock = pygame.time.Clock()

        self.large_font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)

        self.state = "menu"

        self.player_x = self.player_y = 1
        self.exit_x = self.exit_y = 1

        self.maze = None 
        self.cell_size = 15

        self.start_time = 0 
        self.end_time = 0 

        self.name_input = ""
        self.input_active = False 

        self.new_game()

    def new_game(self):
        size = 31
        gen = mazeGenerator(size, size)
        self.maze = gen.generate()
        self.player_x = self.player_y = 1
        self.exit_x = self.exit_y = size - 2
        self.start_time = time.time()
        self.end_time = 0 
        self.moves = 0 

    def event_handling(self):
        for event in pygame.event.get():
            if self.state == "menu":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # left click
                        if start_btn.check_click(mouse_pos):
                            print("clicked start!")
                            self.state = "play"
                            self.new_game() 



class mazeGenerator:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.wall_checker = [[True for _ in range(width)] for _ in range(height)]
        self.visited = [[False for _ in range(width)] for _ in range (height)]

    def generate(self):
        return self.generate_level()

    def generate_level(self):
        stack = [(1,1)]
        self.visited[1][1] = True
        self.wall_checker[1][1] = False
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]


        while stack:
            x, y = stack[-1]
            neighbours = []

            for dx, dy in directions:
                nx, ny = x + dx, y + dy 
                if 0 < nx < self.width - 1 and 0 < ny < self.height - 1 and not self.visited[ny][nx]:
                    neighbours.append((nx, ny, dx // 2, dy // 2))

            if neighbours:
                nx, ny, wx, wy = random.choice(neighbours)
                self.wall_checker[y + wy][x + wx] = False
                self.wall_checker[nx][ny] = True 
                stack.append((nx, ny))
            else: 
                stack.pop()
        return self.wall_checker

# button setup
start_btn = Button(320, 300, 160, 60, "START")
help_btn = Button(320, 420, 160, 60, "HELP")

game = MazeGame()

while running:
    mouse_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # left click
                if start_btn.check_click(mouse_pos):
                    print("clicked start!")
                    game.state = "play"
                if help_btn.check_click(mouse_pos):
                    print("clicked help")
                    game.state = "play"
                    game.new_game()

                   

    

    screen.fill((0, 128, 128))
    
    screen.blit(title_text, title_pos)
    start_btn.draw(screen)
    help_btn.draw(screen)
  
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()





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

# colors
WHITE = (255, 255, 255)
BLACK = (0,0,0)
GREEN = (1, 50, 33)

font = pygame.font.SysFont('Verdana', 60)  
screen = pygame.display.set_mode((800, 600))
title_text = font.render('Maze Escape', True, WHITE)
title_pos = title_text.get_rect(center=(400, 180)) 

class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.font = pygame.font.Font(None, 32)
        self.btn_color = GREEN
        self.text_color = WHITE
        self.clicked = False
        
    def draw(self, surface):
        pygame.draw.rect(surface, self.btn_color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)  # border
        
        txt_surface = self.font.render(self.text, True, self.text_color)
        txt_rect = txt_surface.get_rect(center=self.rect.center)
        surface.blit(txt_surface, txt_rect)
        
    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            return True
        return False

        

class MazeLayout():
    maze = []

    for i in range (5):
        row = []
        for j in range(5):
            cell = random.choice([0, 1])
            row.append(cell)
        maze.append(row)

    for row in maze:
        print(row)

    def DFS(maze, row, col):
        visited[row][col]  

start_btn = Button(320, 300, 160, 60, "START")
help_btn = Button(320, 420, 160, 60, "HELP")


def checkClick(mouse_pos):
    mouse_pos = pygame.mouse.get_pos()
    if start_btn.rect.collidepoint(mouse_pos):
        return(WHITE)



while running:
    mouse_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            level_screen = checkClick(mouse_pos)


    screen.fill((0, 0, 0))
        
    screen.blit(title_text, title_pos)
    start_btn.draw(screen)
    help_btn.draw(screen)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
            
