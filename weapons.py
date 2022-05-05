import math
################################################################################
#########################  WEAPON/PROJECTILE CLASSES  ##########################
################################################################################
class Projectile(object):
    def __init__(self, speed, dmg, direction, xi, yi, size, lifetime, color):
        self.speed = speed
        self.dmg = dmg
        self.di = direction #initial direction
        self.direction = direction
        self.xi = xi
        self.yi = yi
        self.x = xi
        self.y = yi
        self.size = size
        self.color = color
        self.lifetime = lifetime
        self.explodeRadius = 40

    def moveX(self, app):
        #railgun
        if self.speed == 0 and self.lifetime == 3:
            for monster in app.monsters:
                if self.y >= monster.cy - monster.ch and self.y <= monster.cy + monster.ch:
                    if app.player.direction == 1 and monster.cx >= app.player.cx:
                        monster.takeDamage(app, self.dmg)
                    elif app.player.direction == -1 and monster.cx <= app.player.cx:
                        monster.takeDamage(app, self.dmg)
        #normal projectiles
        if self.x - self.speed < app.leftBorder or self.x + self.speed > app.width:
            self.destroy(app)
        else:
            for monster in app.monsters:
                if math.dist((self.x + self.direction*self.speed, self.y), 
                            (monster.cx, monster.cy)) < monster.cw + self.size:
                    if type(app.player.weapon) == BombWeapon:
                        self.explode(app)
                    self.destroy(app)
                    monster.takeDamage(app, self.dmg)
                    break
        
        if self.lifetime == 0:
            self.destroy(app)
        else:
            self.lifetime -= 1

        if self.direction == 1:
            self.x += self.speed
        else:
            self.x -= self.speed

    '''def explode(self, app):
        app.explosions.append((self.x, self.y, self.explodeRadius))
        for monster in app.monsters:
            if ((math.dist((self.x, self.y), (monster.cx, monster.cy))
                <= monster.cw + self.explodeRadius) 
                and (math.dist((self.x, self.y), (monster.cx, monster.cy))
                > monster.cw + self.size)):
                monster.takeDamage(app, self.dmg/2)
        app.explosions.remove((self.x, self.y, self.explodeRadius))'''

    def destroy(self, app):
        app.projectiles.remove(self)

#Each weapon has these stats predefined
class Weapon(object):
    def __init__(self, speed, dmg, reload, color):
        self.speed = speed
        self.dmg = dmg
        self.reloadTime = reload
        self.color = color

class BasicWeapon(Weapon):
    def __init__(self):
        self.speed = 30
        self.dmg = 10
        self.reloadTime = 2
        self.reload = 0
        self.size = 6
        self.color = "yellow"
        self.lifetime = 40
        self.ammo = -1 #infinite
    
    def __repr__(self):
        return "Basic Weapon"

class HeavyWeapon(Weapon):
    def __init__(self):
        self.speed = 15
        self.dmg = 30
        self.reloadTime = 10
        self.reload = 0
        self.size = 10
        self.color = "green"
        self.lifetime = 40
        self.ammo = 50

    def __repr__(self):
        return "Heavy Weapon"

class RailGun(Weapon):
    def __init__(self):
        self.speed = 0
        self.dmg = 50
        self.reloadTime = 40
        self.reload = 0
        self.size = 2
        self.lifetime = 3
        self.color = "lightBlue"
        self.ammo = 20

    def __repr__(self):
        return "Rail Gun"

class BombWeapon(Weapon):
    def __init__(self):
        self.speed = 10
        self.dmg = 40
        self.reloadTime = 10
        self.reload = 0
        self.size = 10
        self.color = "red"
        self.lifetime = 40
        self.ammo = 25
        self.explodeRadius = 40

    def __repr__(self):
        return "Bomb Weapon"