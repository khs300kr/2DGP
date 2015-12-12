from pico2d import *
from Bullet import *


class Character:
    PIXEL_PER_METER = (10.0 / 0.3)           # 10 pixel 100 cm
    RUN_SPEED_KMPH = 30.0                    # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 1.0
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 4

    #sprite
    image = None
    jump = None
    attack = None
    hp = None
    hp_title = None
    skill_cell = None
    skill_title = None
    death = None
    respawn = None
    death_screnn = None
    #sound
    jump_sound = None
    shoot_sound = None
    skill_sound = None

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
        self.life = 3
        self.skill = 0
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
        self.b_skill = False
        self.frame_attack = 0
        #death
        self.b_death = False
        #respawn
        self.respawn_frame = 0.0
        self.b_respawn = False
        self.r_time = 0

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
        if Character.respawn == None:
            Character.respawn = load_image("Resource/Effect/respawn.png")
        if Character.death_screnn == None:
            Character.death_screnn = load_image("Resource/Ui/die.png")
        if Character.skill_title == None:
            Character.skill_title = load_image("Resource/Ui/Skill_Title.png")
        if Character.skill_cell == None:
            Character.skill_cell = load_image("Resource/Ui/skill_cell.png")
        # sound
        if Character.jump_sound == None:
            Character.jump_sound = load_wav("Resource/Sound/jump.wav")
            Character.jump_sound.set_volume(32)
        if Character.shoot_sound == None:
            Character.shoot_sound = load_wav("Resource/Sound/shoot.wav")
            Character.shoot_sound.set_volume(32)
        if Character.skill_sound == None:
            Character.skill_sound = load_wav("Resource/Sound/skill.wav")
            Character.skill_sound.set_volume(32)


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
        if self.b_attack == True:
            self.a_time += frame_time
            if self.a_time >= 0.5:
                self.a_time = 0
                self.b_attack = False
        #death
        if self.b_death == True:
            self.x -= (self.dir * self.speed)

        #respawn
        if self.b_respawn == True:
            self.respawn_frame = int(self.total_frames) % 7
            self.r_time += frame_time
            if self.r_time >= 5.5:
                self.r_time = 0
                self.b_respawn = False



    def draw(self):
        x_left_offset = min(0,self.x-self.canvas_width//2)
        x_right_offset = max(0,self.x - self.fl.w + self.canvas_width//2)
        x_offset = x_left_offset + x_right_offset

        self.hp_title.clip_draw(0,0,244,35,150,550)
        self.hp.clip_draw(0 ,0,self.life * 30 , 25 , 150 , 550)
        self.skill_title.clip_draw(0,0,150,35,850,550)
        self.skill_cell.clip_draw(0,0,self.skill * 30,30,840,550)

        if self.b_jump == True:
            self.jump.clip_draw(0,self.frame_jump * 100, 100, 100, self.canvas_width//2+x_offset,self.y)
        elif self.b_attack == True:
            self.attack.clip_draw(0,self.frame_attack * 100 , 100 ,100 ,self.canvas_width//2+x_offset, self.y)
        elif self.b_death == True:
            self.death.clip_draw(0,0,101,47,self.canvas_width//2+x_offset - 15 ,self.y - 28)
            self.death_screnn.draw(512,300)
        else:
            self.image.clip_draw(self.frame * 100, self.state * 125, 100, 100, self.canvas_width//2+x_offset,
                                 self.y)
        if self.b_respawn == True:
            self.respawn.clip_draw(self.respawn_frame * 200 , 0 , 200 , 200 , self.canvas_width//2+x_offset , self.y + 45 )



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
                if self.b_death == True:  #부활
                    self.b_respawn = True
                    self.b_death = False
                else:
                    self.b_jump = True
                    self.jump_sound.play()
        elif (event.type,event.key) == (SDL_KEYDOWN,SDLK_x):
                if self.b_death == True: # 부활
                    self.b_respawn = True
                    self.b_death = False
                else:
                    self.b_attack = True
                    self.shoot_sound.play()
        elif (event.type,event.key) == (SDL_KEYUP,SDLK_x):
                self.b_attack = False

        elif (event.type,event.key) == (SDL_KEYDOWN,SDLK_z):
                if self.b_death == True: # 부활
                    pass
                else:
                    self.b_skill = True
        elif (event.type,event.key) == (SDL_KEYUP,SDLK_z):
                self.b_skill = False

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

    def skillup(self):
        self.skill = 3
    def skilldown(self):
        self.skill -= 1

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
