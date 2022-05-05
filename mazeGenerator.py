from grid import *
import random
################################################################################
###############################  MAZE GENERATOR  ###############################
################################################################################

#Original source: https://medium.com/swlh/fun-with-python-1-maze-generator-931639b4fb7e
#Code modified greatly, but original structure is based on the website

def printMaze(maze):
    p, w, u = 0, 1, -1
    for i in range(0, len(maze)):
        for j in range(0, len(maze[0])):
            if maze[i][j] == u:
                print(f'{maze[i][j]}', end = ' ')
            else:
                print(f' {maze[i][j]}', end = ' ')
        print()

def mazeToString(maze):
    p, w, u = 0, 'w', -1
    s = ""
    for i in range(0, len(maze)):
        for j in range(0, len(maze[0])):
            if maze[i][j] == u:
                s += f'{maze[i][j]} '
            else:
                s += f' {maze[i][j]} '
        s+='\n'
    return s

def checkSurr(maze, row, col):
    p, w, u = 0, 'w', -1
    total = 0
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    for drow, dcol in directions:
        newRow, newCol = row+drow, col+dcol
        if maze[newRow][newCol] == p:
            total += 1
    return total

def updateSurr(maze, walls, seen, row, col):
    p, w, u = 0, 'w', -1
    #m = copy.deepcopy(maze)
    rows = len(maze)
    cols = len(maze[0])
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    for drow, dcol in directions:
        newRow, newCol = row+drow, col+dcol
        if maze[newRow][newCol] == u:
            maze[newRow][newCol] = w
            #only add if wall isnt already in the list and it isnt an edge
            if((newRow, newCol) not in seen 
                and newRow > 0 and newRow < rows-1 
                and newCol > 0 and newCol < cols-1):
                walls.append((newRow, newCol))
                seen.add((newRow, newCol))
    return maze, walls

def fillInWalls(maze, rows, cols):
    p, w, u = 0, 'w', -1
    #m = copy.deepcopy(maze)
    for i in range(rows):
        for j in range(cols):
            #if there are any unchecked cells left, make them into walls
            if maze[i][j] == u:
                maze[i][j] = w
    return maze

def createEnterAndExit(maze, rows, cols):
    p, w, u = 0, 'w', -1
    #to make the entrance, search for the first point on edge that can 
    #enter into the maze
    for i in range(cols):
        if maze[1][i] == p:
            maze[0][i] = p
            break
    #vice versa for exit
    for i in range(cols-1, 0, -1):
        if maze[rows-2][i] == p:
            maze[rows-1][i] = p
            break
    return maze

def randomizeRooms(app, maze, rows, cols):
    p, w, u = 0, 'w', -1
    for i in range(rows):
        for j in range(cols):
            if maze[i][j] == p:
                maze[i][j] = random.randint(0, len(app.layouts)-1)
    return maze

def createMaze(app, rows, cols):
    maze = [[-1]*cols for row in range(rows)]
    walls = []
    #for searching for already seen
    seen = set()
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    #p is path, w is wall, u is unchecked
    p, w, u = 0, 'w', -1
    #cannot be on the edges of the maze (row 0, or rows)
    startRow = random.randint(1, rows-2)
    startCol = random.randint(1, cols-2)
    maze[startRow][startCol] = p
    #add the walls around this start point and set those points in the
    #maze to be walls
    for drow, dcol in directions:
        newRow, newCol = startRow + drow, startCol + dcol
        #do not add edges
        if newRow > 0 and newRow < rows-1 and newCol > 0 and newCol < cols-1:            
            walls.append((newRow,newCol))
            seen.add((newRow, newCol))
            maze[newRow][newCol] = w
    #while there are still walls to pick from, keep generating
    while len(walls) > 0:
        rWall = walls[random.randint(0, len(walls)-1)]
        wallRow = rWall[0]
        wallCol = rWall[1]
        #check the spots adjacent to the wall. If only one of them
        #has been visited before, and the other is a path, make the wall into 
        # a path
        for drow, dcol in directions:
            newRow, newCol = wallRow+drow, wallCol+dcol
            #checks the opposite direciton
            oppRow, oppCol = wallRow-drow, wallCol-dcol
            #one side of the wall is unchecked, the other side is a path
            if maze[newRow][newCol] == u and maze[oppRow][oppCol] == p:
                if checkSurr(maze, wallRow, wallCol) < 2:
                    maze[wallRow][wallCol] = p
                    #updates the maze, as well as the list of walls
                    maze, walls = updateSurr(maze, walls, seen, 
                                            wallRow, wallCol)
                    #walls.remove(rWall)
        #remove the wall after all checks are done. It is either now a path, or
        #is not a valid wall to change
        walls.remove(rWall)
        seen.remove(rWall)
    maze = fillInWalls(maze, rows, cols)
    maze = createEnterAndExit(maze, rows, cols)
    maze = randomizeRooms(app, maze, rows, cols)
    return maze