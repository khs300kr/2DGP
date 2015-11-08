import random
import json
import os
import game_framework
import title_state

from pico2d import *
from Character import Character
from Stage import Floor
from Stage import Background

name = "MainState"

character = None
floor = None
background = None
bullet = None


def create_game():
    global character, floor, background
    character = Character()
    floor = Floor(1024,600)
    background = Background(1024,600)


def destroy_game():
    global character, floor, background
    del(character)
    del(floor)
    del(background)


def enter():
    create_game()


def exit():
    destroy_game()


def pause():
    pass

def resume():
    pass


def handle_events(frame_time):
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            exit()
        else:
            if (event.type,SDL_KEYDOWN) == (event.key,SDLK_ESCAPE):
                exit()
            else:
                character.handle_event(event)
                background.handle_event(event)
                floor.handle_event(event)


def collide(a,b):
    left_a,bottom_a,right_a,top_a = a.get_bb()
    left_b,bottom_b,right_b,top_b = b.get_bb()
    if left_a > right_b : return False
    if right_a < left_b : return False
    if top_a < bottom_b : return False
    if bottom_a > top_b : return False
    return True


def update(frame_time):
    character.update(frame_time)
    background.update(frame_time)
    floor.update(frame_time)

    if collide(character,floor):
        print("collision")


def draw(frame_time):
    clear_canvas()
    background.draw()
    floor.draw()
    floor.draw_bb()
    character.draw_bb()
    character.draw()
    update_canvas()