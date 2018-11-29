#This file was created by Joe Boxberger
#GitHub link: https://github.com/joeboxberger21/FinalProject

#====================SOURCES====================
#goo.gl/2KMivS
#https://python-forum.io/Thread-PyGame-Enemy-AI-and-collision-part-6
#https://www.pygame.org/project-Rect+Collision+Response-1061-.html
#https://www.youtube.com/watch?v=3zV2ewk-IGU
#===============================================

'''
====================RECENTLY ADDED====================
- Random room genration
- Find all doors on the inside of the map and open them (Player in contained in the map, but can move room to room)
- Room detects when player enters (eventually will close doors, then reopen when all enemies are dead)
======================================================

====================BUGS====================
- Room generation bug where rooms are on edges of map
- When player enters room, spawers are created but not drawing or spawning
============================================

====================TODOs====================
- Enemy Colision
- Start adding sprite images
- Enemy collision with player and health system
=============================================
'''

from settings import *
from sprites import *
import pygame as pg
import random

class Game():
    def __init__(self):
        #TODO: init game window
        #TODO: init pygame and show window
        pg.init()
        # init sound mixer
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        
    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.solid_objects = pg.sprite.Group()
        self.all_enemies = pg.sprite.Group()
        self.player = Player(self.solid_objects)
        self.all_sprites.add(self.player, self.player.weapon, self.player.weapon.bullet_group)

        self.camera = Camera(WIDTH, HEIGHT)
        # self.generate_room(-50, -50, 800, 500)
        self.generate_level()
        #Run game, update info, draw based on update, etc
        self.run()

    def run(self):
        self.playing = True
        while self.playing:
            #Keep loop running at our FPS
            self.clock.tick(FPS)
            #Look for events
            self.events()
            #Do things based on the events
            self.update()
            #Show changes and redraw sprites
            self.draw()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

    def update(self):
        #Keep mosue relative to camera/screen, not a single point on map
        self.player.weapon.mx, self.player.weapon.my = pg.mouse.get_pos()
        self.player.weapon.mx -= self.camera.camera.x
        self.player.weapon.my -= self.camera.camera.y
        self.all_sprites.update()
        self.camera.update(self.player)
        #TODO: Fix bug where bullets stop moving after enemy dies

    
    def draw(self):
        self.screen.fill((5, 10, 5))

        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))

        for sprite in self.player.weapon.bullet_group:
            self.screen.blit(sprite.image, self.camera.apply(sprite))

        try:
            for sprite in self.all_enemies:
                self.screen.blit(sprite.image, self.camera.apply(sprite))
        except:
            pass
        
        #TODO: Weapon rotation in weapon class instead of in game class
        # self.screen.blit(self.spawner.enemy.weapon.rotated_image, self.spawner.enemy.weapon.rotated_rect)
        
        pg.draw.circle(self.screen, WHITE, pg.mouse.get_pos(), 8, 1)
        # Make a buffer screen, then make the buffer the main screen (Less lag)
        pg.display.flip()

    def show_start_screen(self):
        pass
    
    def show_game_screen(self):
        pass

    def generate_room(self, x, y, w, h):
        self.new_room = Room(x, y, w, h, self.player)
        print(self.new_room.rect)
        self.solid_objects.add(self.new_room.wall_group)
        self.all_sprites.add(self.new_room.wall_group, self.new_room)
        self.all_rooms.add(self.new_room)

        #One by one check if any of our new doors, collide with anyother door, if they door move both to make a pathway
        for new_door in self.new_room.room_doors:
            for door in self.all_doors:
                if pg.sprite.collide_rect(new_door, door):
                    self.new_room.openable_doors.add(new_door, door)
                    self.new_room.open_doors()
        self.all_doors.add(self.new_room.room_doors)



    def generate_level(self):
        self.all_rooms = pg.sprite.Group()
        self.all_doors = pg.sprite.Group()
        #Room path generator
        level = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0]]
        max_rooms = 15
        current_tile_x, current_tile_y = 4, 4
        current_room = 1

        #TODO: Fix level generation bug where there are rooms away from path
        while current_room <= max_rooms:
            direction = random.randint(1, 4)
            try:
                if direction == 1:
                    if level[current_tile_y - 1][current_tile_x] == 0:
                        current_tile_y -= 1
                        current_room += 1
                if direction == 2:
                    if level[current_tile_y + 1][current_tile_x] == 0:
                        current_tile_y += 1
                        current_room += 1
                if direction == 3:
                    if level[current_tile_y][current_tile_x - 1] == 0:
                        current_tile_x -= 1
                        current_room += 1
                if direction == 4:
                    if level[current_tile_y][current_tile_x + 1] == 0:
                        current_tile_x += 1
                        current_room += 1
                level[current_tile_y][current_tile_x] = 1
            except:
                current_tile_x = 4
                current_tile_y = 4
                continue
        
        current_room_x = 0
        current_room_y = 0
        current_row = 0
        room_width = 1300
        room_height = 800
        for row in level:
            if 1 in row:
                current_row += 1
            current_room_x = 0
            current_room_y += room_height
            for tile in row:
                current_room_x += room_width
                if tile == 1:
                    self.generate_room(current_room_x, current_room_y, room_width, room_height)

        for row in level:
            print(row)




g = Game()
g.show_start_screen()
pg.mouse.set_visible(False)

while g.running:
    g.new()
    g.show_game_screen()

pg.quit()