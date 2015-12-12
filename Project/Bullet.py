from pico2d import*


class Bullet:
    PIXEL_PER_METER = (10.0 / 0.3 )         # 10 pixel 30cm
    BULLET_SPEED_KMPH = 60.0                   # km / Hour
    BULLET_SPEED_MPM = (BULLET_SPEED_KMPH * 1000.0 / 60.0)
    BULLET_SPEED_MPS = (BULLET_SPEED_MPM / 60.0)
    BULLET_SPEED_PPS = (BULLET_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 2
    BULLET_SPEED = 5

    image = None

    R_STAND, R_WALK, L_STAND, L_WALK = 0, 1, 2, 3

    def __init__(self,x,y,state,bg):
        self.canvas_width = get_canvas_width()
        self.canvas_height = get_canvas_height()
        self.x = x
        self.y = y - 20
        self.sx = 0
        self.flag = 0
        self.total_frames = 0
        self.frame = 0
        self.state = state
        self.bg = bg
        if self.state in (self.R_STAND,self.R_WALK):
            self.dir = 1
        elif self.state in(self.L_STAND,self.L_WALK):
            self.dir = -1
        if Bullet.image == None:
            Bullet.image = load_image('Resource/Bullet/Bullet.png')

    def update(self, frame_time):
        def clamp(minimum, x, maximum):
            return max(minimum, min(x, maximum))
        speed = Bullet.BULLET_SPEED_PPS * frame_time
        self.x += (self.dir * speed)
        self.total_frames += Bullet.FRAMES_PER_ACTION * Bullet.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 2

        self.x = clamp(0, self.x, self.bg.w)

    def draw(self):
        self.sx = self.x - self.bg.left
        if self.state in (self.R_STAND,self.R_WALK):
            self.image.clip_draw(self.frame * 100, 0,100,20,self.sx,self.y)
        elif self.state in(self.L_STAND,self.L_WALK):
            self.image.clip_draw(self.frame * 100, 20,100,20,self.sx,self.y)

    def get_bb(self):
        sx = self.x - self.bg.left
        if self.state in (self.R_STAND,self.R_WALK):
            return sx + 30, self.y - 5, sx + 45, self.y + 5
        if self.state in(self.L_STAND,self.L_WALK):
            return sx - 30, self.y - 5, sx - 45, self.y + 5

    def draw_bb(self):
            draw_rectangle(*self.get_bb())


class Skill:
    PIXEL_PER_METER = (10.0 / 0.3 )         # 10 pixel 30cm
    BULLET_SPEED_KMPH = 30.0                   # km / Hour
    BULLET_SPEED_MPM = (BULLET_SPEED_KMPH * 1000.0 / 60.0)
    BULLET_SPEED_MPS = (BULLET_SPEED_MPM / 60.0)
    BULLET_SPEED_PPS = (BULLET_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 2
    FRAMES_PER_SKILL = 5

    image = None
    hit = None

    R_STAND, R_WALK, L_STAND, L_WALK = 0, 1, 2, 3

    def __init__(self,x,y,state,bg):
        self.canvas_width = get_canvas_width()
        self.canvas_height = get_canvas_height()
        self.x = x
        self.y = y - 20
        self.sx = 0
        self.flag = 0
        self.total_frames = 0
        self.frame = 0
        self.state = state
        self.bg = bg
        #hit
        self.h_time = 0
        self.b_hit = False
        self.frame_hit = 0
        self.total_hit = 0
        if self.state in (self.R_STAND,self.R_WALK):
            self.dir = 1
        elif self.state in(self.L_STAND,self.L_WALK):
            self.dir = -1
        if Skill.image == None:
            Skill.image = load_image('Resource/Bullet/character_skill.png')
        if Skill.hit == None:
            Skill.hit = load_image('Resource/Bullet/skill_hit.png')
    def update(self, frame_time):
        self.frame_hit = int(self.total_hit) % 5
        def clamp(minimum, x, maximum):
            return max(minimum, min(x, maximum))
        speed = Skill.BULLET_SPEED_PPS * frame_time
        self.x += (self.dir * speed)
        self.total_frames += Skill.FRAMES_PER_ACTION * Skill.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 2
        self.x = clamp(0, self.x, self.bg.w)

        if self.b_hit == True:
            self.total_hit += Skill.FRAMES_PER_SKILL * Skill.ACTION_PER_TIME * frame_time
            self.h_time += frame_time
            if self.h_time >= 0.5:
                self.b_hit = False
                self.h_time = 0

    def draw(self):
        self.sx = self.x - self.bg.left
        if self.state in (self.R_STAND,self.R_WALK):
            self.image.clip_draw(self.frame * 200, 0,200,100,self.sx,self.y + 20)
            if self.b_hit == True:
                self.hit.clip_draw(self.frame_hit * 250,0,250,280,self.sx + 20,self.y + 50)
        elif self.state in(self.L_STAND,self.L_WALK):
            self.image.clip_draw(self.frame * 200, 100,200,100,self.sx,self.y + 20)
            if self.b_hit == True:
                self.hit.clip_draw(self.frame_hit * 250,0,250,280,self.sx - 20,self.y + 50)

    def get_bb(self):
        sx = self.x - self.bg.left
        if self.state in (self.R_STAND,self.R_WALK):
            return sx + 30, self.y - 5, sx + 90, self.y + 20
        if self.state in(self.L_STAND,self.L_WALK):
            return sx - 90, self.y - 5, sx - 30, self.y + 20
    def draw_bb(self):
            draw_rectangle(*self.get_bb())

    def hits(self):
        self.b_hit = True
