#This file was created by Joe Boxberger
#Sprite Classes for game

import pygame as pg
from pygame.sprite import Sprite
import pygame.math
import random, math
from settings import *

#====================PLAYER USED CLASSES====================

class Player(Sprite):
    def __init__(self, solids):
        Sprite.__init__(self)
        #TODO: Player health and collisions with enemies
        self.solids = solids
        self.width = 35
        self.height = 45
        self.image = pg.Surface((self.width, self.height))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (self.width / 2, self.height / 2)
        self.rect.x = 0
        self.rect.y = 0
        self.speed = 5
        self.falling = False
        self.weapon = Weapon(self)
        self.invulnerable = False
        self.direction = 'd'
        self.dodging = False

        # self.mx, self.my = pg.mouse.get_pos()
        # self.mouse_image = pg.Surface((8, 8))
        # self.mouse_image.fill(WHITE)
        # self.mouse_rect = self.mouse_image.get_rect()
        # self.mouse_rect.center = (4, 4)
    
    def update(self):
        self.weapon.update()

        m1, m2, m3 = pg.mouse.get_pressed()
        keys = pg.key.get_pressed()
        # 1/square root 2 = ~0.7071, use this to lower the vx and vy if moving both at once, this number is found b/c of a^2 + b^2 = c^2
        if keys[pg.K_a] and keys[pg.K_w]:
            self.speed *= 0.7071
            self.direction = 'lu'
        if keys[pg.K_a] and keys[pg.K_s]:
            self.speed *= 0.7071
            self.direction = 'ld'
        if keys[pg.K_d] and keys[pg.K_w]:
            self.speed *= 0.7071
            self.direction = 'ru'
        if keys[pg.K_d] and keys[pg.K_s]:
            self.speed *= 0.7071
            self.direction = 'rd'

        if keys[pg.K_a]:
            self.move_player(-self.speed, 0)
            self.direction = 'l'
        if keys[pg.K_d]:
            self.move_player(self.speed, 0)
            self.direction = 'r'
        if keys[pg.K_s]:
            self.move_player(0, self.speed)
            self.direction = 'd'
        if keys[pg.K_w]:
            self.move_player(0, -self.speed)
            self.direction = 'u'

            if m3 == 1 and self.dodging == False:
                self.dodge()
            if m3 == 0:
                self.dodging = False

        self.speed = 5
    
    def dodge(self):
        self.invulnerable = True
        self.dodging = True
        pass
    
    def move_axis(self, dx, dy):
        # Move the rect
        self.rect.x += dx
        self.rect.y += dy

        # If you collide with a wall, set x/y to the edge that you collide with (based on velocity)
        for wall in self.solids:
            if self.rect.colliderect(wall.rect):
                if dx > 0:
                    self.rect.right = wall.rect.left
                if dx < 0:
                    self.rect.left = wall.rect.right
                if dy > 0:
                    self.rect.bottom = wall.rect.top
                if dy < 0:
                    self.rect.top = wall.rect.bottom
        
    def move_player(self, dx, dy):
        # Move each axis separately. Checks for collisions both times.
        if dx != 0:
            self.move_axis(dx, 0)
        if dy != 0:
            self.move_axis(0, dy)
        
class Weapon(Sprite):
    def __init__(self, player):
        Sprite.__init__(self)
        self.damage = 10
        self.width = 15
        self.height = 55
        self.mx, self.my = 0, 0

        self.image = pg.Surface((self.width, self.height)).convert_alpha()
        self.rotated_image = self.image
        self.original_image = self.image

        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.pivot_offset = pg.math.Vector2(self.rect.x, self.rect.y)
        self.rotated_rect = self.image.get_rect()
        self.original_rect = self.rect
        self.rect.center = (self.width / 2, self.height / 2)
        self.player = player
        self.image_rect = self.image.get_rect(center=self.rect.center)
        self.deg_rotate = 0
        self.bullet_group = pg.sprite.Group()
        self.shooting = False

        self.holding_side = 1
        self.pivot_side = 1
    
    def update(self):
        m1, m2, m3 = pg.mouse.get_pressed()
        self.rect = self.original_rect
        self.image = self.original_image
        if self.bullet_group != None:
            self.bullet_group.update()
        
        self.rect.y = self.player.rect.y - (self.height / 2) + (self.player.height / 2)

        self.cent_x, self.cent_y = self.player.rect.x + self.player.width / 2 , self.player.rect.y + self.player.height / 2

        #Pythag Theorm
        side1_length = math.sqrt((self.cent_x - self.mx) **2 + ((self.cent_y + self.player.height / 2) - self.my)**2)
        side2_length = self.player.height / 2
        side3_length = math.sqrt((self.cent_x - self.mx) **2 + (self.cent_y - self.my)**2)
        #Law of cos, and pythag theorm to find angle of mouse
        self.deg_rotate = math.degrees(math.acos(((side2_length **2) + (side3_length **2) - (side1_length **2)) / (2 * side2_length * side3_length)))
        
        if self.mx <= self.player.rect.x + (self.player.width / 2):
            self.deg_rotate *= -1
            self.pivot_side = -1
            self.rect.x = self.player.rect.x - (self.width  / 2) + 10
            self.pivot = self.player.width
        if self.mx >= self.player.rect.x + (self.player.width / 2):
            self.pivot_side = 1
            self.rect.x = self.player.rect.x - (self.width  / 2) + (self.player.width) - 10
            self.pivot = self.player.width
        
        self.pivot_offset = pg.math.Vector2(0, self.pivot).rotate(-self.deg_rotate)

        self.rotated_image = pg.transform.rotate(self.image, self.deg_rotate)
        self.rotated_rect = self.rotated_image.get_rect(center=self.rect.center + self.pivot_offset)

        self.image = self.rotated_image
        self.rect = self.rotated_rect

        if m1 == 0:
            self.shooting = False

        if self.shooting == False and m1 == 1:
                self.shooting = True
                self.shoot()

    def shoot(self):
        self.bullet = Projectile(self, self.rect.center + self.pivot_offset, self.player.solids)
        self.bullet_group.add(self.bullet)

class Projectile(Sprite):
    def __init__(self, weapon, pos, solid_objects):
        Sprite.__init__(self)
        self.weapon = weapon
        self.solid_objects = solid_objects
        self.width = 10
        self.height = 10
        self.image = pg.Surface((self.width, self.height)).convert_alpha()
        self.image.fill((245, 240, 40))
        self.rect = self.image.get_rect(center=pos)
        self.speed = 6
        self.pos = pg.math.Vector2(pos)
        self.vel = pg.math.Vector2(0, self.speed).rotate(-weapon.deg_rotate)
        self.creation_time = pg.time.get_ticks()
        
    def update(self):
        # Add the velocity to the position to move the sprite.
        self.pos += self.vel
        self.rect.center = self.pos  # Update rect to be at position
        wall_collisions = pg.sprite.spritecollide(self, self.solid_objects, False)

        #If nothing collides with bullet, delete it after 10 sec
        if (pg.time.get_ticks() - self.creation_time) > 10000:
            self.kill()
        #Kill projectile if it collides with a wall
        if wall_collisions:
            self.kill()

#====================ENEMY CLASSES====================

class Enemy_Spawner(Sprite):
    def __init__(self, max_enemies, enemy_follow, enemy_health, enemy_bulletgroup):
        Sprite.__init__(self)
        # global enemy_type_glo = enemy_type
        self.width = 14
        self.height = 14
        self.image = pg.Surface((self.width, self.height))
        self.image.fill((250, 50, 250))
        self.rect = self.image.get_rect()
        self.rect.center = (self.width/2, self.height/2)
        
        self.enemy_follow = enemy_follow
        self.enemy_health = enemy_health
        self.enemy_bulletgroup = enemy_bulletgroup

        self.max_enemies = max_enemies
        self.enemies_group = pg.sprite.Group()
        self.spawn_interval = 5000
        self.last_time = 0

        self.enemy = Enemy(self.enemy_follow, self.enemy_health, self.enemy_bulletgroup)

    def update(self):
        if len(self.enemies_group) < self.max_enemies and (pg.time.get_ticks() - self.last_time) >= self.spawn_interval:
            self.spawn()
        if self.enemies_group != None:
            self.enemies_group.update()

    def spawn(self):
        self.enemy = Enemy(self.enemy_follow, self.enemy_health, self.enemy_bulletgroup)
        self.enemies_group.add(self.enemy)
        self.enemy.rect.x = self.rect.x 
        self.enemy.rect.y = self.rect.y
        self.last_time = pg.time.get_ticks()
        print('Enemy Attempting to Spawn!')
        print(self.enemies_group)

#TODO: Redo Enemy to add Colisions (and better AI?)
class Enemy(Sprite):
    def __init__(self, follow, health, bulletgroup):
        Sprite.__init__(self)
        self.health = health
        self.bulletgroup = bulletgroup
        self.width = 35
        self.height = 45
        self.image = pg.Surface((self.width, self.height))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (self.width / 2, self.height / 2)
        self.vx = 0
        self.vy = 0
        self.x = 0
        self.y = 0
        self.follow = follow
        self.speed = 3
        self.stop_distance = 150
        self.weapon = AI_Weapon(self)
    
    def update(self):
        # Delete the object if all health is lost
        if self.health <= 0:
            self.kill()
        #Pythag to find distance from player
        self.c = math.sqrt((self.follow.rect.x - self.rect.x) **2 + (self.follow.rect.y - self.rect.y)**2)

        if self.c != 0:
            #Create a multiplier from the distance between the player 
            self.x = (self.follow.rect.x - self.rect.x) / self.c
            self.y = (self.follow.rect.y - self.rect.y) / self.c

        if self.c <= self.stop_distance:
            self.x = 0
            self.y = 0

        #use multiplier to effect speed
        self.rect.x += self.x * self.speed
        self.rect.y += self.y * self.speed
        
        bullet_collisions = pg.sprite.spritecollide(self, self.bulletgroup, True)
        #If there is bullet from the player colliding with the enemy, it will add it to the group, and if there is anything in this group, remove health
        if bullet_collisions:
            self.health -= self.follow.weapon.damage
        self.weapon.update()

#TODO: Just make this a sub class of Weapon instead of new class
class AI_Weapon(Sprite):
    def __init__(self, user):
        Sprite.__init__(self)
        self.damage = 10
        self.width = 15
        self.height = 55
        self.image = pg.Surface((self.width, self.height)).convert_alpha()
        self.rotated_image = self.image
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.pivot_offset = pg.math.Vector2(self.rect.x, self.rect.y)
        self.rotated_rect = self.image.get_rect()
        # self.rect.center = (self.width / 2, self.height / 2)
        self.user = user
        self.image_rect = self.image.get_rect(center=self.rect.center)
        self.deg_rotate = 0
        self.bullet_group = pg.sprite.Group()
        self.shooting = False

        self.holding_side = 1
        self.pivot_side = 1

        self.last_shot = 0
        self.shot_interval = 2000
    
    def update(self):
        self.mx, self.my = self.user.follow.rect.x, self.user.follow.rect.y
        m1, m2, m3 = pg.mouse.get_pressed()
        if self.bullet_group != None:
            self.bullet_group.update()
        
        self.rect.y = self.user.rect.y - (self.height / 2) + (self.user.height / 2)

        self.cent_x, self.cent_y = self.user.rect.x + self.user.width / 2 , self.user.rect.y + self.user.height / 2

        #Pythag Theorm
        side1_length = math.sqrt((self.cent_x - self.mx) **2 + ((self.cent_y + self.user.height / 2) - self.my)**2)
        side2_length = self.user.height / 2
        side3_length = math.sqrt((self.cent_x - self.mx) **2 + (self.cent_y - self.my)**2)
        #Law of cos, and pythag theorm to find angle of mouse
        self.deg_rotate = math.degrees(math.acos(((side2_length **2) + (side3_length **2) - (side1_length **2)) / (2 * side2_length * side3_length)))
        
        if self.mx <= self.user.rect.x + (self.user.width / 2):
            self.deg_rotate *= -1
            self.pivot_side = -1
            self.rect.x = self.user.rect.x - (self.width  / 2) + 10
            self.pivot = self.user.width
        if self.mx >= self.user.rect.x + (self.user.width / 2):
            self.pivot_side = 1
            self.rect.x = self.user.rect.x - (self.width  / 2) + (self.user.width) - 10
            self.pivot = self.user.width
        
        self.pivot_offset = pg.math.Vector2(0, self.pivot).rotate(-self.deg_rotate)

        self.rotated_image = pg.transform.rotate(self.image, self.deg_rotate)
        self.rotated_rect = self.rotated_image.get_rect(center=self.rect.center + self.pivot_offset)

        if (pg.time.get_ticks() - self.last_shot) > self.shot_interval:
            self.shoot()
            self.last_shot = pg.time.get_ticks()

    def shoot(self):
        # self.bullet = Projectile(self, self.rect.center + self.pivot_offset)
        # self.bullet_group.add(self.bullet)
        pass

#====================MAP CLASSES====================

class Wall(Sprite):
    def __init__(self, x, y, w, h):
        Sprite.__init__(self)
        self.width = w
        self.height = h
        self.image = pg.Surface((self.width, self.height))
        self.image.fill((150, 145, 150))
        self.rect = self.image.get_rect()
        self.rect.center = (self.width / 2, self.height / 2)
        self.rect = self.rect.move(x, y)
    
    def update(self):
        pass

class Room(Sprite):
    def __init__(self, x, y, w, h):
        Sprite.__init__(self)
        print('Room generated')
        self.wall_group = pg.sprite.Group()
        self.wall_thickness = 20
        # width = random.randint(500, 1000)
        # height = random.randint(500, 1000)
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.image = pg.Surface((self.width, self.height)).convert_alpha()
        self.image.fill((0, 0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (self.width / 2, self.height / 2)
        self.rect = self.rect.move(x, y)
        #Top walls
        self.wallT1 = Wall(x, y, (self.width + self.wall_thickness) * (4/9), self.wall_thickness)

        self.wallT_door = Wall(x, y, (self.width + self.wall_thickness) * (1/9), self.wall_thickness)
        self.wallT_door.rect.left = self.wallT1.rect.right

        self.wallT2 = Wall(x, y, (self.width + self.wall_thickness) * (4/9), self.wall_thickness)
        self.wallT2.rect.left = self.wallT_door.rect.right
        #Leftmost walls
        self.wallL1 = Wall(x, y, self.wall_thickness, (self.height + self.wall_thickness) * (4/9))
        
        self.wallL_door = Wall(x, y, self.wall_thickness, (self.height + self.wall_thickness) * (1/9))
        self.wallL_door.rect.top = self.wallL1.rect.bottom

        self.wallL2 = Wall(x, y, self.wall_thickness, (self.height + self.wall_thickness) * (4/9))
        self.wallL2.rect.top = self.wallL_door.rect.bottom
        #Bottom walls
        self.wallB1 = Wall(x, y + self.height, (self.width + self.wall_thickness) * (4/9), self.wall_thickness)
        
        self.wallB_door = Wall(x, y + self.height, (self.width + self.wall_thickness) * (1/9), self.wall_thickness)
        self.wallB_door.rect.left = self.wallB1.rect.right
        
        self.wallB2 = Wall(x, y + self.height, (self.width + self.wall_thickness) * (4/9), self.wall_thickness)
        self.wallB2.rect.left = self.wallB_door.rect.right
        #Rightmost walls
        self.wallR1 = Wall(x + self.width, y, self.wall_thickness, (self.height + self.wall_thickness) * (4/9))
        
        self.wallR_door = Wall(x + self.width, y, self.wall_thickness, (self.height + self.wall_thickness) * (1/9))
        self.wallR_door.rect.top = self.wallR1.rect.bottom

        self.wallR2 = Wall(x + self.width, y, self.wall_thickness, (self.height + self.wall_thickness) * (4/9))
        self.wallR2.rect.top = self.wallR_door.rect.bottom

        self.wall_group.add(self.wallT1, self.wallT_door, self.wallT2, self.wallL1, self.wallL_door, self.wallL2, self.wallB1, self.wallB_door, self.wallB2, self.wallR1, self.wallR_door, self.wallR2)
        # self.wall_group.add(self.wallT1,self.wallL1,self.wallR1,self.wallB1)

    def add_doors(self):
        pass

class Camera(Sprite):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.camera = pg.Rect(0,0, width, height)
    
    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        #Keep target in the middle of the screen, keep camera on target
        x = -target.rect.x + int(WIDTH / 2)
        y = -target.rect.y + int(HEIGHT / 2)
        self.camera = pg.Rect(x, y, self.width, self.height)