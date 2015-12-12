from pico2d import*

class Item:
    TIME_PER_ACTION = 1
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 2

    box = None
    slot = None
    hit = None

    def __init__(self):
        self.canvas_width = get_canvas_width()
        self.canvas_height = get_canvas_height()
        self.x = 0
        self.y = 0
        self.hp = 30
        self.total_frames = 0
        self.frame = 0
        #hit
        self.h_time = 0
        self.b_hit = False
        self.frame_hit = 0
        #
        self.b_die = False

        if Item.box == None:
            Item.box = load_image('Resource/Item/box.png')
        if Item.slot == None:
            Item.slot = load_image('Resource/Item/item.png')
        if Item.hit == None:
            Item.hit = load_image('Resource/Item/box_hit.png')

    def update(self, frame_time):
        self.total_frames += Item.FRAMES_PER_ACTION * Item.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 2
        if self.b_hit == True:
            self.h_time += frame_time
            if self.h_time >= 0.3:
               self.h_time = 0
               self.b_hit = False

    def hurt(self,att):
        self.b_hit = True
        self.hp -= att
        print("박스 hp = %d" %(self.hp))

    def death(self):
        self.b_die = True
        self.b_hit= False

    def draw(self):
        sx = self.x - self.fl.left

        if self.b_hit == True:
            self.hit.clip_draw(0,0 ,100,55,sx + 3000,self.y + 55)
        elif self.b_die == True:
            self.slot.clip_draw(0,0,32,32,sx+3000,self.y + 45)
        else:
            self.box.clip_draw(self.frame * 100,0, 100, 55, sx + 3000, self.y + 55)

    def get_bb(self):
        sx = self.x - self.fl.left
        if self.b_die == True:
            return sx + 2990, self.y + 30,  sx + 3010, self.y + 65
        else:
            return sx + 2950, self.y + 30, sx + 3020, self.y + 65

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def set_floor(self,fl):
        self.fl = fl
