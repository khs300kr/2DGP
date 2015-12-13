from pico2d import*

class Item:
    TIME_PER_ACTION = 1
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 2

    box = None
    slot = None
    hit = None
    #sound
    hit_sound = None
    eat_sound = None

    def __init__(self):
        self.canvas_width = get_canvas_width()
        self.canvas_height = get_canvas_height()
        self.x = 0
        self.y = 0
        self.hp = 10
        self.total_frames = 0
        self.frame = 0
        #hit
        self.h_time = 0
        self.b_hit = False
        self.frame_hit = 0
        #
        self.b_die = False
        self.bitem = False

        if Item.box == None:
            Item.box = load_image('Resource/Item/box.png')
        if Item.slot == None:
            Item.slot = load_image('Resource/Item/item.png')
        if Item.hit == None:
            Item.hit = load_image('Resource/Item/box_hit.png')
        if Item.hit_sound == None:
            Item.hit_sound = load_wav("Resource/Sound/box_hits.wav")
        if Item.eat_sound == None:
            Item.eat_sound = load_wav("Resource/Sound/item_bite.wav")
            Item.eat_sound.set_volume(80)

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
        Item.hit_sound.play()

    def death(self):
        self.b_die = True
        self.b_hit= False
# first stage
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

# second stage
    def draw_semi(self):
        if self.bitem == True:
            sx = self.x - self.fl.left
            if self.b_hit == True:
                self.hit.clip_draw(0,0 ,100,55,sx + 1200,self.y + 195)
            elif self.b_die == True:
                self.slot.clip_draw(0,0,32,32,sx+1200,self.y + 185)
            else:
                self.box.clip_draw(self.frame * 100,0, 100, 55, sx + 1200, self.y + 195)

    def get_cc(self):
        sx = self.x - self.fl.left
        if self.b_die == True:
            return sx + 1190, self.y + 170,  sx + 1210, self.y + 205
        else:
            return sx + 1150, self.y + 170, sx + 1220, self.y + 205

    def draw_semi_cc(self):
        if self.bitem == True:
            draw_rectangle(*self.get_cc())


    def set_floor(self,fl):
        self.fl = fl

    def eat(self):
        Item.eat_sound.play()


    def place_item(self):
        self.bitem = True