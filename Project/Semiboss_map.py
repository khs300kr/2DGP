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
    TIME_PER_ACTION = 0.8
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 5

    image = None
    portal = None

    def __init__(self):
        if Floor.image == None:
            self.image = load_image('Resource/Map/Semiboss.png')
        if Floor.portal == None:
            self.portal = load_image("Resource/Map/portal.png")
        self.speed = 0
        self.left = 0
        self.x = 0
        self.total_frames = 0.0
        self.frame = 0
        self.canvas_width = get_canvas_width()
        self.canvas_height = get_canvas_height()
        self.w = self.image.w
        self.h = self.image.h
        self.height = 95
        self.portal_flag = False
        self.bsemi = True

    def set_center_object(self, character):
        self.set_center_object = character

    def draw(self):
        sx = self.x - self.left
        self.image.clip_draw_to_origin(self.left,0,self.canvas_width ,self.canvas_height,0,0)
        if self.bsemi == False:
            self.portal.clip_draw(self.frame * 125,0,125,75,sx + 1385,205)

    def update(self,frame_time):
        self.total_frames += Floor.FRAMES_PER_ACTION * Floor.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 5
        self.left = clamp(0,int(self.set_center_object.x ) - self.canvas_width//2, self.w - self.canvas_width)

    def draw_bb(self):
        draw_rectangle(*self.get_bb())
        draw_rectangle(*self.get_cc())
        draw_rectangle(*self.get_dd())
        if self.bsemi == False:
            draw_rectangle(*self.get_portal())

    def get_bb(self):
        sx = self.x - self.left
        return sx,0,sx + 510,50
    def get_cc(self):
        sx = self.x - self.left
        return 510 + sx,0,sx + 600,110
    def get_dd(self):
        sx = self.x - self.left
        return 600 + sx,0,sx + 1500,170
    def get_portal(self):
        sx = self.x - self.left
        return 1355 + sx,180, 1410 + sx , 205

    def handle_event(self, event):
        pass

    def check_portal(self):
        self.portal_flag = True

    def out_portal(self):
        self.portal_flag = False

    def portal_open(self):
        self.bsemi =False