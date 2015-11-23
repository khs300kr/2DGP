import random
import json
import os
import game_framework
from pico2d import *

from Character import *
from Semiboss_monster import *
from Semiboss_map import *
from Bullet import *

character = None
floor = None
background = None
bullets = None
mushs = None
semiboss = None

def create_world():
    global character, floor, background, bullets, mushs, semiboss
    character = Character()
    mushs = create_mush();
    floor = Floor()
    background = Background(1024,600)
    semiboss = Semi()
    semiboss.set_floor(floor)
    floor.set_center_object(character)
    character.set_floor(floor)
    for mush in mushs:
        mush.set_floor(floor)
    bullets = list()

def destroy_world():
    global character, floor, background,semiboss
    del(character)
    del(floor)
    del(background)
    del(semiboss)


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
            elif (event.type,event.key) == (SDL_KEYDOWN,SDLK_UP):
                if floor.portal_flag == True:
                    pass
                    #game_framework.change_state(title_state)
                else:
                    pass
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
def stagecc_collide(a,b):
    left_a,bottom_a,right_a,top_a = a.get_bb()
    left_b,bottom_b,right_b,top_b = b.get_cc()
    if left_a > right_b : return False
    if right_a < left_b : return False
    if top_a < bottom_b : return False
    if bottom_a > top_b : return False
    return True
def stagedd_collide(a,b):
    left_a,bottom_a,right_a,top_a = a.get_bb()
    left_b,bottom_b,right_b,top_b = b.get_dd()
    if left_a > right_b : return False
    if right_a < left_b : return False
    if top_a < bottom_b : return False
    if bottom_a > top_b : return False
    return True
def portal_collide(a,b):
    left_a,bottom_a,right_a,top_a = a.get_bb()
    left_b,bottom_b,right_b,top_b = b.get_portal()
    if left_a > right_b : return False
    if right_a < left_b : return False
    if top_a < bottom_b : return False
    if bottom_a > top_b : return False
    return True

def update(frame_time):
    background.update(frame_time)
    floor.update(frame_time)
    character.update(frame_time)
    semiboss.update(frame_time)

    if collide(character,floor) and stagecc_collide(character,floor): #b,c
        character.semiboss_doublecollide_b_c()
    elif collide(character,floor): #b
        character.semiboss_collidebb()
    if stagecc_collide(character,floor) and stagedd_collide(character,floor): #c,d
        character.semiboss_doublecollide_c_d()
    elif stagecc_collide(character,floor): #c
        character.semiboss_collidecc()
    elif stagedd_collide(character,floor): #d
        character.semiboss_collidedd()
    for mush in mushs:
        mush.update(frame_time)
        if character.b_death == False:
            if collide(character,mush):
                character.die()
        if mush.life_flag == False:
            mushs.remove(mush)

    for bullet in bullets:
        bullet.update(frame_time)
        for mush in mushs:
            if collide(mush,bullet):
                mush.hurt(character.att)
                if bullets.count(bullet) > 0:   # 0 이하로 떨어질때 지우는거 버그 수정
                    bullets.remove(bullet)
                if mush.hp <= 0:
                    mush.death()

        if bullet.sx >= bullet.canvas_width:
            if bullets.count(bullet) > 0:   # 0 이하로 떨어질때 지우는거 버그 수정
                bullets.remove(bullet)
                print("총알 갯수 = %d" %(bullets.count(bullet)))
        if bullet.x <= 0:
            if bullets.count(bullet) > 0:   # 0 이하로 떨어질때 지우는거 버그 수정
                bullets.remove(bullet)
                print("총알 갯수 = %d" %(bullets.count(bullet)))

    if portal_collide(character,floor):
        floor.check_portal()
    else:
        floor.out_portal()

    delay(0.009)


def draw(frame_time):
    clear_canvas()
    background.draw()
    floor.draw()
    floor.draw_bb()
    character.draw()
    character.draw_bb()
    semiboss.draw()

    for mush in mushs:
        mush.draw()
        mush.draw_bb()

    for bullet in bullets:
        bullet.draw()
        bullet.draw_bb()
    update_canvas()
