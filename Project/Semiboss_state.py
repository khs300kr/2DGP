import random
import json
import os
import temp
import game_framework
import gameover_state
import Final_state
from pico2d import *

from Character import *
from Semiboss_monster import *
from Semiboss_map import *
from Bullet import *
from Time import *
from Item import *

character = None
floor = None
background = None
bullets = None
skills = None
skillcol = False
mushs = None
semiboses = list()
semialive = True
time = None
semi_sound = None
items = list()



def create_world():
    global character, floor, bullets, mushs, semiboses, time, skills, semi_sound, items,background
    # 캐릭터
    character = Character()
    character.life = temp.character_life
    character.skill = temp.character_skill
    #배경
    floor = Floor()
    background = Background(1024,600)
    #준보스
    semiboses.append(Semi())
    for semiboss in semiboses:
        semiboss.set_floor(floor)
    # 스크롤링
    floor.set_center_object(character)
    character.set_floor(floor)
    # 몬스터
    mushs = create_mush();
    for mush in mushs:
        mush.set_floor(floor)
    #총알
    bullets = list()
    #스킬
    skills = list()
    #시간
    time = Time()
    #사운드
    semi_sound = load_music("Resource/Sound/stage_2.mp3")
    semi_sound.set_volume(48)
    semi_sound.repeat_play()
    # item
    items.append(Item())
    for item in items:
        item.set_floor(floor)
def destroy_world():
    global character, floor, time,background
    del(character)
    del(floor)
    del(background)
    del(time)

def shooting():
    global bullets
    bullets.append(Bullet(character.x,character.y,character.state,floor))

def skilling():
    global skills,skillcol
    skills.append(Skill(character.x,character.y,character.state,floor))
    skillcol = True

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
                    temp.character_life = character.life
                    temp.character_skill = character.skill
                    game_framework.change_state(Final_state)
                else:
                    pass
            else:
                character.handle_event(event)
                if character.b_attack == True:
                    shooting()
                if character.skill > 0 :
                    if character.b_skill == True:
                        if skillcol == False:
                            skilling()
                            character.skilldown()
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
def skill1_collide(a,b):
    left_a,bottom_a,right_a,top_a = a.get_bb()
    left_b,bottom_b,right_b,top_b = b.get_skill_1()
    if left_a > right_b : return False
    if right_a < left_b : return False
    if top_a < bottom_b : return False
    if bottom_a > top_b : return False
    return True
def skill2_collide(a,b):
    left_a,bottom_a,right_a,top_a = a.get_bb()
    left_b,bottom_b,right_b,top_b = b.get_skill_2()
    if left_a > right_b : return False
    if right_a < left_b : return False
    if top_a < bottom_b : return False
    if bottom_a > top_b : return False
    return True
def skill3_collide(a,b):
    left_a,bottom_a,right_a,top_a = a.get_bb()
    left_b,bottom_b,right_b,top_b = b.get_skill_3()
    if left_a > right_b : return False
    if right_a < left_b : return False
    if top_a < bottom_b : return False
    if bottom_a > top_b : return False
    return True
def skill4_collide(a,b):
    left_a,bottom_a,right_a,top_a = a.get_bb()
    left_b,bottom_b,right_b,top_b = b.get_skill_4()
    if left_a > right_b : return False
    if right_a < left_b : return False
    if top_a < bottom_b : return False
    if bottom_a > top_b : return False
    return True
def skill5_collide(a,b):
    left_a,bottom_a,right_a,top_a = a.get_bb()
    left_b,bottom_b,right_b,top_b = b.get_skill_5()
    if left_a > right_b : return False
    if right_a < left_b : return False
    if top_a < bottom_b : return False
    if bottom_a > top_b : return False
    return True
def skill6_collide(a,b):
    left_a,bottom_a,right_a,top_a = a.get_bb()
    left_b,bottom_b,right_b,top_b = b.get_skill_6()
    if left_a > right_b : return False
    if right_a < left_b : return False
    if top_a < bottom_b : return False
    if bottom_a > top_b : return False
    return True
def skill7_collide(a,b):
    left_a,bottom_a,right_a,top_a = a.get_bb()
    left_b,bottom_b,right_b,top_b = b.get_skill_7()
    if left_a > right_b : return False
    if right_a < left_b : return False
    if top_a < bottom_b : return False
    if bottom_a > top_b : return False
    return True
def skill8_collide(a,b):
    left_a,bottom_a,right_a,top_a = a.get_bb()
    left_b,bottom_b,right_b,top_b = b.get_skill_8()
    if left_a > right_b : return False
    if right_a < left_b : return False
    if top_a < bottom_b : return False
    if bottom_a > top_b : return False
    return True


def update(frame_time):
    global semialive,skillcol
    background.update(frame_time)
    floor.update(frame_time)
    character.update(frame_time)
    time.update(frame_time)
    # item
    for item in items:
        item.update(frame_time)
        if item.b_die == True:
            if stagecc_collide(character,item):
                items.remove(item)
                item.eat()
                character.skillup()

    # 캐릭터와 맵 충돌.
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

    # 몬스터와 캐릭터 충돌.
    for mush in mushs:
            mush.update(frame_time)
            if character.b_death == False and character.b_respawn == False and mush.b_die == False:
                if collide(character,mush):
                    character.die()
            if mush.life_flag == False:
                mushs.remove(mush)
    # semiboss 캐릭터 충돌
    for semiboss in semiboses:
        semiboss.update(frame_time)
        if character.b_death == False and character.b_respawn == False and semiboss.b_die == False:
            if collide(character,semiboss):
                character.die()
            if semiboss.b_skill == True:
                if semiboss.skill_time >= 0.65:
                    if skill1_collide(character,semiboss):
                        character.die()
                    if skill2_collide(character,semiboss):
                        character.die()
                    if skill3_collide(character,semiboss):
                        character.die()
                    if skill4_collide(character,semiboss):
                        character.die()
            if semiboss.b_skill1 == True:
                if semiboss.skill_time >= 0.65:
                    if skill5_collide(character,semiboss):
                        character.die()
                    if skill6_collide(character,semiboss):
                        character.die()
                    if skill7_collide(character,semiboss):
                        character.die()
                    if skill8_collide(character,semiboss):
                        character.die()
        if semiboss.life_flag == False:
            semiboses.remove(semiboss)
            semialive = False
            floor.portal_open()
            for item in items:
                item.place_item()
        else:
            if int(time.time % 10) == 0:
                semiboss.summonning()
            if int(time.time % 10) == 5:
                semiboss.summonning1()

    # 몬스터와 스킬 충돌
    for skill in skills:
        skill.update(frame_time)
        for mush in mushs:
            if mush.b_die == False:
                if collide(mush,skill):
                    mush.hurt(character.att + 9)
                    skill.hits()
                    if skill.b_hit == False:
                        if skills.count(skill) > 0:   # 0 이하로 떨어질때 지우는거 버그 수정
                            skills.remove(skill)
                    if mush.hp <= 0:
                        mush.death()
    # 준보스와 스킬 충돌
        for semiboss in semiboses:
            if semiboss.b_die == False:
                if collide(semiboss,skill):
                    semiboss.hurt(1)
                    skill.hits()
                    if skill.b_hit == False:
                        if skills.count(skill) > 0:   # 0 이하로 떨어질때 지우는거 버그 수정
                            skills.remove(skill)
                    if semiboss.hp <= 0:
                        semiboss.death()
    # 스킬 사정거리 설정
        if skill.sx >= skill.canvas_width:
            if skills.count(skill) > 0:   # 0 이하로 떨어질때 지우는거 버그 수정
                skills.remove(skill)
                skillcol = False
        if skill.x <= 0:
            if skills.count(skill) > 0:   # 0 이하로 떨어질때 지우는거 버그 수정
                skills.remove(skill)
                skillcol = False
    # 몬스터와 총알 충돌
    for bullet in bullets:
        bullet.update(frame_time)
        for item in items:
            if item.b_die == False:
                if semialive == False:
                    if stagecc_collide(bullet,item):
                        item.hurt(character.att)
                        if bullets.count(bullet) > 0:
                            bullets.remove(bullet)
                            if item.hp <= 0:
                                item.death()
        for mush in mushs:
            if mush.b_die == False:
                if collide(mush,bullet):
                    mush.hurt(character.att)
                    if bullets.count(bullet) > 0:   # 0 이하로 떨어질때 지우는거 버그 수정
                        bullets.remove(bullet)
                    if mush.hp <= 0:
                        mush.death()
    # 준보스와 총알 충돌
        for semiboss in semiboses:
            if semiboss.b_die == False:
                if collide(semiboss,bullet):
                    semiboss.hurt(character.att)
                    if bullets.count(bullet) > 0:   # 0 이하로 떨어질때 지우는거 버그 수정
                        bullets.remove(bullet)
                    if semiboss.hp <= 0:
                        semiboss.death()
    # 총알 화면밖 나갈시 삭제
        if bullet.sx >= bullet.canvas_width:
            if bullets.count(bullet) > 0:   # 0 이하로 떨어질때 지우는거 버그 수정
                bullets.remove(bullet)
        if bullet.x <= 0:
            if bullets.count(bullet) > 0:   # 0 이하로 떨어질때 지우는거 버그 수정
                bullets.remove(bullet)

    if portal_collide(character,floor):
        floor.check_portal()
    else:
        floor.out_portal()

    if character.life < 1:
        game_framework.change_state(gameover_state)

    if semialive == True:
        delay(0.008)
    else:
        delay(0.009)

def draw(frame_time):
    clear_canvas()
    background.draw()
    floor.draw()
    character.draw()
    #character.draw_bb()
    #time.draw()

    for item in items:
        item.draw_semi()

    for semiboss in semiboses:
        semiboss.draw()

    for mush in mushs:
        mush.draw()

    for bullet in bullets:
        bullet.draw()

    for skill in skills:
        skill.draw()
    update_canvas()