#This file was created by Joe Boxberger
#Sprite Classes for game

import pygame as pg
from pygame.sprite import Sprite
import pygame.math
import random, math
from settings import *

class Player(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.width = 35
        self.height = 45
        self.image = pg.Surface((self.width, self.height))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (self.width / 2, self.height / 2)
        self.rect.x = WIDTH / 2
        self.rect.y = HEIGHT / 2
        self.vx = 0
        self.vy = 0
        self.speed = 5
        self.falling = False
        self.weapon = Weapon(self)
    
    def update(self):
        self.weapon.update()
        self.vx = 0
        self.vy = 0
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.vx = -self.speed
        if keys[pg.K_d]:
            self.vx = self.speed
        if keys[pg.K_s]:
            self.vy = self.speed
        if keys[pg.K_w]:
            self.vy = -self.speed
        if self.vx != 0 and self.vy != 0:
            # 1/square root 2 = ~0.7071, use this to lower the vx and vy if moving both at once, this number is found b/c of a^2 + b^2 = c^2
            self.vx *= 0.7071
            self.vy *= 0.7071

        self.rect.x += self.vx
        self.rect.y += self.vy

class Enemy_Spawner(Sprite):
    def __init__(self, enemy_type, max_enemies):
        Sprite.__init__(self)
        # global enemy_type_glo = enemy_type
        self.image = pg.Surface((15, 15))
        self.image.fill((250, 250, 50))
        self.rect = self.image.get_rect()
        self.enemy_type = enemy_type
        self.max_enemies = max_enemies
        self.enemies_group = pg.sprite.Group()
        self.spawn_interval = 1000
        self.last_time = 0

    def update(self):
        if len(self.enemies_group) < self.max_enemies and (pg.time.get_ticks() - self.last_time) >= self.spawn_interval:
            self.spawn()
        if self.enemies_group != None:
            self.enemies_group.update()

    def spawn(self):
        self.enemy = self.enemy_type
        self.enemies_group.add(self.enemy)
        self.last_time = pg.time.get_ticks()
        print('Enemy Attempting to Spawn!')
        print(self.enemies_group)

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
        self.rect.x = 0
        self.rect.y = 0
        self.x = 0
        self.y = 0
        self.follow = follow
        self.speed = 3
    
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

        #use multiplier to effect speed
        self.rect.x += self.x * self.speed
        self.rect.y += self.y * self.speed

        bullet_collisions = pg.sprite.spritecollide(self, self.bulletgroup, True)
        #If there is bullet from the player colliding with the enemy, it will add it to the group, and if there is anything in this group, remove health
        if bullet_collisions:
            self.health -= self.follow.weapon.damage
            

class Weapon(Sprite):
    def __init__(self, player):
        Sprite.__init__(self)
        self.damage = 10
        self.width = 10
        self.height = 60
        self.image = pg.Surface((self.width, self.height)).convert_alpha()
        self.rotated_image = self.image
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rotated_rect = self.image.get_rect()
        # self.rect.center = (self.width / 2, self.height / 2)
        self.player = player
        self.image_rect = self.image.get_rect(center=self.rect.center)
        self.deg_rotate = 0
        self.bullet_group = pg.sprite.Group()
        self.shooting = False
    
    def update(self):
        self.mx, self.my = pg.mouse.get_pos()
        m1, m2, m3 = pg.mouse.get_pressed()
        if self.bullet_group != None:
            self.bullet_group.update()
        
        self.rect.x = self.player.rect.x - (self.width  / 2) + (self.player.width / 2)
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
        self.rotated_image = pg.transform.rotate(self.image, self.deg_rotate)
        self.rotated_rect = self.rotated_image.get_rect(center=self.rect.center)

        if m1 == 0:
            self.shooting = False

        if self.shooting == False and m1 == 1:
                self.shooting = True
                self.shoot()

    def shoot(self):
        self.bullet = Projectile(self, self.rect.center)
        self.bullet_group.add(self.bullet)


class Projectile(Sprite):
    def __init__(self, weapon, pos):
        Sprite.__init__(self)
        self.weapon = weapon
        self.width = 10
        self.height = 10
        self.image = pg.Surface((self.width, self.height)).convert_alpha()
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=pos)
        self.speed = 6
        self.pos = pg.math.Vector2(pos)
        self.vel = pg.math.Vector2(0, self.speed).rotate(-weapon.deg_rotate)
        self.creation_time = pg.time.get_ticks()
        
    def update(self):
        # Add the velocity to the pos to move the sprite.
        self.pos += self.vel
        self.rect.center = self.pos  # Update the rect as well.

        #If nothing collides with bullet, delete it after 10 sec
        if (pg.time.get_ticks() - self.creation_time) > 10000:
            self.kill()
        
class Wall(Sprite):
    def __init__(self, x, y, w, h):
        Sprite.__init__(self)
        self.width = 500
        self.height = 20
        self.image = pg.Surface((self.width, self.height))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH / 2
        self.rect.y = HEIGHT - 100
