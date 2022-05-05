from cmu_112_graphics import *
from playerAndMonsters import *
from weapons import *
from mazeGenerator import *
from roomGenerator import *
from grid import *
from drawFunctions import *


################################################################################
############################  ANDY'S LABYRINTH  ################################
################################################################################

################################################################################
##############################  APP  STARTED  ##################################
################################################################################

def appStarted(app):
    app.gameOver = False
    app.win = False
    app.player = Player(app)
    #grid
    app.drawGrid = False
    app.rows = 10
    app.cols = 10
    app.leftBorder = 300
    app.gameWidth = app.width-app.leftBorder
    app.margin = 0
    app.mapMargin = 50
    app.mapWidth = 200
    #other
    app.timerDelay = 50
    app.g = 250
    #monster stats
    app.monsterHp = 50
    app.monsterDmg = 20
    #list of platforms
    app.platformHeight = 20
    app.floor = (0, app.height - 20, app.width, app.height)
    app.layouts = [
                    #layout 0
                    [ (8, 1), (8, 2), 
                      (7, 4), (7, 5), 
                      (5, 8), (5, 9), 
                      (5, 0), (5, 1),
                      (3, 4), (3, 5), (3, 6), 
                      (2, 0), (2, 1),
                      (1, 4), (1, 5), 
                      (1, 8), (1, 9),
                      (8, 7), (8, 8), (8, 9) ],

                    #layout 1
                    [ (7, 2), (7, 3), (7, 4),
                      (8, 6), (8, 7),
                      (5, 6), (5, 7), (5, 8), (5, 9),
                      (4, 2), (4, 3),
                      (3, 8), (3, 9),
                      (2, 0), (2, 1), (2, 2),
                      (1, 5), (1, 6), (1, 7),
                      (5, 0)                
                    ],

                    #layout 2
                    [ (5, 0),
                      (5, 9),
                      (5, 3), 
                      (5, 6), 
                      (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7),
                      (3, 2), (3, 3), (3, 4), (3, 5),
                      (2, 8), (2, 9),
                      (1, 1), (1, 2), (1, 3), (1, 4), (1, 5)
                    ]
                ]
    app.platforms = []
    #map
    app.showMap = False
    app.mapRows = 8
    app.mapCols = app.mapRows
    startGame(app)
    
    '''app.monsters = []
    app.drops = []
    app.projectiles = []    #starting position
    app.player.cx = app.leftBorder + app.player.cw + 20
    app.player.cy = app.height - app.player.ch'''

def startGame(app):
    app.gameOver = False
    app.win = False
    #starting position
    app.player.cx = app.leftBorder + app.player.cw + 20
    app.player.cy = app.height - app.player.ch
    app.player.hp = app.player.maxHp
    app.monsters = []
    app.drops = []
    app.projectiles = []
    app.explosions = []
    app.weaponIndex = 0
    app.loadout = [BasicWeapon()]
    app.player.weapon = app.loadout[0]
    app.heavyDropped = False
    app.railDropped = False
    app.bombDropped = False
    app.map = createMaze(app, app.mapRows, app.mapCols)
    app.currentRoom = ()
    app.visited = dict()
    #find the entrance
    for col in range(len(app.map[0])):
        if app.map[0][col] != 'w':
            app.currentRoom = (0, col)
            break
    #app.visited.add(app.currentRoom)
    app.visited[app.currentRoom] = 3
    app.player.loadRoom(app, app.currentRoom[0], app.currentRoom[1])

def winStats(app):
    app.monsterHp*=1.1
    app.monsterHp= int(app.monsterHp)
    app.monsterDmg *= 1.1
    app.mapRows += 1
    app.mapCols = app.mapRows
    #print(app.monsterHp, app.monsterDmg)

######################## Built-in Controller Functions #########################

def mousePressed(app, event):
    if event.y > 420 and event.y < 480:
        if app.gameOver == True:
            if event.x > 550 and event.x < 610:
                app.player.maxHp += 10
                app.player.hp = app.player.maxHp
                startGame(app)
            elif event.x > 670 and event.x < 730:
                app.player.bonusDmg += 10
                app.player.hp = app.player.maxHp
                startGame(app)
            elif event.x > 790 and event.x < 850:
                app.player.armor += 5
                app.player.hp = app.player.maxHp
                startGame(app)
        elif app.win == True:
            if event.x > 550 and event.x < 610:
                app.player.maxHp += 20
                app.player.hp = app.player.maxHp
                startGame(app)
                winStats(app)
            elif event.x > 670 and event.x < 730:
                app.player.bonusDmg += 10
                app.player.hp = app.player.maxHp
                startGame(app)
                winStats(app)
            elif event.x > 790 and event.x < 850:
                app.player.armor += 10
                app.player.hp = app.player.maxHp
                startGame(app)
                winStats(app)

def keyPressed(app, event):
    if event.key == "Left":
        app.player.vx = -1 * app.player.walkSpeed
        app.player.ax = 0
        app.player.movingX = True
        app.player.direction = -1
    elif event.key == "Right":
        app.player.vx = app.player.walkSpeed
        app.player.ax = 0
        app.player.movingX = True
        app.player.direction = 1
    elif event.key == "Up":
        app.player.isJumping = True
        app.player.jump()
    elif event.key == "r":
        appStarted(app)
    elif event.key == "m":
        if app.showMap:
            app.showMap = False
        else:
            app.showMap = True
    elif event.key == "Space":
        app.player.attack(app)
    #switching weapons
    elif event.key == "s":
        app.weaponIndex += 1
        app.weaponIndex %= len(app.loadout)
        app.player.weapon = app.loadout[app.weaponIndex]
    elif event.key == "w":
        app.win = True
    elif event.key == "g":
        app.drawGrid = True

def keyReleased(app, event):
    #if the right or left key is released while on the ground, decelerate.
    if event.key == "Left":
        app.player.ax = app.player.walkSpeed*0.2
    elif event.key == "Right":
        app.player.ax = app.player.walkSpeed*-0.2
    elif event.key == "Up":
        app.player.isFalling = True
        app.player.isJumping = False
    elif event.key == "g":
        app.drawGrid = False

def timerFired(app):
    if app.gameOver:
        return
    elif app.win:
        return
    coeff = 0.01 #allows numbers to stay as integers
    app.player.checkIfHit(app)
    app.player.checkToPickUp(app)
    if app.player.weapon.reload > 0:
        app.player.weapon.reload -= 1
    if app.player.invincible > 0:
        app.player.invincible -= 1
    #player movement
    if app.player.isFalling:
        app.player.vy += app.g
    app.player.moveCharY(app, app.player.vy*coeff)
    app.player.moveCharX(app, app.player.vx*coeff)
    if app.player.vx == 0:
        app.player.movingX = False
        app.player.ax = 0
    app.player.vx += app.player.ax
    app.player.checkIfOffScreenAndUpdateRoom(app)

    #monster movement
    for monster in app.monsters:
        if monster.isFalling:
            monster.vy += app.g
        monster.moveY(app, monster.vy*coeff)
        monster.moveX(app, monster.vx*coeff)

    #projectile movement
    for proj in app.projectiles:
        proj.moveX(app)

    #drops movement
    for drop in app.drops:
        if drop.isFalling:
            drop.vy += app.g
        drop.moveY(app, drop.vy*coeff)

def redrawAll(app, canvas):
    if app.drawGrid:
        drawGrid(app, canvas)
    drawPlatforms(app, canvas)
    drawMonsters(app, canvas)
    drawProjectiles(app, canvas)
    drawDrops(app, canvas)
    drawChar(app, canvas)
    drawUI(app, canvas)
    #drawExplosions(app, canvas)
    if app.gameOver:
        drawGameOver(app, canvas)
    elif app.win:
        drawWin(app, canvas)
    if app.showMap:
        drawMinimap(app, canvas)
    else:
        canvas.create_rectangle(2*app.mapMargin, (app.height - app.mapWidth/2 - 2*app.mapMargin),
                    2*app.mapMargin + app.mapWidth/2,
                    (app.height - 2*app.mapMargin),
                    fill = "black", outline = "red")
        canvas.create_text(app.mapMargin + app.mapWidth/2,
                            app.height - app.mapWidth/2 - app.mapMargin - 25, 
                            text = "Press 'm' to\n    toggle\n  minimap",
                            font = "Arial 10 bold",
                            fill = "white",
                            anchor = "n")
    '''canvas.create_text(app.leftBorder + app.gameWidth/2, app.height/2 - 30, 
        text = f"Room: ({app.currentRoom[0]},{app.currentRoom[1]})",
        font = "Arial 20")'''
    #canvas.create_text(app.leftBorder + app.gameWidth/2, app.height/2, 
    #    text = mazeToString(app.map), 
    #    font = "Arial 10",
    #    anchor = "n")

runApp(width = 1100, height = 800)