from pico2d import *

import game_framework
import title_state
import Semiboss_state
import first_stage
import Character

init = None
name = "gameover_state"
image = None
gameover_sound = None
character_hp = 0


def enter():
    global image,character_hp, gameover_sound
    if image == None:
        image = load_image('Resource/State/gameover.png')
    if init == None:
        character_hp = 0
    gameover_sound = load_music("Resource/Sound/gameover.mp3")
    gameover_sound.set_volume(64)
    gameover_sound.play()




def exit():
    global image
    del(image)


def handle_events(frame_time):
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if(event.type,event.key) == (SDL_KEYDOWN,SDLK_ESCAPE):
                game_framework.quit()
            elif(event.type,event.key) == (SDL_KEYDOWN,SDLK_SPACE):
                game_framework.change_state(title_state)


def draw(frame_time):
    clear_canvas()
    image.draw(512,300)
    update_canvas()


def update(frame_time):
    pass


def pause():
    pass


def resume():
    pass






