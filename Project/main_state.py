import random
import json
import os
import game_framework
import title_state

from pico2d import *
from Character import *
from Monster import *
from Stage import *
from Bullet import *

name = "MainState"

character = None
floor = None
background = None
bullets = None
yangs = None


def create_world():
    global character, floor, background, bullets , yangs
    character = Character(95)
    yangs = create_sheep();
    floor = Floor()
    background = Background(1024,600)

    floor.set_center_object(character)
    character.set_floor(floor)
    for yang in yangs:
        yang.set_floor(floor)
    bullets = list()

def destroy_world():
    global character, floor, background#, sheep
    #del(sheep)
    del(character)
    del(floor)
    del(background)


def shooting():
    global bullets
    bullets.append(Bullet(character.x,character.y,character.state,floor))


def enter():
    create_world()


def exit():
    destroy_world()


def pause():
    pass


def resume():
    pass


def handle_events(frame_time):
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type,event.key) == (SDL_KEYDOWN,SDLK_ESCAPE):
                game_framework.quit()
            else:
                character.handle_event(event)
                if character.b_attack == True:
                    shooting()
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
    #global bullets, yangs

    background.update(frame_time)
    floor.update(frame_time)
    character.update(frame_time)

    for yang in yangs:
        yang.update(frame_time)
        if collide(character,yang):
            character.knockback()
        if yang.life_flag == False:
            yangs.remove(yang)

    for bullet in bullets:
        bullet.update(frame_time)
        for yang in yangs:
            if collide(yang,bullet):
                yang.hurt(character.att)
                if bullets.count(bullet) > 0:   # 0 이하로 떨어질때 지우는거 버그 수정
                    bullets.remove(bullet)
                if yang.hp <= 0:
                    yang.death()


        if bullet.sx >= bullet.canvas_width:
                bullets.remove(bullet)
        elif bullet.x <= 0:
                bullets.remove(bullet)

    delay(0.010)


def draw(frame_time):
    clear_canvas()
    background.draw()
    floor.draw()
    floor.draw_bb()
    character.draw()
    character.draw_bb()

    for yang in yangs:
        yang.draw()
        yang.draw_bb()

    for bullet in bullets:
        bullet.draw()
        bullet.draw_bb()
    update_canvas()

