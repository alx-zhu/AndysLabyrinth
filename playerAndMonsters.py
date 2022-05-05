from roomGenerator import *
from weapons import *
import random

################################################################################
##############################  PLAYER CLASS  ##################################
################################################################################

class Player(object):
    def __init__(self, app):
        #stats
        self.maxHp = 100
        self.hp = 100
        self.armor = 0
        self.bonusDmg = 0
        self.walkSpeed = 1000
        self.invincible = 0 #2 seconds invincibility
        #40 is 2 seconds invincibility
        #colors
        self.invincibleColor = "gray"
        self.originalColor = "black"
        self.color = self.originalColor
        #items/weapons
        self.weapon = BasicWeapon()
        #starting position
        self.cw = 20
        self.ch = 20
        self.cx = self.cw + self.cw
        self.cy = app.height - self.ch
        #velocity
        self.vy = 0
        self.vx = 0
        self.direction = 1
        #gravity
        self.g = 250
        #jump
        self.jumpAccel = -2500
        #acceleration
        self.ax = 0
        self.ay = 0
        #bools and other checks
        self.jumps = 2
        self.isJumping = False
        self.isFalling = False
    
    def aboveOrBelow(self, x1, x2, leftEdge, rightEdge):
        if leftEdge < x2 and rightEdge > x1:
            return True
        return False

    def moveCharY(self, app, dy):
        leftEdge = self.cx - self.cw
        rightEdge = self.cx + self.cw
        bottomEdge = self.cy + self.ch
        topEdge = self.cy - self.ch
        #for debugging falling
        for x1, y1, x2, y2 in app.platforms:
            if ((bottomEdge + dy > y1) and (topEdge < y1) and 
                    self.aboveOrBelow(x1, x2, leftEdge, rightEdge)):
                self.jumps = 2
                self.cy = y1 - self.ch
                self.isFalling = False
                self.vy = 0
                return
            #if below a platform and topEdge will go through, collide
            if((topEdge + dy < y2) and (bottomEdge > y2) and
                self.aboveOrBelow(x1, x2, leftEdge, rightEdge)):
                #if you hit the bottom of a platform stop moving, and fall.
                #set dy to 0 so the position does not update.
                self.cy = y2 + self.ch
                self.vy = 0
                dy = 0
                self.isFalling = True
        if self.isFalling or self.isJumping:
            self.cy += dy
        else:
            self.isFalling = True
            #print("I am Falling")
        #print(f"Jumping: {app.isJumping}, Falling: {app.isFalling}")

    def nextTo(self, y1, y2, topEdge, bottomEdge):
        #if (y1 > topEdge and y1 < bottomEdge) or (y2 < bottomEdge and y2 > topEdge):
        if (((topEdge < y2 and topEdge > y1) or 
            (bottomEdge > y1 and bottomEdge < y2)) or
            ((y1 > topEdge and y1 < bottomEdge) or 
            (y2 < bottomEdge and y2 > topEdge))):
            return True
        return False 

    def moveCharX(self, app, dx):
        leftEdge = self.cx - self.cw
        rightEdge = self.cx + self.cw
        bottomEdge = self.cy + self.ch
        topEdge = self.cy - self.ch
        for x1, y1, x2, y2 in app.platforms:
            #print(nextToPlatform(y1, y2, topEdge, bottomEdge))
            if (self.nextTo(y1, y2, topEdge, bottomEdge) and 
                ((rightEdge + dx >= x1 and leftEdge < x1) or 
                (leftEdge + dx <= x2 and rightEdge > x2))):
                #if on the left of a platform, stop right when the right side
                #touches, and vice versa
                if rightEdge <= x1:
                    self.cx = x1 - self.cw
                elif leftEdge >= x2:
                    self.cx = x2 + self.cw
                self.vx = 0
                dx = 0
                self.ax = 0
        self.cx += dx
        #if canMove: self.cx += dx

    def jump(self):
        if self.jumps > 0:
            self.vy = self.jumpAccel
            self.jumps -= 1

    #makes the walls for open doors
    def openDoors(self, app, roomRow, roomCol):
        directions = [(0, -1), (0, 1), (1, 0), (-1, 0)]
        left = right = up = down = False
        for d in directions:
            drow, dcol = d
            row = roomRow + drow
            col = roomCol + dcol
            #tells which directions there are more rooms
            if isLegal(app, row, col):
                if drow == -1:
                    up = True
                elif drow == 1:
                    down = True
                elif dcol == -1:
                    left = True
                elif dcol == 1:
                    right = True
        #make the walls and floors
        app.platforms = getWallsAndFloors(app, left, right, up, down)

    #adds the platforms for the corresponding layout of the current room
    def createLayout(self, app):
        #rooms will have randomized layouts generated by the maze initially
        layout = app.layouts[app.map[app.currentRoom[0]][app.currentRoom[1]]]
        #converts row cols into coordinates and combines long platforms
        combinedPlatforms = combinePlatforms(app, layout)
        #make the platforms
        app.platforms.extend(combinedPlatforms)

    #makes the room with openings based on the rooms around them
    def loadRoom(self, app, roomRow, roomCol):
        app.drops = []
        app.projectiles = []
        #make the walls and floors
        if app.visited[app.currentRoom] == 0:
            self.openDoors(app, roomRow, roomCol)
        else:
            app.platforms = getWallsAndFloors(app, False, False, False, False)
        self.createLayout(app)
        #spawn one monster for every 3 platforms (grid spaces, not combined)
        app.monsters = []
        #add current room to app.visited
        numMonsters = app.visited.get(app.currentRoom, random.randint(3, 10))
        #add surrounding rooms to app.visited, to reveal them
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        currRow = app.currentRoom[0]
        currCol = app.currentRoom[1]
        for drow, dcol in directions:
            newRow = currRow + drow
            newCol = currCol + dcol
            if (newRow > 0 and newRow < len(app.map) and
                newCol > 0 and newCol < len(app.map[0]) and
                app.map[newRow][newCol] != "w"):
                app.visited[(newRow,newCol)] = app.visited.get((newRow, newCol), random.randint(3, 10))
        
        layout = app.layouts[app.map[app.currentRoom[0]][app.currentRoom[1]]]
        if numMonsters > 0:
            while len(app.monsters) < numMonsters:
                index = random.randint(0, len(layout)-1)
                row, col = layout[index]
                #Prevents them from spawning in doorways
                if (row == 1 or (row, col) == (5, 0) or (row, col) == (5, 1)
                    or (row, col) == (5, 8) or (row, col) == (5, 9)):
                    continue
                app.monsters.append(spawnMonster(app, row, col))
        if len(app.loadout) < 4:
            app.bombDropped = False
        if len(app.loadout) < 3:
            app.railDropped = False
        if len(app.loadout) < 2:
            app.heavyDropped = False

    def checkIfOffScreenAndUpdateRoom(self, app):
        roomRow, roomCol = app.currentRoom
        if (roomRow, roomCol) not in app.visited:
            #assign a random number of monsters to each room
            app.visited[app.currentRoom] = random.randint(5, 10)
        if self.cx < app.leftBorder:
            roomRow, roomCol = app.currentRoom
            roomCol -= 1
            app.currentRoom = (roomRow, roomCol)
            #update position
            self.cx = app.width - self.cw - 10
            self.loadRoom(app, roomRow, roomCol)
        elif self.cx > app.width:
            roomCol += 1
            app.currentRoom = (roomRow, roomCol)
            #update position
            self.cx = app.leftBorder + self.cw + 10
            #load new room
            self.loadRoom(app, roomRow, roomCol)
        elif self.cy < 0:
            roomRow -= 1
            app.currentRoom = (roomRow, roomCol)
            #update position
            self.cy = app.height - self.cw - 10
            self.loadRoom(app, roomRow, roomCol)
        elif self.cy > app.height:
            roomRow += 1
            app.currentRoom = (roomRow, roomCol)
            #update position
            self.cy = self.cw + 10
            self.loadRoom(app, roomRow, roomCol)
    
    def checkIfHit(self, app):
        if self.invincible > 0:
            return
        for monster in app.monsters:
            mw = monster.cw
            mh = monster.ch
            if ((abs(self.cy - monster.cy) <= self.ch + mh) and 
                (abs(self.cx - monster.cx) <= self.cw + mw)):    
                self.takeDamage(app, monster.dmg)
                self.invincible = 10
                break
    
    def checkToPickUp(self, app):
        for drop in app.drops:
            dw = drop.cw
            dh = drop.ch
            if ((abs(self.cy - drop.cy) <= self.ch + dh) and 
                (abs(self.cx - drop.cx) <= self.cw + dw)):    
                if type(drop) == HealthDrop and self.hp < self.maxHp:
                    self.hp += drop.hp
                    if self.hp > self.maxHp:
                        self.hp = self.maxHp
                elif type(drop) == AmmoDrop:
                    if self.weapon.ammo != -1:
                        self.weapon.ammo += drop.ammo
                elif type(drop) == WeaponDrop:
                    if drop.weaponType == "HeavyWeapon":
                        if len(app.loadout) < 2:
                            app.loadout.append(HeavyWeapon())
                    elif drop.weaponType == "RailGun":
                        if len(app.loadout) < 3:
                            app.loadout.append(RailGun())
                    elif drop.weaponType == "BombWeapon":
                        if len(app.loadout) < 4:
                            app.loadout.append(BombWeapon())
                app.drops.remove(drop)

    def attack(self, app):
        if self.invincible > 0:
            return
        if self.weapon.reload == 0 and (self.weapon.ammo > 0 or self.weapon.ammo == -1):
            #fire a projectile at the character's height
            speed = self.weapon.speed
            dmg = self.weapon.dmg + self.bonusDmg
            size = self.weapon.size
            color = self.weapon.color
            cx = self.cx + self.direction*self.cw
            app.projectiles.append(Projectile(speed, dmg, self.direction, 
                                cx, self.cy, size, self.weapon.lifetime, color))
            self.weapon.reload = self.weapon.reloadTime
            if self.weapon.ammo != -1:
                self.weapon.ammo -= 1
        
    def takeDamage(self, app, dmg):
        dmgPercent = 1 - self.armor/100
        self.hp -= int(dmg * dmgPercent)
        if self.hp <= 0:
            self.hp = 0
            app.gameOver = True

################################################################################
################################  DROP CLASS  ##################################
################################################################################

class Drop(object):
    def __init__(self, app, cx, cy):
        self.cx = cx
        self.cy = cy
        self.cw = 10
        self.ch = 10
        self.isFalling = True
        self.vy = 0

    def aboveOrBelowPlatform(self, x1, x2, leftEdge, rightEdge):
        if leftEdge < x2 and rightEdge > x1:
            return True
        return False

    def moveY(self, app, dy):
        leftEdge = self.cx - self.cw
        rightEdge = self.cx + self.cw
        bottomEdge = self.cy + self.ch
        topEdge = self.cy - self.ch
        for x1, y1, x2, y2 in app.platforms:
            if ((bottomEdge + dy > y1) and (topEdge < y1) and 
                    self.aboveOrBelowPlatform(x1, x2, leftEdge, rightEdge)):
                self.cy = y1 - self.ch
                self.isFalling = False
                self.vy = 0
                return
        if self.isFalling:
            self.cy += dy
        else:
            self.isFalling = True

class HealthDrop(Drop):
    def __init__(self, app, hp, cx, cy):
        super().__init__(app, cx, cy)
        self.hp = hp
        self.color = "lightGreen"
    
class AmmoDrop(Drop):
    def __init__(self, app, ammo, cx, cy):
        super().__init__(app, cx, cy)
        self.ammo = ammo
        self.color = "lightYellow"
    
class WeaponDrop(Drop):
    def __init__(self, app, weaponType, cx, cy):
        super().__init__(app, cx, cy)
        self.weaponType = weaponType
        if weaponType == "HeavyWeapon":
            self.color = "green"
        elif weaponType == "RailGun":
            self.color = "lightBlue"
        elif weaponType == "BombWeapon":
            self.color = "red"
        
def spawnRandomDrop(app, hp, ammo, cx, cy):
    probability = random.randint(0, 100)
    if len(app.visited) > 2 and len(app.loadout) < 2 and app.heavyDropped == False:
        app.heavyDropped = True
        return WeaponDrop(app, "HeavyWeapon", cx, cy)
    elif len(app.visited) > 4 and len(app.loadout) < 3 and app.railDropped == False:
        app.railDropped = True
        return WeaponDrop(app, "RailGun", cx, cy)
    #elif len(app.visited) > 6 and len(app.loadout) < 4 and app.bombDropped == False:
    #    app.bombDropped = True
    #    return WeaponDrop(app, "BombWeapon", cx, cy)
    if probability%3 == 0:
        return AmmoDrop(app, ammo, cx, cy) 
    else:
        return HealthDrop(app, hp, cx, cy)


################################################################################
###############################  MONSTER CLASS  ################################
################################################################################

class Monster(object):
    def __init__(self, app, hp, dmg, cx, cy):
        self.hp = hp
        self.dmg = dmg
        #starting position
        self.size = 20
        self.ch = self.size
        self.cw = self.size
        self.cx = cx
        self.cy = cy - 4*self.ch
        #velocity
        self.vy = 0
        self.vx = int(600*random.random())
        #x-component of unit vector
        randDir = [-1, 1]
        self.direction = randDir[random.randint(0, 1)]
        #gravity
        self.g = 250
        #bools and other checks
        self.isJumping = False
        self.isFalling = False
        self.isTakingDmg = False
        self.dmgColor = "darkRed"
        self.originalColor = "red"
        self.color = self.originalColor

    def aboveOrBelowPlatform(self, x1, x2, leftEdge, rightEdge):
        if leftEdge < x2 and rightEdge > x1:
            return True
        return False

    def moveY(self, app, dy):
        if self.color == self.dmgColor:
            self.color = self.originalColor
        leftEdge = self.cx - self.cw
        rightEdge = self.cx + self.cw
        bottomEdge = self.cy + self.ch
        topEdge = self.cy - self.ch
        for x1, y1, x2, y2 in app.platforms:
            if ((bottomEdge + dy > y1) and (topEdge < y1) and 
                    self.aboveOrBelowPlatform(x1, x2, leftEdge, rightEdge)):
                self.cy = y1 - self.ch
                self.isFalling = False
                self.vy = 0
                return
        if self.isFalling:
            self.cy += dy
        else:
            self.isFalling = True

    def nextToPlatform(self, y1, y2, topEdge, bottomEdge):
        #if (y1 > topEdge and y1 < bottomEdge) or (y2 < bottomEdge and y2 > topEdge):
        if (((topEdge < y2 and topEdge > y1) or 
            (bottomEdge > y1 and bottomEdge < y2)) or
            ((y1 > topEdge and y1 < bottomEdge) or 
            (y2 < bottomEdge and y2 > topEdge))):
            return True
        return False 

    def moveX(self, app, dx):
        leftEdge = self.cx - self.cw
        rightEdge = self.cx + self.cw
        bottomEdge = self.cy + self.ch
        topEdge = self.cy - self.ch
        for x1, y1, x2, y2 in app.platforms:
            if (bottomEdge >= y1 and topEdge < y1 and 
                self.aboveOrBelowPlatform(x1, x2, leftEdge, rightEdge)):
                if rightEdge > x2:
                    self.direction = -1
                elif leftEdge < x1:
                    self.direction = 1
            if (self.nextToPlatform(y1, y2, topEdge, bottomEdge) and 
                ((rightEdge + dx >= x1 and leftEdge < x1) or 
                (leftEdge - dx <= x2 and rightEdge > x2))):
                #print(f"TOUCHING A PLATFORM, leftEdge = {leftEdge}, x2 = {x2}")
                #if on the left of a platform, stop right when the right side
                #touches, and vice versa
                if rightEdge <= x1:
                    self.cx = x1 - self.cw - 5
                    self.direction = -1
                    #print("here")
                if leftEdge >= x2:
                    self.cx = x2 + self.cw + 5
                    self.direction = 1
                #self.vx = 0

        if self.direction == 1:
            self.cx += dx
        elif self.direction == -1:
            self.cx -= dx

    def takeDamage(self, app, dmg):
        self.hp -= dmg
        #for color change
        self.color = self.dmgColor
        if self.hp <= 0:
            chance = random.randint(0, 100)
            if chance <= 40:
                drop = spawnRandomDrop(app, 20, 5, self.cx, self.cy-10)
                app.drops.append(drop)
            #print(app.drops)
            app.monsters.remove(self)
            app.visited[app.currentRoom] = len(app.monsters)
            #print(app.visited[app.currentRoom])
            if app.visited[app.currentRoom] == 0:
                app.player.openDoors(app, app.currentRoom[0], app.currentRoom[1])
                app.player.createLayout(app)
                if checkIfGameOver(app):
                    app.win = True

class BasicMonster(Monster):
    def __init__(self, app, hp, dmg, cx, cy):
        super().__init__(app, hp, dmg, cx, cy)
        self.dmgColor = "darkRed"
        self.originalColor = "red"
        self.color = self.originalColor
        self.size = 20
        self.ch = self.size
        self.cw = self.size
        self.hp = hp

class BigMonster(Monster):
    def __init__(self, app, hp, dmg, cx, cy):
        super().__init__(app, hp, dmg, cx, cy)
        self.dmgColor = "darkGreen"
        self.originalColor = "green"
        self.color = self.originalColor
        self.size = 22
        self.ch = self.size
        self.cw = self.size
        self.vx = int(300*random.random())


#outside of class
def spawnMonster(app, row, col):
        x1, y1, x2, y2 = getCellBounds(app, row, col)
        #place a monster at center of platform
        cx = x1 + (x2-x1)/2
        cy = y2
        randChance = random.randint(1, 100)
        if randChance <= 25:
            return BigMonster(app, app.monsterHp*2, app.monsterDmg*1.5, cx, cy)
        else:
            return BasicMonster(app, app.monsterHp, app.monsterDmg, cx, cy)

def checkIfGameOver(app):
    for room in app.visited:
        if app.visited[room] != 0:
            return False
    else:
        return True
