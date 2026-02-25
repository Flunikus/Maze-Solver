#import libraries
import pygame

pygame.init()
font = pygame.font.SysFont(None, 36)
screen_size = (600,450)
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock() 
running = True
direction = 0

# direction definitions:
'''
0 = up
1 = right
2 = down
3 = left
'''

#grid parametre
cell_size = 50
rows = screen.get_height() // cell_size
cols = screen.get_width() // cell_size
#2d list
maze = [[4,4,4,4,4,4,4,4,4,4,4,4],
        [4,3,1,1,1,1,1,1,1,1,0,4],
        [4,0,0,0,0,0,0,0,0,1,0,4],
        [4,0,1,0,1,1,1,1,1,1,1,4],
        [4,0,1,1,1,0,0,0,1,0,0,4],
        [4,0,0,1,0,1,1,1,0,0,0,4],
        [4,0,0,1,1,1,0,1,1,1,1,4],
        [4,0,0,0,0,1,0,0,1,0,2,4],
        [4,4,4,4,4,4,4,4,4,4,4,4]]

#start position
for row in range(len(maze)):
    for col in range(len(maze[row])):
        if maze[row][col] == 2:
            player_col = col
            player_row = row

#tjekker væg
def can_move(row,col):
    if row<0 or col<0:
        return False
    if row>= len(maze) or col>= len(maze[0]):
        return False
    return maze[row][col] != 0 and maze[row][col] != 4

#gå fremad
def move_forward():
    global player_col, player_row

    if direction == 0:
        if can_move(player_row-1,player_col):
            player_row -= 1
    elif direction == 2:
        if can_move(player_row+1,player_col):
            player_row += 1
    elif direction == 1:
        if can_move(player_row,player_col+1):
            player_col += 1
    elif direction == 3:
        if can_move(player_row,player_col-1):
            player_col -= 1

#drej venstre
def turn_left():
    global direction
    direction = (direction - 1 ) % 4   
#drej højre
def turn_right():
    global direction
    direction = (direction + 1) % 4

#næste pos efter dir
def get_next_step(dir):
    if dir == 0:    #up
        return player_row - 1, player_col
    if dir == 1:    #right
        return player_row, player_col+1
    if dir == 2:    #down
        return player_row+1, player_col
    if dir == 3:    #left
        return player_row, player_col-1
    
#venstre hånds reglen
def step(): 
    global direction
    
    #check venstre
    left_dir = (direction - 1 ) % 4
    row, col = get_next_step(left_dir)
    
    if can_move(row, col):
        direction = left_dir
        move_forward()
        return
    
    #check ligeud
    row, col = get_next_step(direction)
    if can_move(row, col):
        move_forward()
        return
    
    #hvis ikke drej højre
    direction = (direction + 1 ) % 4

while running:
    #clearer skærm
    screen.fill("black")
    
    #grid tegn
    for row in range(len(maze)):
        for col in range(len(maze[row])):
            rect = pygame.Rect(cell_size*col, cell_size*row, cell_size, cell_size)
            if maze[row][col]==1:
                pygame.draw.rect(screen, "black", rect, 1)#gang
            elif maze[row][col]==2:
                pygame.draw.rect(screen, "yellow", rect, 0)#start
            elif maze[row][col]==3:
                pygame.draw.rect(screen, "green", rect, 0)#mål
            elif maze[row][col]==4:
                pygame.draw.rect(screen, "red", rect, 1)#kant
            else:
                pygame.draw.rect(screen, "white", rect, 1)#væg
    
    for event in pygame.event.get(): 
        #slut event
        if event.type == pygame.QUIT:
            running = False
        
        #player auto move
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                step()
                
        #manuel styring
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                move_forward()
            if event.key == pygame.K_a:
                turn_left()
            if event.key == pygame.K_d:
                turn_right()
            
    #player pos
    player_x = player_col * cell_size + cell_size // 2
    player_y = player_row * cell_size + cell_size // 2
    player_pos = (player_x,player_y)
    
    #text maze
    text_read = font.render("MAZE SOLVER",True,"white")
    screen.blit(text_read,(220,60))
    
    #player draw
    pygame.draw.circle(screen, "blue", (player_pos), 15)
    
    #retning indikation
    if direction == 0:
        end = (player_x,player_y-15)
    elif direction == 2:
        end = (player_x,player_y+15)
    elif direction == 1:
        end = (player_x+15,player_y)
    elif direction == 3:
        end = (player_x-15,player_y)
        
    pygame.draw.line(screen,"white", (player_pos),end,2)
    
    #updater billede
    pygame.display.flip()
        
pygame.quit()
