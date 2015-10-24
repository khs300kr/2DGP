import random
import json
import os

from pico2d import *

import game_framework
import title_state

name = "MainState"

character = None
tile = None
background = None
bullet = None


class Background:
    def __init__(self):
        self.image = load_image('Resource/Map/mapBack.png')
    def draw(self):
        self.image.draw(1024,300)

class Tile:
    def __init__(self):
        self.image = load_image('Resource/Map/MapleMap_image.png')

    def draw(self):
        self.image.draw(400, 300)


class Character:
    image = None
    jump = None
    attack = None

    R_STAND, R_WALK, L_STAND, L_WALK = 0, 1, 2, 3


    def handle_left_walk(self):
        if self.stand_check == 1:
            self.state = self.L_STAND

    def handle_right_walk(self):
        if self.stand_check == 1:
            self.state = self.R_STAND

    def handle_left_stand(self):
        if self.run_check == 1:
            self.state = self.R_WALK
        elif self.run_check == 2:
            self.state = self.L_WALK

    def handle_right_stand(self):
        if self.run_check == 1:
            self.state = self.R_WALK
        elif self.run_check == 2:
            self.state = self.L_WALK

    handle_state = {
        L_STAND : handle_left_stand,
        L_WALK : handle_left_walk,
        R_STAND : handle_right_stand,
        R_WALK : handle_right_walk
    }

    def __init__(self):
        self.x = 100
        self.y = 195
        self.frame = 0
        self.direction = 3
        self.state = self.R_STAND
        self.speed = 8
        self.run_check = 0
        self.stand_check = 0

        #jump
        self.up_check = 3
        self.j_time = 0
        self.b_jump = False
        self.frame_jump = 0
        #attack
        self.a_time = 0
        self.attack_check = 3
        self.b_attack = False
        self.frame_attack = 0

        if Character.image == None:
            Character.image = load_image('Resource/Character/Moving.png')
        if Character.jump == None:
            Character.jump = load_image('Resource/Character/jump.png')
        if Character.attack == None:
            Character.attack = load_image('Resource/Character/attack.png')

    def update(self):
        if self.direction == 1:
            self.x += (self.speed * self.direction)
        elif self.direction == -1:
            self.x += (self.speed * self.direction)

        if self.b_jump == True:
            self.j_time += 0.5
            self.y -= -15 + (0.98 * self.j_time * self.j_time) / 2
            if self.y <= 195:
                self.j_time = 0
                self.b_jump = False
                self.y = 195
        if self.b_attack == True:
            self.a_time += 0.5
            if self.a_time >= 2:
                self.a_time = 0
                self.b_attack = False

        self.frame = (self.frame + 1) % 4
        self.handle_state[self.state](self)

        delay(0.03)



    def draw(self):
        if self.b_jump == True:
            self.jump.clip_draw(0,self.frame_jump * 100, 100, 100, self.x,self.y)
        elif self.b_attack == True:
            self.attack.clip_draw(0,self.frame_attack * 100 , 100 ,100 ,self.x, self.y)
        else:
            self.image.clip_draw(self.frame * 100, self.state * 125, 100, 100, self.x, self.y)

    def handle_events(self,event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                self.direction = 1
                self.run_check = 1
                self.stand_check = 0
                self.frame_jump = 0
                self.frame_attack = 0
            elif event.key == SDLK_LEFT:
                self.direction = -1
                self.run_check = 2
                self.stand_check = 0
                self.frame_jump = 1
                self.frame_attack = 1
            elif event.key == SDLK_RIGHT and SDLK_LEFT:
                if self.upcheck == 1:
                    self.direction = 1
                    self.run_check = 1
                    self.stand_check = 0
                    self.up_check = 3
                elif self.upcheck == 2:
                    self.direction = -1
                    self.run_check = 2
                    self.stand_check = 0
                    self.up_check = 3
            elif event.key == SDLK_c:
                    self.b_jump = True
            elif event.key == SDLK_x:
                    self.b_attack = True

        if event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                self.run_check = 0
                self.stand_check = 1
                self.up_check = 1
                self.direction = 3
                self.b_attack = False

            elif event.key == SDLK_LEFT:
                self.run_check = 0
                self.stand_check = 1
                self.up_check = 2
                self.direction = 3
                self.b_attack = False



def enter():
    global character, tile, background
    character = Character()
    tile = Tile()
    background = Background()


def exit():
    global character, tile, background
    del(character)
    del(tile)
    del(background)


def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            exit()
        if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            exit()
        else:
             character.handle_events(event)


def update():
    character.update()

def draw():
    clear_canvas()
    background.draw()
    tile.draw()
    character.draw()
    update_canvas()