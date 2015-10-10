from pico2d import *

def handle_events():
    global running
    global x
    global check
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
                 if event.key == SDLK_RIGHT:
                     check = 0
                 elif event.key == SDLK_LEFT:
                     check = 1
                 elif event.key == SDLK_ESCAPE:
                     running = False
        elif event.type == SDL_KEYUP:
            check = 3



open_canvas()
grass = load_image('MapleMap_image.png')
character = load_image('R_Walk.png')

check = 3
running = True
x = 0
frame = 0
while (running):
    if check == 0:
        x += 10
    elif check == 1:
        x-= 10

    clear_canvas()
    grass.draw(400, 300)
    character.clip_draw(frame * 100, 0, 100, 100, x, 190)
    update_canvas()
    frame = (frame + 1) % 3

    delay(0.05)
    handle_events()

close_canvas()

