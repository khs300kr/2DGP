import game_framework
import Semiboss_state
import gameover_state
import temp
from Character import *
from Monster import *
from Stage import *
from Bullet import *
from Item import *

character = None
floor = None
background = None
bullets = None
yangs = None
skills = None
skillcol = False
items = list()
bgm_sound = None

def create_world():
    global character, floor, background, bullets , yangs , items, skills,bgm_sound
    character = Character()
    yangs = create_sheep();
    floor = Floor()
    items.append(Item())
    for item in items:
        item.set_floor(floor)
    background = Background(1024,600)
    floor.set_center_object(character)
    character.set_floor(floor)
    for yang in yangs:
        yang.set_floor(floor)
    bullets = list()
    skills = list()
    if bgm_sound == None:
        bgm_sound = load_music("Resource/Sound/stage_1.mp3")
        bgm_sound.set_volume(64)
        bgm_sound.repeat_play()

def destroy_world():
    global character, floor, background
    del(character)
    del(floor)
    del(background)


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
                    game_framework.change_state(Semiboss_state)
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
def stageee_collide(a,b):
    left_a,bottom_a,right_a,top_a = a.get_bb()
    left_b,bottom_b,right_b,top_b = b.get_ee()
    if left_a > right_b : return False
    if right_a < left_b : return False
    if top_a < bottom_b : return False
    if bottom_a > top_b : return False
    return True
def stageff_collide(a,b):
    left_a,bottom_a,right_a,top_a = a.get_bb()
    left_b,bottom_b,right_b,top_b = b.get_ff()
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
    global skillcol
    background.update(frame_time)
    floor.update(frame_time)
    character.update(frame_time)

    if collide(character,floor) and stagecc_collide(character,floor): #b,c
        character.floor_doublecollide_b_c()
    elif collide(character,floor): #b
        character.floor_collidebb()
    if stagecc_collide(character,floor) and stagedd_collide(character,floor): #c,d
        character.floor_doublecollide_c_d()
    elif stagecc_collide(character,floor): #c
        character.floor_collidecc()
    if stagedd_collide(character,floor) and stageee_collide(character,floor): #d,e
        character.floor_doublecollide_d_e()
    elif stagedd_collide(character,floor): #d
        character.floor_collidedd()
    elif stageee_collide(character,floor): #e
        character.floor_collidecc()
    if stageee_collide(character,floor) and stageff_collide(character,floor): #e,f
        character.floor_doublecollide_e_f()
    elif stageff_collide(character,floor): #f
        character.floor_collideff()

    for item in items:
        item.update(frame_time)
        if item.b_die == True:
            if collide(character,item):
                items.remove(item)
                item.eat()
                character.skillup()

    for yang in yangs:
        yang.update(frame_time)
        if character.b_death == False and character.b_respawn == False and yang.b_die == False :
            if collide(character,yang):
                character.die()
        if yang.life_flag == False:
            yangs.remove(yang)

    # 몬스터와 스킬 충돌
    for skill in skills:
        skill.update(frame_time)
        for yang in yangs:
            if yang.b_die == False:
                if collide(yang,skill):
                    yang.hurt(character.att + 9)
                    skill.hits()
                    if skill.b_hit == False:
                        if skills.count(skill) > 0:   # 0 이하로 떨어질때 지우는거 버그 수정
                            skills.remove(skill)
                    if yang.hp <= 0:
                        yang.death()
    # 스킬 사정거리 설정
        if skill.sx >= skill.canvas_width:
            if skills.count(skill) > 0:   # 0 이하로 떨어질때 지우는거 버그 수정
                skills.remove(skill)
                skillcol = False
                print("스킬 갯수 = %d" %(skills.count(skill)))
        if skill.x <= 0:
            if skills.count(skill) > 0:   # 0 이하로 떨어질때 지우는거 버그 수정
                skills.remove(skill)
                skillcol = False
                print("스킬 갯수 = %d" %(skills.count(skill)))
    for bullet in bullets:
        bullet.update(frame_time)
        for item in items:
            if item.b_die == False:
                if collide(item,bullet):
                    item.hurt(character.att)
                    if bullets.count(bullet) > 0:
                        bullets.remove(bullet)
                        if item.hp <= 0:
                            item.death()
        for yang in yangs:
            if yang.b_die == False:
                if collide(yang,bullet):
                    yang.hurt(character.att)
                    if bullets.count(bullet) > 0:   # 0 이하로 떨어질때 지우는거 버그 수정
                        bullets.remove(bullet)
                    if yang.hp <= 0:
                        yang.death()

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

    if character.life < 1:
        game_framework.change_state(gameover_state)

    delay(0.009)


def draw(frame_time):
    clear_canvas()
    background.draw()
    floor.draw()
    #floor.draw_bb()
    character.draw()
    #character.draw_bb()
    for item in items:
        item.draw()
        #item.draw_bb()

    for yang in yangs:
        yang.draw()
        #yang.draw_bb()

    for bullet in bullets:
        bullet.draw()
        #bullet.draw_bb()

    for skill in skills:
        skill.draw()
        #skill.draw_bb()
    update_canvas()

