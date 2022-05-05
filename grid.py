################################################################################
###################################  GRID  #####################################
################################################################################

def getCell(app, x, y):
    gridWidth  = app.gameWidth - 2*app.margin
    gridHeight = app.height - 2*app.margin
    cellWidth  = gridWidth / app.cols
    cellHeight = gridHeight / app.rows
    row = int((y - app.margin) / cellHeight)
    col = int((x - app.margin) / cellWidth)
    return (row, col)

def getCellBounds(app, row, col):
    gridWidth  = app.gameWidth
    gridHeight = app.height
    cellWidth = gridWidth / app.cols
    cellHeight = gridHeight / app.rows
    x0 = app.margin + app.leftBorder + col * cellWidth
    x1 = app.margin + app.leftBorder + (col+1) * cellWidth
    y0 = app.margin + row * cellHeight
    y1 = app.margin + (row+1) * cellHeight
    return (x0, y0, x1, y1)

def drawGrid(app, canvas):
    for row in range(app.rows):
        for col in range(app.cols):
            (x0, y0, x1, y1) = getCellBounds(app, row, col)
            canvas.create_rectangle(x0, y0, x1, y1)
            midX = (x1-x0)/2
            midY = (y1-y0)/2
            canvas.create_text(x0 + midX, y0 + midY - 15, 
                    text = f"({row},{col})", font = "Arial 15", anchor = "n")

################################  Minimap Grid  ################################

def mapCellBounds(app, row, col):
    width = app.mapWidth
    height = app.mapWidth
    cellWidth = width/app.mapRows
    cellHeight = width/app.mapCols
    x0 = app.mapMargin + col * cellWidth
    x1 = app.mapMargin + (col+1) * cellWidth
    y0 = (app.height - height - app.mapMargin) + row * cellHeight
    y1 = (app.height - height - app.mapMargin) + (row+1) * cellHeight
    return (x0, x1, y0, y1)

def drawMapGrid(app, canvas):
    for row in range(app.mapRows):
        for col in range(app.mapCols):
            x0, x1, y0, y1 = mapCellBounds(app, row, col)
            if (row, col) == app.currentRoom:
                canvas.create_rectangle(x0, y0, x1, y1, fill = "red",
                outline = "red")
            elif (row, col) in app.visited and app.visited[(row, col)] > 0:
                canvas.create_rectangle(x0, y0, x1, y1, fill = "gray",
                outline = "gray")
            elif (row, col) in app.visited and app.visited[(row, col)] == 0:
                canvas.create_rectangle(x0, y0, x1, y1, fill = "white",
                outline = "white")
            else:
                canvas.create_rectangle(x0, y0, x1, y1, fill = "black",
                    outline = "red")