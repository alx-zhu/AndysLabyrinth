from grid import *
import copy

################################################################################
####################################  ROOM  ####################################
################################################################################

#creates the walls and floors necesarry for a room based on the rooms around it
def getWallsAndFloors(app, left, right, up, down):
    wallsAndFloors = []
    #left, right, up and down tell where the doors are.
    #will return a list of the coordinates of the walls.
    if left == True:
        wallsAndFloors.append((app.leftBorder, 0, app.leftBorder + 10, 
                        app.height/2 - 80))
        wallsAndFloors.append((app.leftBorder, app.height/2 + 80, 
                        app.leftBorder + 10, app.height))
    else: 
        wallsAndFloors.append((app.leftBorder, 0, app.leftBorder + 10, app.height))
    
    if right == True:
        wallsAndFloors.append((app.width-10, 0, app.width, app.height/2 - 80))
        wallsAndFloors.append((app.width-10, app.height/2 + 80, 
                                app.width, app.height))
    else:
        wallsAndFloors.append((app.width-10, 0, app.width, app.height))
    
    if up == True:
        wallsAndFloors.append((app.leftBorder, 0, 
                    app.leftBorder + app.gameWidth/2 - 80, 10))
        wallsAndFloors.append((app.leftBorder + app.gameWidth/2 + 80, 
                    0, app.width, 10))
    else:
        wallsAndFloors.append((app.leftBorder, 0, app.width, 10))
    
    if down == True:
        wallsAndFloors.append((app.leftBorder, app.height-20, 
                    app.leftBorder + app.gameWidth/2 - 80, app.height))
        wallsAndFloors.append((app.leftBorder + app.gameWidth/2 + 80, 
                    app.height-20, app.width, app.height))
    else:
        wallsAndFloors.append((app.leftBorder, app.height-20, app.width, app.height))
    return wallsAndFloors

def isLegal(app, row, col):
    if row < 0 or row >= len(app.map) or col < 0 or col >= len(app.map[0]):
        return False
    elif app.map[row][col] == 'w':
        return False
    else:
        return True

#combines platforms since the long platformsa are actually 2 or 3 platforms
#put together. 
#May not be used in final game. Just to easily create new room layouts without
#having to calculate the x and y coordinates.
def combinePlatforms(app, rowColsList):
    plats = copy.copy(rowColsList)
    previous = plats[0]
    plats = plats[1:]
    #returns a list of lists of the combined platforms in format:
    #[[row, col, row, col, row, col], [row, col, row, col], etc.]
    combinedPlatformsRowCol = combinePlatsHelper(app, previous, plats, 
                                    [previous[0], previous[1]], [])
    #makes each list of row, col, row, col into a single tuple of 
    # (x1, y1, x2, y2)
    combinedPlatforms = convertToXYCoords(app, combinedPlatformsRowCol)
    return combinedPlatforms

#combines adjacent platforms by storing them in lists, [row, col, row, col, etc]
#Stores these combined platforms in combinedList. They will then be changed to
#be only one platform later using getCellBounds
def combinePlatsHelper(app, previous, uncombined, combinedPlat, combinedList):
    if uncombined == []:
        if len(combinedPlat) != 0:
            combinedList.append(combinedPlat)
        return combinedList
    else:
        current = uncombined[0]
        currRow = current[0]
        currCol = current[1]
        #print(currRow, currCol, combinedPlat)
        prevRow = previous[0]
        prevCol = previous[1]
        #if they are in the same row, and adjacent cols, add to the combined
        #Tuple. Otherwise, add the combinedPlat to combinedList if it is not
        #empty. then empty the combinedPlat
        if currRow == prevRow and abs(currCol - prevCol) == 1:
            combinedPlat.append(currRow)
            combinedPlat.append(currCol)
        else:
            #if combinedPlat is actually a platform, add it to the list
            if len(combinedPlat) > 0:
                combinedList.append(combinedPlat)
                #now set combinedPlat to the new platform. The old platform
                #was just added to the list.
                combinedPlat = [currRow, currCol]
        return combinePlatsHelper(app, current, uncombined[1:], 
                                    combinedPlat, combinedList)

def convertToXYCoords(app, rowColList):
    xyCoordsList = []
    for platform in rowColList:
        #use the first and last platform to get dimensions for entire platform
        #only using x1 of first, and x2 and y2 of last platform
        x1, a, b, c = getCellBounds(app, platform[0], platform[1])
        a, b, x2, y2 = getCellBounds(app, platform[-2], platform[-1])
        xyCoordsList.append((x1, y2 - app.platformHeight, x2, y2))
    return xyCoordsList

