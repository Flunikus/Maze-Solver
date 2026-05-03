# Import libraries
import pygame
import random
from enum import Enum
import numpy as np
import sys

#-----------------------------------
# Maze generation
#-----------------------------------
sys.setrecursionlimit(100000)

# Konstanter
WALL    = 0
PATH    = 1
START   = 2
GOAL    = 3
VISITED = 0.5

# Maze generation retninger
class MazeDirections(Enum):
	UP     = 1
	DOWN   = 2
	LEFT   = 3
	RIGHT  = 4
# Algoritmen til maze generering
class Backtracing:
    algorithm = "Recursive Backtracing"

    def __init__(self,width,height):
        
        # Sørger for maze er odd for at beholde symmetri og sørge for vi ik træder ud af maze
        if width % 2  == 0:
            width     += 1

        if height % 2 == 0:
            height    += 1

        self.width    = width
        self.height   = height
    # Laver 2d array der er vores maze
    def create_maze(self):
        maze = np.ones((self.height,self.width))

        for i in range(self.height):
            for j in range(self.width):
                if i % 2 == 1 or j % 2 == 1:   # if odd
                    maze[i,j] = WALL           # Walls

                if (i == 0 or j == 0 or i == self.height -1   
                    or j == self.width -1):    # if kant      
                    maze[i,j] = VISITED        # Markerer kant besøgt
        # Start pos
        sx = random.choice(range(2,self.width -2, 2))   
        sy = random.choice(range(2,self.height -2, 2))  

        self.generate(sx,sy,maze)

        # Farver besøgte tiles
        for i in range(self.height):
            for j in range(self.width):
                if maze[i,j] == VISITED:
                    maze[i,j] = PATH

        # Laver hul til start og slut
        maze[1,2] = GOAL
        maze[self.height - 2, self.width - 3] = START

        return maze
    # Carver stigen
    def generate(self,cx,cy,grid):
        grid[cy,cx] = VISITED # np definerer axis 0 som rows derfor y

        # Chekker if nabo er besøgt
        if(grid[cy-2,cx] == VISITED  and
            grid[cy+2,cx] == VISITED and
            grid[cy,cx-2] == VISITED and 
            grid[cy,cx +2] == VISITED):
            pass
        else:
            li = [1,2,3,4]
            while len(li) > 0:
                dir = random.choice(li)
                li.remove(dir)

                if dir ==  MazeDirections.UP.value:
                    nx = cx
                    mx = cx
                    ny = cy - 2
                    my = cy - 1
                elif dir == MazeDirections.DOWN.value:
                    nx = cx
                    mx = cx
                    ny = cy + 2
                    my = cy + 1
                elif dir == MazeDirections.LEFT.value:
                    nx = cx - 2
                    mx = cx - 1
                    ny = cy 
                    my = cy 
                elif dir == MazeDirections.RIGHT.value:
                    nx = cx + 2
                    mx = cx + 1
                    ny = cy
                    my = cy
                else:
                    nx = cx
                    mx = cx
                    ny = cy
                    my = cy
                
                if grid[ny, nx] != VISITED:
                    grid[my,mx] = VISITED
                    self.generate(nx,ny,grid)

#-----------------------------------
# Gameplay loop (Solve)
#-----------------------------------
pygame.init()

# Grid parametre 
maze_size_x = 50
maze_size_y = 50
cell_size = 10

maze_type = Backtracing(maze_size_x, maze_size_y)
maze = maze_type.create_maze()

# Skærm config
screen_size_x = (maze_size_x+1)*cell_size
screen_size_y = (maze_size_y+1)*cell_size
screen_size = ((maze_size_x+1)*cell_size,(maze_size_y+1)*cell_size)
screen = pygame.display.set_mode(screen_size)

# Engine config
clock = pygame.time.Clock() 
font = pygame.font.SysFont(None, screen_size_x // 5)

# Move direction
UP     = 0
RIGHT  = 1
DOWN   = 2
LEFT   = 3

# Start conditions
running   = True
finished  = False
show_text = True
move_dir  = UP

# Start position
def start_pos():
    for row in range(len(maze)):
        for col in range(len(maze[row])):
            if maze[row][col] == START:
                player_col = col
                player_row = row

                return player_col, player_row
player_col, player_row = start_pos()

# Tjekker om væg
def can_move(row,col):
    global finished
    if row < 0 or col < 0:
        return False
    if row >= len(maze) or col >= len(maze[0]):
        return False
    return maze[row][col] != WALL

# Gå fremad
def move_forward():
    global player_row, player_col, finished

    next_row, next_col = player_row, player_col

    if move_dir == UP:
        next_row -= 1
    elif move_dir == DOWN:
        next_row += 1
    elif move_dir == RIGHT:
        next_col += 1
    elif move_dir == LEFT:
        next_col -= 1

    if can_move(next_row, next_col):
        player_row, player_col = next_row, next_col
        if maze[player_row][player_col] == GOAL:
            finished = True

# Drej til venstre
def turn_left():
    global move_dir
    move_dir = (move_dir - 1 ) % 4   

# Drej til højre
def turn_right():
    global move_dir
    move_dir = (move_dir + 1) % 4

# Næste pos efter dir
def get_next_step(dir):
    if dir == UP:   
        return player_row - 1, player_col
    
    if dir == RIGHT:    
        return player_row, player_col+1
    
    if dir == DOWN:   
        return player_row+1, player_col
    
    if dir == LEFT:    
        return player_row, player_col-1
    
# Venstre hånds reglen
def step(): 
    global move_dir, finished
    
    # Check venstre
    left_dir = (move_dir - 1 ) % 4
    row, col = get_next_step(left_dir)
    
    if can_move(row, col):
        move_dir = left_dir
        move_forward()
        if finished == True:
            reset()
        return
    
    # Check ligeud
    row, col = get_next_step(move_dir)
    if can_move(row, col):
        move_forward()
        return
    
    # Hvis ikke drej højre
    move_dir = (move_dir + 1 ) % 4

# Reset funktion    
def reset():
    global finished, maze, player_col, player_row, move_dir
    maze = maze_type.create_maze()
    player_col, player_row = start_pos()
    move_dir = 0
    finished = False

# Loop update   
while running:
    # Clearer skærm
    screen.fill("black")
    
    # Grid tegn
    for row in range(len(maze)):
        for col in range(len(maze[row])):
            rect = pygame.Rect(cell_size*col, cell_size*row, cell_size, cell_size)

            if maze[row][col]   == PATH:
                pygame.draw.rect(screen, "black", rect, 1)  

            elif maze[row][col] == START:
                pygame.draw.rect(screen,"grey", rect, 0) 

            elif maze[row][col] == GOAL:
                pygame.draw.rect(screen,"grey", rect, 0) 

            elif maze[row][col] == WALL:
                pygame.draw.rect(screen, "white", rect, 1)      

    # Key presses
    pressed_keys = pygame.key.get_pressed()

    # Player auto move
    if pressed_keys[pygame.K_TAB]:
        step()
    
    for event in pygame.event.get():

        # Sslut event
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            show_text = False
        # Player step
            if event.key == pygame.K_SPACE:
                step()

        # Manuel styring
            elif event.key == pygame.K_w:
                move_forward()
            elif event.key == pygame.K_a:
                turn_left()
            elif event.key == pygame.K_d:
                turn_right()
        # Restart
            elif event.key == pygame.K_r:
                reset()

    # Player pos
    player_x = player_col * cell_size + cell_size // 2
    player_y = player_row * cell_size + cell_size // 2
    player_pos = (player_x,player_y)
    
    # Titel maze
    if show_text == True:
        text_read = font.render("MAZE SOLVER",True,"white")
        text_pos = text_read.get_rect(center=(screen_size_x/2, screen_size_y/2))
        screen.blit(text_read,text_pos)

    # Player draw
    player_size = cell_size/2
    pygame.draw.circle(screen, "white", (player_pos), player_size)

    # Retning indikation
    if move_dir == UP:
        end = (player_x,player_y-player_size)
    elif move_dir == DOWN:
        end = (player_x,player_y+player_size)
    elif move_dir == RIGHT:
        end = (player_x+player_size,player_y)
    elif move_dir == LEFT:
        end = (player_x-player_size,player_y)
        
    pygame.draw.line(screen,"black", (player_pos),end,2)
    
    # Updater billede
    pygame.display.flip()
    clock.tick((maze_size_x*maze_size_y)/10)
""" 
    #----------------------------
    #Assertions
    #----------------------------
    def test_maze_size_is_odd():
        generator = Backtracing(50, 50)

        assert generator.width % 2 == 1
        assert generator.height % 2 == 1
    
    def test_maze_contains_start_and_goal():
        generator = Backtracing(50, 50)
        test_maze = generator.create_maze()

        assert START in test_maze
        assert GOAL in test_maze
    
    def test_maze_shape():
        generator = Backtracing(50, 50)
        test_maze = generator.create_maze()

        assert test_maze.shape == (51, 51)
print(f"Test fejl: {test_maze_contains_start_and_goal()}")
print(f"Test fejl:{test_maze_shape()}")
print(f"Test fejl:{test_maze_size_is_odd()}")
"""
pygame.quit()