from pico2d import *
import random

class Floor:
    TIME_PER_ACTION = 1.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 5

    image = None
    portal = None

    def __init__(self):
        if Floor.image == None:
            self.image = load_image('Resource/Map/final_boss.png')
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
        #
        self.bquake = False
        self.quake_time = 0
    def set_center_object(self, character):
        self.set_center_object = character

    def draw(self):
        if self.bquake == True:
            self.image.clip_draw_to_origin(self.left,0,self.canvas_width ,self.canvas_height,random.randint(0,3),random.randint(0,3))
        else:
            self.image.clip_draw_to_origin(self.left,0,self.canvas_width ,self.canvas_height,0,0)

    def update(self,frame_time):
        self.left = clamp(0,int(self.set_center_object.x ) - self.canvas_width//2, self.w - self.canvas_width)

        if self.bquake == True:
            self.total_frames += Floor.FRAMES_PER_ACTION * Floor.ACTION_PER_TIME* frame_time
            self.quake_time += frame_time
            if self.quake_time >= 1.5:
                self.total_frames = 0
                self.quake_time = 0
                self.bquake = False


    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        sx = self.x - self.left
        return sx,0,sx + 1600,50

    def handle_event(self, event):
        pass

    def quake(self):
        self.bquake = True
