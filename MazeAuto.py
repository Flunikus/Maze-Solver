import random
from enum import Enum
import numpy as np
import cv2
import sys

sys.setrecursionlimit(8000)

class Directions(Enum):
	UP = 1
	DOWN = 2
	LEFT = 3
	RIGHT = 4

class Backtracing:
    algorithm = "Recursive Backtracing"

    def __init__(self,width,height,display_maze):

        print("Using OpenCV version: " + cv2.__version__)

        # Sørger for maze er odd for at beholde symmetri og sørge for vi ik træder ud af maze
        if width % 2 == 0:
            width += 1
        if height % 2 == 0:
            height += 1

        self.width          = width
        self.height         = height
        self.display_maze   = display_maze

    def create_maze(self):
        maze = np.ones((self.height,self.width),dtype = float)

        for i in range(self.height):
            for j in range(self.width):
                if i % 2 == 1 or j % 2 == 1:    # if odd
                    maze[i,j] = 0               # Walls
                if (i == 0 or j == 0 or i == self.height -1   
                    or j == self.width -1):     # if kant     
                                
                    maze[i,j] = 0.5             # Markerer besøgt
        # Start pos
        sx = random.choice(range(2,self.width -2, 2))   
        sy = random.choice(range(2,self.height -2, 2))  

        self.generate(sx,sy,maze)

        # Farver hvid
        for i in range(self.height):
            for j in range(self.width):
                if maze[i,j] == 0.5:
                    maze[i,j] = 1

        # Laver hul til start og slut
        maze[1,2] = 1
        maze[self.height - 2, self.width - 3] = 1

        # Display maze
        if self.display_maze:
            cv2.namedWindow('Maze',cv2.WINDOW_NORMAL)
            cv2.imshow('Maze', maze)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        return 0

    def generate(self,cx,cy,grid):

        grid[cy,cx] = 0.5 # np definerer axis 0 som rows derfor y

        # Chekker if nabo er besøgt
        if(grid[cy-2,cx] == 0.5 and grid[cy+2,cx] == 0.5
           and grid[cy,cx-2] == 0.5 and grid[cy,cx +2] == 0.5):
            pass
        else:
            li = [1,2,3,4]
            while len(li) > 0:
                dir = random.choice(li)
                li.remove(dir)

                if dir ==  Directions.UP.value:
                    nx = cx
                    mx = cx
                    ny = cy - 2
                    my = cy - 1
                elif dir == Directions.DOWN.value:
                    nx = cx
                    mx = cx
                    ny = cy + 2
                    my = cy + 1
                elif dir == Directions.LEFT.value:
                    nx = cx - 2
                    mx = cx - 1
                    ny = cy 
                    my = cy 
                elif dir == Directions.RIGHT.value:
                    nx = cx + 2
                    mx = cx + 1
                    ny = cy
                    my = cy
                else:
                    nx = cx
                    mx = cx
                    ny = cy
                    my = cy
                
                if grid[ny, nx] != 0.5:
                    grid[my,mx] = 0.5
                    self.generate(nx,ny,grid)
            
maze1 = Backtracing(50,50,True)
maze1.create_maze()

    


                    


    