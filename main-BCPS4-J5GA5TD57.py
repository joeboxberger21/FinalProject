#This file was created by Joe Boxberger
#GitHub link: https://github.com/joeboxberger21/Demo

#====================SOURCES====================
#goo.gl/2KMivS
#https://python-forum.io/Thread-PyGame-Enemy-AI-and-collision-part-6
#https://www.pygame.org/project-Rect+Collision+Response-1061-.html
#https://www.youtube.com/watch?v=3zV2ewk-IGU
#===============================================

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
        self.screen.fill((15, 20, 20))

        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))

        for sprite in self.player.weapon.bullet_group:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        
        for sprite in self.spawner.enemy.weapon.bullet_group:
            self.screen.blit(sprite.image, self.camera.apply(sprite))

        for sprite in self.spawner.enemies_group:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        
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
        new_room = Room(x, y, w, h)
        self.solid_objects.add(new_room.wall_group)
        self.all_sprites.add(new_room.wall_group, new_room)

        spawners_amount = random.randint(1, 3)
        for i in range(spawners_amount):
            enemy_amount = random.randint(2, 5)
            self.spawner = Enemy_Spawner(0, self.player, 100, self.player.weapon.bullet_group)
            self.spawner.rect.x, self.spawner.rect.y = (random.randint(x + new_room.wall_thickness, x + new_room.width - new_room.wall_thickness), random.randint(y + new_room.wall_thickness, y + new_room.height - new_room.wall_thickness))
            print('spawner @: ' + str(self.spawner.rect))
            self.all_sprites.add(self.spawner)
        self.all_rooms.add(new_room)



    def generate_level(self):
        self.all_rooms = pg.sprite.Group()
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

        current_room_x = 0
        current_room_y = 0
        #TODO: Fix level generation bug where there are rooms away from path
        while current_room <= max_rooms:
            direction = random.randint(1, 4)
            try:
                if direction == 1:
                    if level[current_tile_y - 1][current_tile_x] == 0:
                        current_tile_y -= 1
                        current_room += 1
                        current_room_y -= room_height
                        self.generate_room(current_room_x, current_room_y, room_width, room_height, 'd')
                if direction == 2:
                    if level[current_tile_y + 1][current_tile_x] == 0:
                        current_tile_y += 1
                        current_room += 1
                        current_room_y += room_height
                        self.generate_room(current_room_x, current_room_y, room_width, room_height, 'u')
                if direction == 3:
                    if level[current_tile_y][current_tile_x - 1] == 0:
                        current_tile_x -= 1
                        current_room += 1
                        current_room_x -= room_width
                        self.generate_room(current_room_x, current_room_y, room_width, room_height, 'r')
                if direction == 4:
                    if level[current_tile_y][current_tile_x + 1] == 0:
                        current_tile_x += 1
                        current_room += 1
                        current_room_x += room_width
                        self.generate_room(current_room_x, current_room_y, room_width, room_height, 'l')
                level[current_tile_y][current_tile_x] = 1
            except:
                current_tile_x = 4
                current_tile_y = 4
                continue
        
        # current_row = 0
        # for row in level:
        #     room_height = 800
        #     if 1 in row:
        #         current_row += 1
        #     current_room_x = 0
        #     current_room_y += room_height
        #     for tile in row:
        #         room_width = 1300
        #         current_room_x += room_width
        #         if tile == 1:
        #             self.generate_room(current_room_x, current_room_y, room_width, room_height, )

        
        #TODO: Create doorways, and close with enemies
            

        for row in level:
            print(row)




g = Game()
g.show_start_screen()
pg.mouse.set_visible(False)

while g.running:
    g.new()
    g.show_game_screen()

pg.quit()