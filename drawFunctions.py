from playerAndMonsters import *
from weapons import *
################################################################################
############################### Draw Functions #################################
################################################################################

def drawChar(app, canvas):
    if app.player.invincible > 0:
        canvas.create_rectangle(app.player.cx - app.player.cw, 
                                app.player.cy - app.player.ch, 
                                app.player.cx + app.player.cw, 
                                app.player.cy + app.player.ch, 
                                fill = app.player.invincibleColor)
    else:
        canvas.create_rectangle(app.player.cx - app.player.cw, 
                                app.player.cy - app.player.ch, 
                                app.player.cx + app.player.cw, 
                                app.player.cy + app.player.ch, 
                                fill = app.player.originalColor)
    size = app.player.weapon.size
    if app.player.direction == 1:
        cx = app.player.cx + app.player.cw
        cy = app.player.cy
        canvas.create_rectangle(cx-5, cy-size, cx+10, cy+size, 
                fill = app.player.weapon.color)
    else:
        cx = app.player.cx - app.player.cw
        cy = app.player.cy
        canvas.create_rectangle(cx-10, cy-size, cx+5, cy+size, 
                fill = app.player.weapon.color)

def drawPlatforms(app, canvas):
    for x1, y1, x2, y2 in app.platforms:
        canvas.create_rectangle(x1, y1, x2, y2, fill = "black")

def drawMonsters(app, canvas):
    for monster in app.monsters:
        x = monster.cx
        y = monster.cy
        canvas.create_rectangle(x - monster.cw, y - monster.ch,
                                x + monster.cw, y + monster.ch, fill = monster.color)

def drawDrops(app, canvas):
    for drop in app.drops:
        x = drop.cx
        y = drop.cy
        if type(drop) == WeaponDrop:
            canvas.create_rectangle(x - 2*drop.cw, y - drop.ch,
                                x + 2*drop.cw, y + drop.cw, fill = drop.color)
        else:
            canvas.create_rectangle(x - drop.cw, y - drop.ch,
                                x + drop.cw, y + drop.cw, fill = drop.color)

def drawFloor(app, canvas):
    canvas.create_rectangle(0, app.height-10, app.width, app.height)

def drawMinimap(app, canvas):
    drawMapGrid(app, canvas)

def drawProjectiles(app, canvas):
    for proj in app.projectiles:
        if proj.speed == 0:
            if proj.di == 1:
                canvas.create_rectangle(proj.xi, proj.yi - proj.size,
                        app.width, proj.yi + proj.size, fill = proj.color, outline = proj.color)
            else:
                canvas.create_rectangle(proj.xi, proj.yi - proj.size,
                        app.leftBorder, proj.yi + proj.size, fill = proj.color, outline = proj.color)
        else:
            canvas.create_oval(proj.x-proj.size, proj.y-proj.size, 
                    proj.x+proj.size, proj.y+proj.size, fill = proj.color)

def drawHpBar(app, canvas, topMargin):
    sideMargin = 20
    hpBarHeight = 20
    maxHp = app.player.maxHp
    currHp = app.player.hp
    hpLength = app.leftBorder - 2*sideMargin
    currHpLength = hpLength * (currHp/maxHp)
    missingHpLength = hpLength - currHpLength
    x1 = sideMargin
    y1 = topMargin + hpBarHeight
    x2 = sideMargin + currHpLength
    y2 = y1 + hpBarHeight
    x3 = x2 + missingHpLength
    canvas.create_rectangle(x1, y1, x2, y2, fill = "green", outline = None)
    canvas.create_rectangle(x2, y1, x3, y2, fill = "red", outline = None)
    midX = sideMargin + (x3-x1)/2
    midY = y1 + (y2-y1)/2
    canvas.create_text(midX, topMargin, text = "Health", font = "Arial 20 bold")
    canvas.create_text(midX, midY, text = f"{currHp}/{maxHp}", font = "Arial 10")

def inventoryCellBounds(app, row, col, topMargin):
    width = app.leftBorder
    height = topMargin
    cellWidth = 60
    cellHeight = 60
    margin = (width - len(app.loadout)*cellWidth)/2
    x0 = margin + col * cellWidth
    x1 = margin + (col+1) * cellWidth
    y0 = topMargin + row * cellHeight
    y1 = topMargin + (row+1) * cellHeight
    return (x0, y0, x1, y1)

def drawInventory(app, canvas, rows, cols, topMargin):
    cellSize = 60
    canvas.create_text(app.leftBorder/2, topMargin, text = "Loadout", font = "Arial 20 bold")
    canvas.create_text(app.leftBorder/2, topMargin + 20, 
        text = "Press 's' to cycle through", font = "Arial 10")
    for row in range(rows):
        for col in range(cols):
            x1, y1, x2, y2 = inventoryCellBounds(app, row, col, topMargin + 40)
            #print(x1, y1, x2, y2)
            if app.weaponIndex == col:
                canvas.create_rectangle(x1+2, y1+2, x2-2, y2-2, fill = "white", 
                    outline = "black", width = 8)
            else:
                canvas.create_rectangle(x1, y1, x2, y2, fill = "white", 
                    outline = "black", width = 3)
            if col < len(app.loadout):
                midX = x1 + (x2-x1)/2
                midY = y1 + (y2-y1)/2
                weaponColor = app.loadout[col].color
                size = app.loadout[col].size
                if type(app.loadout[col]) == RailGun:
                    canvas.create_rectangle(midX-3*size, midY-size, midX+3*size, midY + size,
                        fill = weaponColor)
                elif type(app.loadout[col] == HeavyWeapon):
                    canvas.create_rectangle(midX-size, midY-size, midX+size, midY+size,
                        fill = weaponColor)
                elif type(app.loadout[col] == BombWeapon):
                    canvas.create_rectangle(midX-size, midY-size, midX+size, midY+size,
                        fill = weaponColor)

def drawReload(app, canvas, topMargin):
    sideMargin = 40
    barHeight = 10
    maxReload = app.player.weapon.reloadTime
    currReload = maxReload - app.player.weapon.reload
    barLength = app.leftBorder - 2*sideMargin
    currReloadLength = barLength * (currReload/maxReload)
    missingHpLength = barLength - currReloadLength
    x1 = sideMargin
    y1 = topMargin + barHeight
    x2 = sideMargin + currReloadLength
    y2 = y1 + barHeight
    x3 = x2 + missingHpLength
    canvas.create_rectangle(x1, y1, x2, y2, fill = "yellow")
    if app.player.weapon.ammo == 0:
        canvas.create_rectangle(x1, y1, x1 + barLength, y2, fill = "gray")
    else:
        canvas.create_rectangle(x2, y1, x3, y2, fill = "gray")
    midX = sideMargin + (x3-x1)/2
    #midY = y1 + (y2-y1)/2
    #canvas.create_text(midX, topMargin + 5, text = "Reload", font = "Arial 15")
    if app.player.weapon.reload > 0:
        canvas.create_text(midX, topMargin, text = f"Reloading...", font = "Arial 10")
    else:
        canvas.create_text(midX, topMargin, text = app.player.weapon, font = "Arial 10 bold")
    canvas.create_text(midX, y2 + 5, 
        text = f"Damage: {app.player.weapon.dmg + app.player.bonusDmg}        Speed: {app.player.weapon.speed}        Ammo: {app.player.weapon.ammo}",
        anchor = "n")

def drawUI(app, canvas):
    topMargin = 40
    drawHpBar(app, canvas, topMargin)
    topMargin += 80
    drawInventory(app, canvas, 1, len(app.loadout), topMargin)
    topMargin += 120
    drawReload(app, canvas, topMargin)

def drawGameOver(app, canvas):
    canvas.create_rectangle(app.leftBorder, 0, app.width, app.height, fill = "white")
    cx = app.leftBorder + (app.width-app.leftBorder)/2
    cy = app.height/2 - 100
    canvas.create_text(cx, cy,
            text = "You Died.", font = "Arial 40", anchor = "n", fill = "red")
    cy += 60
    canvas.create_text(cx, cy,
            text = "Select an Upgrade to Restart", font = "Arial 20", anchor = "n", fill = "black")
    cy += 60
    canvas.create_rectangle(cx - 150, cy, cx - 90, cy + 60, fill = "green")
    canvas.create_rectangle(cx - 30, cy, cx + 30, cy + 60, fill = "red")
    canvas.create_rectangle(cx + 90, cy, cx + 150, cy + 60, fill = "gray")
    cy += 80
    canvas.create_text(cx - 120, cy, text = "+10 HP", font = "Arial 10")
    canvas.create_text(cx, cy, text = "+10 DMG", font = "Arial 10")
    canvas.create_text(cx + 120, cy, text = "+5 DEF", font = "Arial 10")

def drawWin(app, canvas):
    canvas.create_rectangle(app.leftBorder, 0, app.width, app.height, fill = "white")
    cx = app.leftBorder + (app.width-app.leftBorder)/2
    cy = app.height/2 - 150
    canvas.create_text(cx, cy,
            text = "You Won!", font = "Arial 40", anchor = "n", fill = "green")
    cy += 60
    canvas.create_text(cx, cy,
            text = "Select an Upgrade to Play Again.\nMonsters will be stronger this time!", 
            font = "Arial 20", anchor = "n", fill = "black")
    cy += 120
    canvas.create_rectangle(cx - 150, cy, cx - 90, cy + 60, fill = "green")
    canvas.create_rectangle(cx - 30, cy, cx + 30, cy + 60, fill = "red")
    canvas.create_rectangle(cx + 90, cy, cx + 150, cy + 60, fill = "gray")
    cy += 80
    canvas.create_text(cx - 120, cy, text = "+20 HP", font = "Arial 10")
    canvas.create_text(cx, cy, text = "+10 DMG", font = "Arial 10")
    canvas.create_text(cx + 120, cy, text = "+10 DEF", font = "Arial 10")

def drawExplosions(app, canvas):
    for explosion in app.explosions:
        cx = explosion[0]
        cy = explosion[1]
        r = explosion[2]
        canvas.create_oval(cx - r, cy - r, cx + r, cy +r, fill = "orange")