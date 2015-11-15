from pico2d import *

class Background:
    PIXEL_PER_METER = (10.0 / 0.3)           # 10 pixel 30 cm
    SCROLL_SPEED_KMPH = 20.0                    # Km / Hour
    SCROLL_SPEED_MPM = (SCROLL_SPEED_KMPH * 1000.0 / 60.0)
    SCROLL_SPEED_MPS = (SCROLL_SPEED_MPM / 60.0)
    SCROLL_SPEED_PPS = (SCROLL_SPEED_MPS * PIXEL_PER_METER)
    
    def __init__(self,w,h):
        self.image = load_image('Resource/Map/Background.png')
        self.speed = 0
        self.left = 0
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
    SCROLL_SPEED_PPS = 183

    def __init__(self):
        self.image = load_image('Resource/Map/Stage1.png')
        self.speed = 0
        self.left = 0
        self.canvas_width = get_canvas_width()
        self.canvas_height = get_canvas_height()
        self.w = self.image.w
        self.h = self.image.h

    def set_center_object(self, character):
        self.set_center_object = character

    def draw(self):
         # x = int(self.left)
         # w = min(self.image.w - x, self.canvas_width)
         # self.image.clip_draw_to_origin(x,0,1024,self.canvas_height,0,0)
         # self.image.clip_draw_to_origin(0,0,self.canvas_width-1024,self.canvas_height,1024,0)
          self.image.clip_draw_to_origin(self.left,0,self.canvas_width ,self.canvas_height,0,0)

    def update(self,frame_time):
        self.left = clamp(0,int(self.set_center_object.x ) - self.canvas_width//2, self.w - self.canvas_width)

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return 0,0,2047,90
    
    def handle_event(self, event):
        pass
        # if event.type == SDL_KEYDOWN:
        #     if event.key == SDLK_LEFT: self.speed -= Floor.SCROLL_SPEED_PPS
        #     elif event.key == SDLK_RIGHT: self.speed += Floor.SCROLL_SPEED_PPS
        # if event.type == SDL_KEYUP:
        #     if event.key == SDLK_LEFT: self.speed += Floor.SCROLL_SPEED_PPS
        #     elif event.key == SDLK_RIGHT: self.speed -= Floor.SCROLL_SPEED_PPS

