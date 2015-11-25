from pico2d import*
import random
import json


class Semi:
    PIXEL_PER_METER = (10.0 / 0.3)           # 10 pixel 30 cm
    RUN_SPEED_KMPH = 30.0                    # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.8
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 6
    FRAMES_PER_DIE = 12

    image = None
    hit = None
    die = None
    summon = None

    def __init__(self):
        self.canvas_width = get_canvas_width()
        self.canvas_height = get_canvas_height()
        self.x = 1200
        self.y = 235
        self.min = 0
        self.max = 0
        self.life_flag = True
        # 능력치
        self.hp = 10
        self.total_frames = random.randint(0,6)
        self.frame = 0
        self.total_die = 0.0
        #hit
        self.h_time = 0
        self.b_hit = False
        self.frame_hit = 0
        #die
        self.d_time = 0
        self.b_die = False
        self.die_frame = 0
        self.frame_die = 0
        #summon
        self.s_time = 0
        self.summon_frame = 0
        self.b_summon = False

        if Semi.image == None:
            Semi.image = load_image('Resource/Monster/Semi/semi_stand.png')
        if Semi.hit == None:
            Semi.hit = load_image('Resource/Monster/Semi/semi_hit.png')
        #if Semi.summon == None:
        #   Semi.summon = load_image('Resource/Monster/Semi/semi.summon.png')
        if Semi.die == None:
           Semi.die = load_image('Resource/Monster/Semi/semi_die.png')

    def update(self, frame_time):
        self.total_frames += Mush.FRAMES_PER_ACTION * Mush.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 6
        self.die_frame = int(self.total_die) % 12

        if self.b_hit == True:
            self.h_time += frame_time
            if self.h_time >= 0.5:
               self.h_time = 0
               self.b_hit = False

        if self.b_die == True:
            self.total_die += Mush.FRAMES_PER_DIE * Mush.ACTION_PER_TIME * frame_time
            self.d_time += frame_time
            if self.d_time >= 3.2:
                self.life_flag = False
                print("False")
                self.d_time = 0

    def hurt(self,att):
        self.b_hit = True
        self.hp -= att
        print("Semi hp = %d" %(self.hp))

    def death(self):
        self.b_die = True

    def draw(self):
        sx = self.x - self.fl.left

        if self.b_hit == True:
            self.hit.clip_draw(0,self.frame_hit * 130 ,110,130,sx,self.y)
        elif self.b_die == True:
            self.die.clip_draw(self.die_frame * 200, 0 ,200,200,sx,self.y)
        else:
            self.image.clip_draw(self.frame * 100,0, 100, 130, sx, self.y)

    def get_bb(self):
        sx = self.x - self.fl.left
        return sx - 45, self.y - 60, sx + 35, self.y + 30

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def set_floor(self,fl):
        self.fl = fl


#######################################################################################################################



class Mush:
    PIXEL_PER_METER = (10.0 / 0.3)           # 10 pixel 30 cm
    RUN_SPEED_KMPH = 30.0                    # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.8
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 4
    FRAMES_PER_DIE = 3

    image = None
    hit = None
    die = None

    L_WALK,R_WALK = 0, 1

    def __init__(self):
        self.canvas_width = get_canvas_width()
        self.canvas_height = get_canvas_height()
        self.x = 900
        self.y = 150
        self.min = 0
        self.max = 0
        self.dir = -1
        self.state = self.L_WALK
        self.life_flag = True
        # 능력치
        self.hp = 3
        self.total_frames = random.randint(0,3)
        self.frame = 0
        self.total_die = 0.0
        self.dir = -1
        #hit
        self.h_time = 0
        self.b_hit = False
        self.frame_hit = 0
        #die
        self.d_time = 0
        self.b_die = False
        self.die_frame = 0
        self.frame_die = 0

        if Mush.image == None:
            Mush.image = load_image('Resource/Monster/Mush/mush_run.png')
        if Mush.hit == None:
            Mush.hit = load_image('Resource/Monster/Mush/mush_hit.png')
        if Mush.die == None:
            Mush.die = load_image('Resource/Monster/Mush/mush_die.png')

    def update(self, frame_time):
        self.total_frames += Mush.FRAMES_PER_ACTION * Mush.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 4
        self.die_frame = int(self.total_die) % 3

        if self.b_die == False:
            self.x += frame_time * Mush.RUN_SPEED_PPS * self.dir

        if self.x < self.min:
            self.dir = 1
            self.state = self.R_WALK
            self.frame_hit = 1
            self.frame_die = 1
        elif self.x > self.max:
            self.dir = -1
            self.state = self.L_WALK
            self.frame_hit = 0
            self.frame_die = 0

        if self.b_hit == True:
            self.h_time += frame_time
            if self.h_time >= 0.3:
               self.h_time = 0
               self.b_hit = False

        if self.b_die == True:
            self.total_die += Mush.FRAMES_PER_DIE * Mush.ACTION_PER_TIME * frame_time
            self.d_time += frame_time
            if self.d_time >= 0.7:
                self.life_flag = False
                self.d_time = 0


    def hurt(self,att):
        self.b_hit = True
        self.hp -= att
        print("몬스터 hp = %d" %(self.hp))

    def death(self):
        self.b_die = True

    def draw(self):
        sx = self.x - self.fl.left

        if self.b_hit == True:
            self.hit.clip_draw(0,self.frame_hit * 80 ,100,80,sx,self.y)
        elif self.b_die == True:
            self.die.clip_draw(self.die_frame * 100, self.frame_die * 65 ,100,65,sx,self.y-15)
        else:
            self.image.clip_draw(self.frame * 100,self.state*80, 100, 80, sx, self.y)

    def get_bb(self):
        sx = self.x - self.fl.left
        return sx - 40, self.y - 40, sx + 10, self.y + 20

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def set_floor(self,fl):
        self.fl = fl


def create_mush():
    team_data_text = '\
{\
    "Mush1" : {"StartState":"L_WALK", "x":400, "y":90, "min":0, "max":500},\
	"Mush2"    : {"StartState":"L_WALK", "x":500, "y":90, "min":0, "max":500},\
	"Mush3"   : {"StartState":"R_WALK", "x":800, "y":210, "min":600, "max":1500},\
	"Mush4"    : {"StartState":"L_WALK", "x":900, "y":210, "min":600, "max":1500},\
	"Mush5"   : {"StartState":"R_WALK", "x":1000, "y":210, "min":600, "max":1500},\
	"Mush6"   : {"StartState":"L_WALK", "x":1100, "y":210, "min":600, "max":1500}\
}\
'

    mush_state_table = {
        "L_WALK" : Mush.L_WALK,
        "R_WALK" : Mush.R_WALK,
    }
    team_data = json.loads(team_data_text)
    mushs = []

    for name in team_data:
        mush = Mush()
        mush.name = name
        mush.x = team_data[name]['x']
        mush.y = team_data[name]['y']
        mush.min = team_data[name]['min']
        mush.max = team_data[name]['max']
        mush.state = mush_state_table[team_data[name]['StartState']]
        mushs.append(mush)

    return mushs