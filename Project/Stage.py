from pico2d import *

class Background:
    PIXEL_PER_METER = (10.0 / 0.3)           # 10 pixel 30 cm
    SCROLL_SPEED_KMPH = 10.0                    # Km / Hour
    SCROLL_SPEED_MPM = (SCROLL_SPEED_KMPH * 1000.0 / 60.0)
    SCROLL_SPEED_MPS = (SCROLL_SPEED_MPM / 60.0)
    SCROLL_SPEED_PPS = (SCROLL_SPEED_MPS * PIXEL_PER_METER)
    
    def __init__(self,w,h):
        self.image = load_image('Resource/Map/Background.png')
        self.speed = 0
        self.left = 0
        self.height = 95
        self.screen_width = w
        self.screen_height = h

    def draw(self):
        x = int(self.left)
        w = min(self.image.w - x, self.screen_width)
        self.image.clip_draw_to_origin(x,0,w,self.screen_height,0,0)
        self.image.clip_draw_to_origin(0,0,self.screen_width-w,self.screen_height,w,0)

    def update(self,frame_time):
        self.left = (self.left + frame_time * self.speed) % self.image.w
        
    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_LEFT: self.speed -= Background.SCROLL_SPEED_PPS
            elif event.key == SDLK_RIGHT: self.speed += Background.SCROLL_SPEED_PPS
        if event.type == SDL_KEYUP:
            if event.key == SDLK_LEFT: self.speed += Background.SCROLL_SPEED_PPS
            elif event.key == SDLK_RIGHT: self.speed -= Background.SCROLL_SPEED_PPS        


class Floor:
    def __init__(self):
        self.image = load_image('Resource/Map/Stage1.png')
        self.speed = 0
        self.left = 0
        self.x = 0
        self.canvas_width = get_canvas_width()
        self.canvas_height = get_canvas_height()
        self.w = self.image.w
        self.h = self.image.h
        self.height = 95

    def set_center_object(self, character):
        self.set_center_object = character

    def draw(self):
        self.image.clip_draw_to_origin(self.left,0,self.canvas_width ,self.canvas_height,0,0)

    def update(self,frame_time):
        self.left = clamp(0,int(self.set_center_object.x ) - self.canvas_width//2, self.w - self.canvas_width)

    def draw_bb(self):
        draw_rectangle(*self.get_bb())
        draw_rectangle(*self.get_cc())
        draw_rectangle(*self.get_dd())
        draw_rectangle(*self.get_ee())
        draw_rectangle(*self.get_ff())

    def get_bb(self):
        sx = self.x - self.left
        return sx,0,sx + 2065,165
    def get_cc(self):
        sx = self.x - self.left
        return 2065 + sx,0,sx + 2735,90
    def get_dd(self):
        sx = self.x - self.left
        return 2735 + sx,0,sx + 3220,30
    def get_ee(self):
        sx = self.x - self.left
        return 3220 + sx,0,sx + 3310,90
    def get_ff(self):
        sx = self.x - self.left
        return 3310 + sx,0,sx + 3874,150

    def handle_event(self, event):
        pass

