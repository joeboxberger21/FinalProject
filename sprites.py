#This file was created by Joe Boxberger
#Sprite Classes for game

import pygame as pg
from pygame.sprite import Sprite
import random, math
from settings import *

class Player(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.width = 35
        self.height = 45
        self.image = pg.Surface((self.width, self.height))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (self.width / 2, self.height / 2)
        self.rect.x = WIDTH / 2
        self.rect.y = HEIGHT / 2
        self.vx = 0
        self.vy = 0
        self.speed = 5
        self.falling = False
        self.weapon = Weapon()
        self.weapon.player = self
    
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

class Enemy(Sprite):
    def __init__(self):
        Sprite.__init__(self)
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
        self.follow = None
        self.speed = 3
    
    def update(self):
        #Pythag to find distance from player
        self.c = math.sqrt((self.follow.rect.x - self.rect.x) **2 + (self.follow.rect.y - self.rect.y)**2)

        if self.c != 0:
            #Create a multiplier from the distance between the player 
            self.x = (self.follow.rect.x - self.rect.x) / self.c
            self.y = (self.follow.rect.y - self.rect.y) / self.c

        #use multiplier to effect speed
        self.rect.x += self.x * self.speed
        self.rect.y += self.y * self.speed

class Weapon(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.width = 10
        self.height = 60
        self.image = pg.Surface((self.width, self.height)).convert_alpha()
        self.rotated_image = self.image
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rotated_rect = self.image.get_rect()
        # self.rect.center = (self.width / 2, self.height / 2)
        self.player = None
        self.image_rect = self.image.get_rect(center=self.rect.center)
        self.deg_rotate = 0
    
    def update(self):
        self.mx, self.my = pg.mouse.get_pos()
        m1, m2, m3 = pg.mouse.get_pressed()
        self.rect.x = self.player.rect.x - (self.width  / 2) + (self.player.width / 2)
        self.rect.y = self.player.rect.y - (self.height / 2) + (self.player.height / 2)

        self.cent_x, self.cent_y = self.player.rect.x + self.player.width / 2 , self.player.rect.y + self.player.height / 2

        #Pythag Theorm
        side1_length = math.sqrt((self.cent_x - self.mx) **2 + ((self.cent_y + self.player.height / 2) - self.my)**2)
        side2_length = self.player.height / 2
        side3_length = math.sqrt((self.cent_x - self.mx) **2 + (self.cent_y - self.my)**2)
        #Law of cos, and pythag theorm to find angle of mouse
        self.deg_rotate = math.degrees(math.acos(((side2_length **2) + (side3_length **2) - (side1_length **2)) / (2 * side2_length * side3_length)))
        print(self.deg_rotate)
        if self.mx <= self.player.rect.x + (self.player.width / 2):
            self.deg_rotate *= -1

        pivot_x, pivot_y = self.rect.center
        self.rotated_image = pg.transform.rotate(self.image, self.deg_rotate)
        self.rotated_rect = self.rotated_image.get_rect(center=(pivot_x, pivot_y))

        if m1 == 1:
            self.shoot()
        
        self.rotated_image = pg.transform.rotate(self.image, self.deg_rotate)
        self.rotated_rect = self.rotated_image.get_rect(center=self.rect.center)
  
    def shoot(self):
        self.bullet = Projectile()
        self.bullet.weapon = self


class Projectile(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.width = 5
        self.height = 5
        self.image = pg.Surface((self.width, self.height))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.speed = 5
        self.weapon = None
        
    def update(self):
        self.change_x = math.cos(self.weapon.deg_rotate) * self.speed
        self.change_y = math.sin(self.weapon.deg_rotate) * self.speed

        x = self.weapon.rotated_image.x
        y = self.weapon.rotated_image.y
        self.pos = pg.Vector2D(x,y)
        self.velocity = pg.Vector2D().create_from_angle(self.weapon.deg_rotate, self.speed, return_instance=True)
    def update(self):
        self.pos.add(self.velocity)

class Platform(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.width = 500
        self.height = 20
        self.image = pg.Surface((self.width, self.height))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH / 2
        self.rect.y = HEIGHT - 100
