#This file was created by Joe Boxberger
#GitHub link: https://github.com/joeboxberger21/Demo

#====================SOURCES====================
#goo.gl/2KMivS
#https://python-forum.io/Thread-PyGame-Enemy-AI-and-collision-part-6
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
        self.all_enemies = pg.sprite.Group()
        #Create a player and enemy, and then add them to our sprite group
        self.player = Player()
        self.all_sprites.add(self.player)

        # self.enemy = Enemy(self.player, 100, self.player.weapon.bullet_group)
        # self.all_sprites.add(self.enemy)
        self.spawner = Enemy_Spawner(Enemy(self.player, 100, self.player.weapon.bullet_group), 5)
        self.all_sprites.add(self.spawner)
        self.spawner.rect = (200, 500)
        # Call run
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
        self.all_sprites.update()

    
    def draw(self):
        self.screen.fill((15, 20, 15))
        self.all_sprites.draw(self.screen)
        self.player.weapon.bullet_group.draw(self.screen)
        self.spawner.enemies_group.draw(self.screen)
        self.screen.blit(self.player.weapon.rotated_image, self.player.weapon.rotated_rect)
        pg.draw.circle(self.screen, WHITE, pg.mouse.get_pos(), 8, 1)
        # Make a buffer screen, then make the buffer the main screen (Less lag)
        pg.display.flip()

    def show_start_screen(self):
        pass
    
    def show_game_screen(self):
        pass

g = Game()
g.show_start_screen()
pg.mouse.set_visible(False)

while g.running:
    g.new()
    g.show_game_screen()

pg.quit()