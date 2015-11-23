from pico2d import*
import random


class Sheep:
    PIXEL_PER_METER = (10.0 / 0.3)           # 10 pixel 30 cm
    RUN_SPEED_KMPH = 30.0                    # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.8
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 3
    FRAMES_PER_DIE = 5

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
        self.hp = 5
        self.speed = 300
        self.total_frames = random.randint(0,2)
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

        if Sheep.image == None:
            Sheep.image = load_image('Resource/Monster/Sheep/sheep_run.png')
        if Sheep.hit == None:
            Sheep.hit = load_image('Resource/Monster/Sheep/sheep_hit.png')
        if Sheep.die == None:
            Sheep.die = load_image('Resource/Monster/Sheep/sheep_die.png')

    def update(self, frame_time):
        self.total_frames += Sheep.FRAMES_PER_ACTION * Sheep.ACTION_PER_TIME * frame_time
        self.total_die += Sheep.FRAMES_PER_DIE * Sheep.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 3
        self.die_frame = int(self.total_die) % 5

        if self.b_die == False:
            self.x += frame_time * Sheep.RUN_SPEED_PPS * self.dir

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
            self.h_time += 0.1
            if self.h_time >= 2:
               self.h_time = 0
               self.b_hit = False

        if self.b_die == True:
            self.d_time += 0.1
            if self.d_time >= 3.8:
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
            self.hit.clip_draw(0,self.frame_hit * 65 ,100,65,sx,self.y)
        elif self.b_die == True:
            self.die.clip_draw(self.die_frame * 100, self.frame_die * 65 ,100,65,sx,self.y)
        else:
            self.image.clip_draw(self.frame * 100,self.state*65, 100, 65, sx, self.y)

    def get_bb(self):
        sx = self.x - self.fl.left
        return sx - 40, self.y - 30, sx + 30, self.y + 20

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def set_floor(self,fl):
        self.fl = fl


def create_sheep():
    team_data_text = '\
{\
    "Sheep1" : {"StartState":"L_WALK", "x":1800, "y":195, "min":0, "max":2000},\
	"Sheep2"    : {"StartState":"L_WALK", "x":1900, "y":195, "min":0, "max":2000},\
	"Sheep3"   : {"StartState":"L_WALK", "x":2000, "y":195, "min":0, "max":2000},\
	"Sheep4"    : {"StartState":"R_WALK", "x":2100, "y":120, "min":2120, "max":2700},\
	"Sheep5"   : {"StartState":"R_WALK", "x":2250, "y":120, "min":2120, "max":2700},\
	"Sheep6"   : {"StartState":"R_WALK", "x":2350, "y":120, "min":2120, "max":2700},\
	"Sheep7"    : {"StartState":"R_WALK", "x":2950, "y":60, "min":2780, "max":3200},\
	"Sheep8"   : {"StartState":"R_WALK", "x":3050, "y":60, "min":2780, "max":3200},\
	"Sheep9"   : {"StartState":"R_WALK", "x":3150, "y":60, "min":2780, "max":3200},\
	"Sheep10" : {"StartState":"R_WALK", "x":3500, "y":180, "min":3350, "max":3600}\
}\
'
    yang_state_table = {
        "L_WALK" : Sheep.L_WALK,
        "R_WALK" : Sheep.R_WALK,
    }
    team_data = json.loads(team_data_text)
    yangs = []

    for name in team_data:
        yang = Sheep()
        yang.name = name
        yang.x = team_data[name]['x']
        yang.y = team_data[name]['y']
        yang.min = team_data[name]['min']
        yang.max = team_data[name]['max']
        yang.state = yang_state_table[team_data[name]['StartState']]
        yangs.append(yang)

    return yangs