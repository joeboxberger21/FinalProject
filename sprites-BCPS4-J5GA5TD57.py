#This file was created by Joe Boxberger
#Sprite Classes for game

import pygame as pg
from pygame.sprite import Sprite
import pygame.math
import random, math
from settings import *

#====================SPRITES====================
class Spritesheet():
    def __init__(self, file):
        self.spritesheet = pg.image.load(file).convert()
    def get_image(self, x, y, width, height):
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0,0), (x, y, width, height))
        image = pg.transform.scale(image, (width // 2, height // 2))
        return image

#====================PLAYER USED CLASSES====================

class Player(Sprite):
    def __init__(self, solids, game):
        Sprite.__init__(self)
        self.solids = solids
        self.game = game
        self.width = 55 #35
        self.height = 80 #45
        # self.image = pg.Surface((self.width, self.height))
        self.image = pg.transform.scale(self.game.spritesheet.get_image(725, 318, 240, 313), (60, 80))
        self.rect = self.image.get_rect()
        self.rect.center = (self.width / 2, self.height / 2)
        self.rect.x = 7150
        self.rect.y = 4400
        self.speed = 5
        self.falling = False
        self.weapon = Weapon(self)
        self.invulnerable = False
        self.walking = False
        self.y_direction = 'd'
        self.x_direction = 'r'
        self.dodging = False
        self.health = 9
        self.last_time_hit = 0

        self.forward_right_walk_cycle = [pg.transform.scale(self.game.spritesheet.get_image(312, 5, 240, 313), (60, 80)), pg.transform.scale(self.game.spritesheet.get_image(552, 5, 240, 313), (60, 80))]
        self.forward_left_walk_cycle = []
        for sprite in self.forward_right_walk_cycle:
            self.forward_left_walk_cycle.append(pg.transform.flip(sprite, True, False))
        
        self.back_right_walk_cycle = [pg.transform.scale(self.game.spritesheet.get_image(258, 954, 240, 313), (60, 80)), pg.transform.scale(self.game.spritesheet.get_image(511, 954, 240, 313), (60, 80))]
        self.back_left_walk_cycle = []
        for sprite in self.back_right_walk_cycle:
            self.back_left_walk_cycle.append(pg.transform.flip(sprite, True, False))



        self.current_frame = 0
        self.last_frame = 0

    def update(self):
        self.weapon.update()
        self.animate()
        vx, vy = 0, 0

        if self.health <= 0:
            self.kill()
            self.weapon.kill()
            self.game.game_over()

        if pg.time.get_ticks() - self.last_time_hit >= 5000 and self.invulnerable == True:
            self.invulnerable = False

        if self.invulnerable == False and pg.sprite.spritecollide(self, self.game.all_enemies, False):
            self.health -= 1
            self.invulnerable = True
            print(self.health)
            self.last_time_hit = pg.time.get_ticks()

        m1, m2, m3 = pg.mouse.get_pressed()
        keys = pg.key.get_pressed()

        if keys[pg.K_a]:
            vx = -self.speed
            self.x_direction = 'l'
            self.walking = True
        if keys[pg.K_d]:
            vx = self.speed
            self.x_direction = 'r'
            self.walking = True
        if keys[pg.K_s]:
            vy = self.speed
            self.y_direction = 'd'
            self.walking = True
        if keys[pg.K_w]:
            vy = -self.speed
            self.y_direction = 'u'
            self.walking = True
        if vx != 0 and vy != 0:
            # 1/square root 2 = ~0.7071, use this to lower the vx and vy if moving both at once, this number is found b/c of pythag theorm
            vx *= 0.7071
            vy *= 0.7071

        if not keys[pg.K_w] and not keys[pg.K_a] and not keys[pg.K_s] and  not keys[pg.K_d]:
            self.walking = False
        
        if m3 == 1 and self.dodging == False:
            self.dodge()
        if m3 == 0:
            self.dodging = False
        
        self.move_player(vx, vy)
    
    def animate(self):
        now = pg.time.get_ticks()
        # self.image = self.game.spritesheet.get_image(5, 631, 230, 303)
        if self.walking == False:
            if self.y_direction == 'd':
                if self.x_direction == 'r':
                    self.image = pg.transform.scale(self.game.spritesheet.get_image(725, 318, 240, 313), (60, 80))
                if self.x_direction == 'l':
                    self.image = pg.transform.flip(pg.transform.scale(self.game.spritesheet.get_image(725, 318, 240, 313), (60, 80)), True, False)
        if self.walking:
            if now - self.last_frame >= 100:
                self.current_frame += 1
                self.last_frame = pg.time.get_ticks()
            if self.y_direction == 'd':
                if self.x_direction == 'r':
                    self.image = self.forward_right_walk_cycle[self.current_frame % 2]
                if self.x_direction == 'l':
                    self.image = self.forward_left_walk_cycle[self.current_frame % 2]
            if self.y_direction == 'u':
                if self.x_direction == 'r':
                    self.image = self.back_right_walk_cycle[self.current_frame % 2]
                if self.x_direction == 'l':
                    self.image = self.back_left_walk_cycle[self.current_frame % 2]
        
        self.image.set_colorkey(BLACK)
        # self.game.spritesheet.get_image(5, 631, 230, 303)


    def dodge(self):
        self.invulnerable = True
        self.dodging = True
        if self.direction == 'u':
            self.move_player(0, self.speed * 2)
        self.invulnerable = False
        self.dodging = False
    
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
        self.mx, self.my = 0, 0
        self.player = player

        # self.image = pg.Surface((self.width, self.height)).convert_alpha() 5, 5, 297, 155
        self.image = pg.transform.scale(pg.transform.flip(pg.transform.rotate(self.player.game.spritesheet.get_image(5, 5, 297, 155).convert_alpha(), 90), False, True), (math.floor(155/3.5), math.floor(297/3.5)))
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rotated_image = self.image
        self.original_image = self.image
        self.rect = self.image.get_rect()
        self.pivot_offset = pg.math.Vector2(self.rect.x, self.rect.y)
        self.rotated_rect = self.image.get_rect()
        self.original_rect = self.rect
        self.rect.center = (self.width / 2, self.height / 2)
        self.image_rect = self.image.get_rect(center=self.rect.center)
        self.deg_rotate = 0
        self.bullet_group = pg.sprite.Group()
        self.shooting = False

        self.holding_side = 1
        self.pivot_side = 1
    
    def update(self):
        self.image.set_colorkey(BLACK)

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
            self.image = pg.transform.flip(self.image, True, False)
        
        self.pivot_offset = pg.math.Vector2(0, self.pivot).rotate(-self.deg_rotate)

        self.rotated_image = pg.transform.rotate(self.image, self.deg_rotate).convert_alpha()
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
        self.image = pg.Surface((self.width, self.height)).convert_alpha()
        self.image.fill((250, 50, 250, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (self.width/2, self.height/2)
        
        self.enemy_follow = enemy_follow
        self.enemy_health = enemy_health
        self.enemy_bulletgroup = enemy_bulletgroup

        self.max_enemies = max_enemies
        self.enemies_spawned = 0
        self.enemies_group = pg.sprite.Group()
        self.spawn_interval = 500
        self.last_time = 0

        self.enemy = Enemy(self.enemy_follow, self.enemy_health, self.enemy_bulletgroup)

    def update(self):
        if self.enemies_spawned < self.max_enemies and (pg.time.get_ticks() - self.last_time) >= self.spawn_interval:
            self.spawn()
            self.enemies_spawned += 1
        if self.enemies_spawned == self.max_enemies:
            self.kill()
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

#TODO: Add Enemy Colisions (and better AI?)
class Enemy(Sprite):
    def __init__(self, follow, health, bulletgroup):
        Sprite.__init__(self)
        self.health = health
        self.bulletgroup = bulletgroup
        self.width = 60
        self.height = 80
        self.image = pg.Surface((self.width, self.height))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (self.width / 2, self.height / 2)
        self.x = 0
        self.y = 0
        self.follow = follow
        self.speed = 2
        self.weapon = AI_Weapon(self)
    
    def update(self):
        self.image = pg.transform.scale(self.follow.game.spritesheet.get_image(5, 318, 243, 303), (60, 80)).convert_alpha()
        self.image.set_colorkey(BLACK)
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
    def __init__(self, x, y, w, h, player):
        Sprite.__init__(self)
        print('Room generated')
        self.player = player
        self.wall_group = pg.sprite.Group()
        self.room_doors = pg.sprite.Group()
        self.spawners_group = pg.sprite.Group()
        self.wall_thickness = 20
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.image = pg.Surface((self.width - 119 - self.wall_thickness, self.height - 159 - self.wall_thickness)).convert_alpha()
        self.image.fill((0, 0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (self.width / 2, self.height / 2)
        self.rect.x, self.rect.y = (x + 59 + self.wall_thickness), (y + 79 + self.wall_thickness)
        self.new_spawner = None
        self.player_inside = False
        self.entered = False
        self.doors_are_open = False
        self.enemies_insdie = None
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
        self.room_doors.add(self.wallB_door, self.wallL_door, self.wallR_door, self.wallT_door)

    def update(self):
        #TODO: Check if player in room
        self.player_inside = pg.sprite.collide_rect(self.player, self)
        if self.player_inside and self.entered == False:
            self.entered = True
            for i in range(random.randint(1, 3)):
                self.new_spawner = Enemy_Spawner(random.randint(0, 0), self.player, random.randint(100, 150), self.player.weapon.bullet_group)
                self.new_spawner.rect.x, self.new_spawner.rect.y = (random.randint(self.x + self.wall_thickness, self.x + self.width - self.wall_thickness), random.randint(self.y + self.wall_thickness, self.y + self.height - self.wall_thickness))
                self.spawners_group.add(self.new_spawner)
                print('spawner @: ' + str(self.new_spawner.rect))

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