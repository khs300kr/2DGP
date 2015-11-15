from pico2d import*


class Monster:
    PIXEL_PER_METER = (10.0 / 0.3)           # 10 pixel 30 cm
    RUN_SPEED_KMPH = 20.0                    # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.8
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 3

    image = None
    hit = None
    die = None

    def __init__(self):
        self.x = 1200
        self.y = 125
        self.speed = 300
        self.total_frames = 0.0
        self.frame = 0
        self.dir = -1
        #hit
        self.j_time = 0
        self.b_hit = False
        self.frame_hit = 0
        #die
        self.a_time = 0
        self.b_die = False
        self.frame_die = 0

        if Monster.image == None:
            Monster.image = load_image('Resource/Monster/Sheep/sheep_run.png')
        if Monster.hit == None:
            Monster.hit = load_image('Resource/Monster/Sheep/sheep_hit.png')
        if Monster.die == None:
            Monster.die = load_image('Resource/Monster/Sheep/sheep_die.png')

    def update(self, frame_time):
        def clamp(minimum, x, maximum):
            return max(minimum, min(x, maximum))

        self.total_frames += Monster.FRAMES_PER_ACTION * Monster.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 3
        self.x -= frame_time * self.speed
        self.x = clamp(100, self.x, 2048)

        #if self.b_hit == True:
            #self.j_time += 0.5
            #self.y -= -15 + (0.98 * self.j_time * self.j_time) / 2
            #if self.y <= 145:
             #   self.j_time = 0
              #  self.b_jump = False
              #  self.y = 145
           # pass
       # if self.b_die == True:
           # self.a_time += 0.5
           # if self.a_time >= 2:
               # self.a_time = 0
                #self.b_attack = False
           # pass


    def draw(self):
        if self.b_hit == True:
            self.hit.clip_draw(0,65, 100, 100, self.x,self.y)
       # elif self.b_die == True:
            #pass
           # self.die.clip_draw(self.frame_die * 100,65 , 100 ,100 ,self.x, self.y)
        else:
            self.image.clip_draw(self.frame * 100,0, 100, 65, self.x, self.y)

    def get_bb(self):
        return self.x - 40, self.y - 30, self.x + 30, self.y + 20

    def draw_bb(self):
        draw_rectangle(*self.get_bb())
