import game_framework
import Character
import first_stage
from pico2d import *

init = None
character_life = 0
character_skill = 0

def enter():
    global character_life,character_skill
    if init == None:
        character_life = 5
        character_skill = 0


def exit():
    pass


def handle_events():
    pass


def draw():
    pass


def update():
    pass


def pause():
    pass


def resume():
    pass