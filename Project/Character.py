from pico2d import *
from Bullet import *


class Character:
    PIXEL_PER_METER = (10.0 / 0.3)           # 10 pixel 100 cm
    RUN_SPEED_KMPH = 150.0                    # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 1.0
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 4

    image = None
    jump = None
    attack = None
    hp = None
    hp_title = None
    death = None

    R_STAND, R_WALK, L_STAND, L_WALK = 0, 1, 2, 3

    def __init__(self):
        self.canvas_width = get_canvas_width()
        self.canvas_height = get_canvas_height()
        self.x = 100
        self.y = 215
        self.fy = 0
        self.speed = 0
        #능력치
        self.att = 1
        self.life = 5
        #
        self.life_time = 0.0
        self.total_frames = 0.0
        self.frame = 0
        self.dir = 0
        self.state = self.R_STAND
        #jump
        self.j_time = 0
        self.b_jump = False
        self.frame_jump = 0
        #attack
        self.a_time = 0
        self.b_attack = False
        self.frame_attack = 0
        #death
        self.b_death = False

        if Character.image == None:
            Character.image = load_image('Resource/Character/Moving.png')
        if Character.jump == None:
            Character.jump = load_image('Resource/Character/jump.png')
        if Character.attack == None:
            Character.attack = load_image('Resource/Character/attack.png')
        if Character.hp == None:
            Character.hp = load_image('Resource/Ui/Hp.png')
        if Character.hp_title == None:
            Character.hp_title = load_image("Resource/Ui/Hp_Title.png")
        if Character.death == None:
            Character.death = load_image("Resource/Ui/Death.png")

    def update(self, frame_time):
        def clamp(minimum, x, maximum):
            return max(minimum, min(x, maximum))

        self.life_time += frame_time
        self.speed = Character.RUN_SPEED_PPS * frame_time
        self.total_frames += Character.FRAMES_PER_ACTION * Character.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 4
        self.x += (self.dir * self.speed)
        self.x = clamp(0, self.x, self.fl.w)
        #jump
        if self.b_jump == True:
            self.j_time += 0.18
            self.y -= -9 + (0.98 * self.j_time * self.j_time) / 2
            if self.y <= self.fy:
                self.j_time = 0
                self.b_jump = False
                self.y = self.fy
        else: # 중력 적용
            self.y += -9 + (0.98) / 2
        #attack
        if self.b_attack == 1:
            self.a_time += 0.1
            if self.a_time >= 2:
                self.a_time = 0
                self.b_attack = False
        #death
        if self.b_death == True:
            self.x -= (self.dir * self.speed)


    def draw(self):
        x_left_offset = min(0,self.x-self.canvas_width//2)
        x_right_offset = max(0,self.x - self.fl.w + self.canvas_width//2)
        x_offset = x_left_offset + x_right_offset

        self.hp_title.clip_draw(0,0,244,35,150,550)
        self.hp.clip_draw(0 ,0,self.life * 30 , 25 , 150 , 550)

        if self.b_jump == True:
            self.jump.clip_draw(0,self.frame_jump * 100, 100, 100, self.canvas_width//2+x_offset,self.y)
        elif self.b_attack == True:
            self.attack.clip_draw(0,self.frame_attack * 100 , 100 ,100 ,self.canvas_width//2+x_offset, self.y)
        elif self.b_death == True:
            self.death.clip_draw(0,0,101,47,self.canvas_width//2+x_offset - 15 ,self.y - 28)
        else:
            self.image.clip_draw(self.frame * 100, self.state * 125, 100, 100, self.canvas_width//2+x_offset,
                                 self.y)

    def handle_event(self,event):
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):
            if self.state in (self.R_STAND, self.L_STAND, self.R_WALK):
                self.state = self.L_WALK
                self.dir = -1
                self.frame_jump = 1
                self.frame_attack = 1
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
            if self.state in (self.R_STAND, self.L_STAND, self.L_WALK):
                self.state = self.R_WALK
                self.dir = 1
                self.frame_jump = 0
                self.frame_attack = 0
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_LEFT):
            if self.state in (self.L_WALK,):
                self.state = self.L_STAND
                self.dir = 0
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_RIGHT):
            if self.state in (self.R_WALK,):
                self.state = self.R_STAND
                self.dir = 0
        elif (event.type,event.key) == (SDL_KEYDOWN,SDLK_c):
                self.b_jump = True
                if self.b_death == True:
                    self.b_death = False
        elif (event.type,event.key) == (SDL_KEYDOWN,SDLK_x):
                self.b_attack = True
                if self.b_death == True:
                    self.b_death = False
        elif (event.type,event.key) == (SDL_KEYUP,SDLK_x):
                self.b_attack = False

    def get_bb(self):
        x_left_offset = min(0,self.x-self.canvas_width//2)
        x_right_offset = max(0,self.x - self.fl.w + self.canvas_width//2)
        x_offset = x_left_offset + x_right_offset

        return self.canvas_width//2+x_offset - 35, self.y - 50, self.canvas_width//2+x_offset + 5, self.y + 35

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def die(self):
        self.life -= 1
        self.b_death = True

    def set_floor(self,fl):
        self.fl = fl

# Stage1 충돌
    def floor_collidebb(self):
        self.y = 165 + 50
        self.fy = 165 + 50
    def floor_collidecc(self):
        self.y = 90 + 50
        self.fy = 90 + 50
    def floor_collidedd(self):
        self.y = 30 + 50
        self.fy = 30 + 50
    def floor_collideff(self):
        self.y = 150 + 50
        self.fy = 150 + 50
    def floor_doublecollide_b_c(self):
        self.y = 90 + 50
        self.fy = 90 + 50
        if self.state in (self.L_WALK,):
            self.x -= (self.dir * self.speed)
    def floor_doublecollide_c_d(self):
        self.y = 30 + 50
        self.fy = 30 + 50
        if self.state in (self.L_WALK,):
            self.x -= (self.dir * self.speed)
    def floor_doublecollide_d_e(self):
        self.y = 30 + 50
        self.fy = 30 + 50
        if self.state in (self.R_WALK,):
            self.x -= (self.dir * self.speed)
    def floor_doublecollide_e_f(self):
        self.y = 90 + 50
        self.fy = 90 + 50
        if self.state in (self.R_WALK,):
            self.x -= (self.dir * self.speed)


        #semibos 충돌
    def semiboss_collidebb(self):
        self.y = 50 + 50
        self.fy = 50 + 50
    def semiboss_collidecc(self):
        self.y = 110 + 50
        self.fy = 110 + 50
    def semiboss_collidedd(self):
        self.y = 170 + 50
        self.fy = 170 + 50
    def semiboss_doublecollide_b_c(self):
        self.y = 50 + 50
        self.fy = 50 + 50
        if self.state in (self.R_WALK,):
            self.x -= (self.dir * self.speed)
    def semiboss_doublecollide_c_d(self):
        self.y = 110 + 50
        self.fy = 110 + 50
        if self.state in (self.R_WALK,):
            self.x -= (self.dir * self.speed)
