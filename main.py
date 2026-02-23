import pygame 
import sys 
import random 
import os 
import time 
from datetime import datetime
import sqlite3


new_database = sqlite3.connect("leaderboard_input.db")
cursor = new_database.cursor()

leaderboard_list = []

pygame.init()
running = True
clock = pygame.time.Clock()

x = 170
y = 120
TILE = 40
COLS, ROWS = 10, 10
level = 1
level_font = pygame.font.SysFont('Verdana', 30)

game_state = "menu"
maze = None
player = None
elapsed_time = 0
is_paused = False
velocity = 4
player_pos = pygame.Vector2(800/2, 600/2)

input_box = pygame.Rect(350, 220, 500, 35)
#input box colours: default is grey vs white when clicked 
box_clicked = pygame.Color(255, 255, 255)
box_default = pygame.Color(128, 128, 128)
colour = box_default 
input_text = ''

clicked = False

WHITE = (255, 255, 255)
BLACK = (0,0,0)
GREEN = (1, 50, 33)

font = pygame.font.SysFont('Verdana', 60)  
screen = pygame.display.set_mode((800, 600))
title_text = font.render('Maze Escape', True, WHITE)
title_pos = title_text.get_rect(center=(400, 180)) 

pygame.display.set_caption("Maze Escape")

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
        pygame.draw.rect(surface, BLACK, self.rect, 2) 
        
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
        pygame.draw.circle(surface, GREEN, (120, 45), 20 )
        surface.blit(pygame.font.Font(None, 32).render("||", True, WHITE), (114, 32))

    def check_click(self, pos):
        dist = ((pos[0] - 120)**2 + (pos[1] - 45)**2)**0.5
        if dist <= 20:
            toggle_pause()


    

help = help_button()
pause = pause_button()


def start_function():
    global game_state, maze, start_time, x, y 
    x = 170
    y = 120
    velocity = 5
    game_state = "playing"
    if checkClick((320, 300)) == True and game_state == "menu":
        game_state = "playing"
    maze = generate_maze()
    start_time = pygame.time.get_ticks()
    

    
def toggle_pause():
    global is_paused, elapsed_time, start_time, game_state
    if game_state == "playing":
        is_paused = True
        elapsed_time += (pygame.time.get_ticks() - start_time)
        game_state = "paused"
    elif game_state == "paused":
        is_paused = False
        start_time = pygame.time.get_ticks()
        game_state = "playing"
 
def back_to_menu():
    global game_state, level, total_seconds, elapsed_seconds
    game_state = "menu"
    level = 1 
    total_seconds = 0
    elapsed_seconds = 0 




class Cell:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False

    def draw(self, sc):
        x, y = self.x * TILE + 150, self.y * TILE + 100
        if self.walls['top']:
            pygame.draw.line(sc, pygame.Color('white'), (x, y), (x + TILE, y), 2)
        if self.walls['right']:
            pygame.draw.line(sc, pygame.Color('white'), (x + TILE, y), (x + TILE, y + TILE), 2)
        if self.walls['bottom']:
            pygame.draw.line(sc, pygame.Color('white'), (x + TILE, y + TILE), (x, y + TILE), 2)
        if self.walls['left']:
            pygame.draw.line(sc, pygame.Color('white'), (x, y + TILE), (x, y), 2)

    def check_neighbours(self, grid):
        neighbours = []
        # Index math for 1D grid list
        get_idx = lambda x, y: x + y * COLS
        
        if self.y > 0: neighbours.append(grid[get_idx(self.x, self.y - 1)]) # top
        if self.x < COLS - 1: neighbours.append(grid[get_idx(self.x + 1, self.y)]) # right
        if self.y < ROWS - 1: neighbours.append(grid[get_idx(self.x, self.y + 1)]) # bottom
        if self.x > 0: neighbours.append(grid[get_idx(self.x - 1, self.y)]) # left

        unvisited = [n for n in neighbours if n and not n.visited]
        return random.choice(unvisited) if unvisited else None

def remove_walls(current, next_cell):
    dx, dy = current.x - next_cell.x, current.y - next_cell.y
    if dx == 1: current.walls['left'] = next_cell.walls['right'] = False
    elif dx == -1: current.walls['right'] = next_cell.walls['left'] = False
    if dy == 1: current.walls['top'] = next_cell.walls['bottom'] = False
    elif dy == -1: current.walls['bottom'] = next_cell.walls['top'] = False

def generate_maze():
    
    grid = [Cell(col, row) for row in range(ROWS) for col in range(COLS)]
    current = grid[0]
    stack = []
    visited_count = 1

    while visited_count < len(grid):
        current.visited = True
        next_cell = current.check_neighbours(grid)
        if next_cell:
            next_cell.visited = True
            visited_count += 1
            stack.append(current)
            remove_walls(current, next_cell)
            current = next_cell
        elif stack:
            current = stack.pop()
    return grid
    
'''class MazeLayout():
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
            path = row, col''' 

'''def display_maze():
    file  = open("mazefile.txt")'''


exit_rect = pygame.Rect(510, 460, 40, 40)

start_btn = Button(320, 300, 160, 60, "START", start_function)
help_btn = Button(43, 35, 20, 20, "?", show_help)
back_btn = Button(330, 310, 160, 50, "BACK", back_to_menu)
resume_btn = Button(330, 310, 160, 50, "RESUME", toggle_pause)
menu_btn = Button(550, 20, 160, 60, "MENU", back_to_menu)



def checkClick(mouse_pos):
    mouse_pos = pygame.mouse.get_pos()




while running:
    mouse_pos = pygame.mouse.get_pos()
  
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 

        key_pressed = pygame.key.get_pressed()


        if event.type == pygame.MOUSEBUTTONDOWN:

            mouse_pos = pygame.mouse.get_pos()
            help.check_click(mouse_pos)
            pause.check_click(mouse_pos)
            
            if game_state == "leaderboard_input":
                if input_box.collidepoint(event.pos):
                    clicked = True
                else:
                    clicked = False

            if game_state == "menu":
                start_btn.check_click(mouse_pos)

            if game_state == "help":
                back_btn.check_click(mouse_pos)

            if game_state == "paused":
                resume_btn.check_click(mouse_pos)

            if game_state == "leaderboard":
                menu_btn.check_click(mouse_pos)
        
        if event.type == pygame.KEYDOWN and game_state == "leaderboard_input":
            if event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            elif event.key == pygame.K_RETURN:
                #print(f"Final Name: {input_text}")
                #cursor.execute("""CREATE TABLE playerStats(Name TEXT, Time INTEGER) """)
                cursor.execute("INSERT INTO playerStats (Name, Time) VALUES (?, ?)", (input_text, total_seconds))
                cursor.execute("SELECT * FROM playerStats")
                cursor.execute("SELECT Name, Time FROM PlayerStats ORDER BY Time ASC LIMIT 10;")

                leaderboard_list = []
                for row in cursor.fetchall():
                     entry = f"{row[0]}:            {row[1] // 60} minutes {row[1] % 60} seconds"
                     leaderboard_list.append(entry)
                # Commit changes and close connection
                new_database.commit()
                input_text = ""
                game_state = "leaderboard"
            else:
                if event.unicode.isprintable():
                    input_text = input_text + event.unicode
    if clicked:
        colour = box_clicked
    else:
        colour = box_default



    screen.fill((0, 0, 0))
    if game_state == "menu":    
        screen.blit(title_text, title_pos)
        start_btn.draw(screen)
        help.draw(screen)
        pause.draw(screen)

    elif game_state == "help":
        help_text_l1 = pygame.font.Font(None, 24).render("The aim is to complete these mazes as fast as possible", True, WHITE)
        screen.blit(help_text_l1, (300 - help_text_l1.get_width()//2, 200))
        back_btn.draw(screen)

    elif game_state == "leaderboard":
        y = 100
        leaderboard_title = level_font.render('Leaderboard', True, WHITE)
        screen.blit(leaderboard_title, (300, 50)) 
        for i in leaderboard_list:
            display_list = level_font.render(i, True, (255, 255, 255))
            screen.blit(display_list, (50, 10 + y))
            y += 50
        menu_btn.draw(screen)

    elif game_state == "paused":
        screen.fill(BLACK)
        pause_text = level_font.render("Paused", True, WHITE)
        screen.blit(pause_text, (350, 250))
        resume_btn.draw(screen)
        


    elif game_state == "playing":
        
        # Draw the generated maze cells


        if maze:
            for cell in maze:
                cell.draw(screen)
        # Draw player
        player = pygame.draw.circle(screen, (255, 255, 255), (x, y), 8)

        level_display = f"Level: {level}"
        screen.blit(level_font.render(level_display, True, WHITE), (350, 50))
        
        if exit_rect.collidepoint((x, y)) == True:
            maze = generate_maze()
            x = 170
            y = 120
            level = level + 1 

            if level > 10:
                game_state = "leaderboard_input"
                


        total_seconds = ((( pygame.time.get_ticks() - start_time) + elapsed_time) // 1000) 
        minutes = total_seconds // 60
        seconds = total_seconds % 60
  
        if seconds == 60:
            minutes = minutes + 1 
        display_time = f"Time:  {minutes}:{seconds:02d}"


        time_font = pygame.font.SysFont('Verdana', 30)

        screen.blit(time_font.render(display_time, True, WHITE), (150, 50))


        column = (x - 150) // TILE
        row  = (y - 100) // TILE

        index = column + (row * COLS)
        current_cell = maze[index]

        right_edge = x + 8 + velocity
        left_edge = x - 8 - velocity
        top_edge = y - 8 - velocity 
        bottom_edge = y + 8 + velocity

        key_pressed = pygame.key.get_pressed()
        if current_cell.walls['left'] == False or left_edge > column * TILE + 150:
            if key_pressed[pygame.K_LEFT] or key_pressed[pygame.K_a]:
                x -= velocity
        if current_cell.walls['right'] == False or right_edge < column * TILE + 150 + TILE:
            if key_pressed[pygame.K_RIGHT] or key_pressed[pygame.K_d]:
                x += velocity
        if current_cell.walls['top'] == False or top_edge > row * TILE + 100:
            if key_pressed[pygame.K_UP] or key_pressed[pygame.K_w]:
                y -= velocity
        if current_cell.walls['bottom'] == False or bottom_edge < row * TILE + 100 + TILE:
            if key_pressed[pygame.K_DOWN] or key_pressed[pygame.K_s]:
                y += velocity 

    elif game_state == "leaderboard_input":
       screen.fill((0, 0, 0))
       screen.blit(level_font.render(f"Enter name:  ", True, WHITE), (300, 50))
       
       pygame.draw.rect(screen, colour, input_box)
       text_surface = level_font.render(input_text, True, (0, 0, 0))
       screen.blit(text_surface, (input_box.x+5, input_box.y+5))
       input_box.width = max(250, text_surface.get_width()+10)

    pause.draw(screen)
        
  
    pygame.display.flip()
    clock.tick(60)

new_database.close()
pygame.quit()
sys.exit()
            
            
