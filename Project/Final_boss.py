from pico2d import*
import random
import json

class Final:
    PIXEL_PER_METER = (10.0 / 0.3)           # 10 pixel 30 cm
    RUN_SPEED_KMPH = 30.0                    # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 1.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 9
    FRAMES_PER_DIE = 4
    FRAMES_PER_SUMMON = 12
    FRAMES_PER_SKILL = 9
    SKILL_PER_TIME = 1.0 / 5
    SKILL2_PER_TIME = 1.0 / 1.5

    image = None
    hit = None
    die = None
    summon1 = None
    summon2 = None
    skill = None
    shadow = None
    hp_bar = None
    hp_cell = None
    # sound
    hit_sound = None
    die_sound = None
    skill_sound = None
    skill_sound2 = None

    def __init__(self):
        self.canvas_width = get_canvas_width()
        self.canvas_height = get_canvas_height()
        self.x = 1200
        self.y = 235
        self.min = 0
        self.max = 0
        self.life_flag = True
        # 능력치
        self.hp = 200
        self.total_frames = random.randint(0,6)
        self.frame = 0
        #hit
        self.h_time = 0
        self.b_hit = False
        self.frame_hit = 0
        #die
        self.d_time = 0
        self.b_die = False
        self.die_frame = 0
        self.frame_die = 0
        self.total_die = 0.0
        #summon
        self.s_time = 0
        self.summon_frame = 0
        self.b_summon1 = False
        self.b_summon2 = False
        self.total_summon = 0.0
        #skill
        self.skill_time = 0
        self.skill_frame = 0
        self.b_skill = False
        self.b_skill1 = False
        self.b_patt = False
        self.total_skill = 0.0

        if Final.image == None:
            Final.image = load_image('Resource/Monster/Final/final_stand.png')
        if Final.hit == None:
            Final.hit = load_image('Resource/Monster/Final/final_hit.png')
        if Final.summon1 == None:
            Final.summon1 = load_image('Resource/Monster/Final/final_summon1.png')
        if Final.summon2 == None:
            Final.summon2 = load_image('Resource/Monster/Final/final_summon2.png')
        if Final.die == None:
            Final.die = load_image('Resource/Monster/Final/final_die.png')
        if Final.skill == None:
            Final.skill = load_image("Resource/Monster/Final/final_skill.png")
        if Final.hp_bar == None:
            Final.hp_bar = load_image("Resource/Ui/Final_Boss_Hp.png")
        if Final.hp_cell == None:
            Final.hp_cell = load_image("Resource/Ui/Final_Boss_Cell.png")
        # sound
        if Final.hit_sound == None:
            Final.hit_sound = load_wav("Resource/Sound/hit.wav")
            Final.hit_sound.set_volume(32)
        if Final.die_sound == None:
            Final.die_sound = load_wav("Resource/Sound/boss_die.wav")
            Final.die_sound.set_volume(32)
        if Final.skill_sound == None:
            Final.skill_sound = load_wav("Resource/Sound/boss_skill.wav")
            Final.skill_sound.set_volume(32)
        if Final.skill_sound2 == None:
            Final.skill_sound2 = load_wav("Resource/Sound/boss_Skill2.wav")
            Final.skill_sound2.set_volume(32)

    def update(self, frame_time):
        self.total_frames += Final.FRAMES_PER_ACTION * Final.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 9
        self.die_frame = int(self.total_die) % 4
        self.summon_frame = int(self.total_summon) % 12
        self.skill_frame = int(self.total_skill) % 9

        if self.b_hit == True:
            self.h_time += frame_time
            if self.h_time >= 0.5:
               self.h_time = 0
               self.b_hit = False

        if self.b_die == True:
            self.total_die += Final.FRAMES_PER_DIE * Final.ACTION_PER_TIME * frame_time
            self.d_time += frame_time
            if self.d_time >= 3.0:
                self.life_flag = False
                self.d_time = 0

        if self.b_summon1 == True:
            self.total_summon += Final.FRAMES_PER_SUMMON * Final.ACTION_PER_TIME * frame_time
            self.s_time += frame_time
            if self.s_time >= 1.5:
                self.total_summon = 0
                self.b_summon1 = False
                self.s_time = 0

        if self.b_summon2 == True:
            self.total_summon += Final.FRAMES_PER_SUMMON * Final.ACTION_PER_TIME * frame_time
            self.s_time += frame_time
            if self.s_time >= 1.5:
                self.total_summon = 0
                self.b_summon2 = False
                self.s_time = 0

        if self.b_skill == True:
            self.total_skill += Final.FRAMES_PER_SKILL * Final.SKILL2_PER_TIME* frame_time
            self.skill_time += frame_time
            if self.skill_time >= 1.2:
                self.total_skill = 0
                self.skill_time = 0
                self.b_skill = False

        if self.b_skill1 == True:
            self.total_skill += Final.FRAMES_PER_SKILL * Final.SKILL_PER_TIME* frame_time
            self.skill_time += frame_time
            if self.skill_time >= 1.4:
                self.total_skill = 0
                self.skill_time = 0
                self.b_skill1 = False


    def hurt(self,att):
        self.b_hit = True
        self.hp -= att
        self.hit_sound.play()

    def death(self):
        self.b_die = True
        self.die_sound.play()

    def summonning1(self):
        self.b_summon1 = True
        self.b_skill = True
        self.skill_sound.play()

    def summonning2(self):
        self.b_summon2 = True
        self.b_skill1 = True
        self.skill_sound2.play()

    def draw(self):
        sx = self.x - self.fl.left
        self.hp_bar.clip_draw(0,0,804,29,512,500)
        for i in range(0,int(self.hp//2)):
            self.hp_cell.clip_draw(0,0,10,25,216-99+(i*8),500)
        if self.b_hit == True:
            self.hit.clip_draw(0,self.frame_hit * 570 ,900,570,sx + 230,self.y + 50)
        elif self.b_die == True:
            self.die.clip_draw(self.die_frame * 900, 0 ,900,580,sx + 230,self.y + 50)
        elif self.b_summon2 == True:
            self.summon1.clip_draw(self.summon_frame * 900 , 0 , 900 , 585 ,sx + 230, self.y + 50)
        elif self.b_summon1 == True:
            self.summon2.clip_draw(self.summon_frame * 900 , 0 , 900 , 585 ,sx + 230, self.y + 50)
        else:
            self.image.clip_draw(self.frame * 900,0, 900, 570, sx + 230, self.y + 50)

        if self.b_skill == True:
             self.skill.clip_draw(self.skill_frame * 147, 0,147,111,sx - 100,100)
             self.skill.clip_draw(self.skill_frame * 147, 0,147,111,sx - 300,100)
             self.skill.clip_draw(self.skill_frame * 147, 0,147,111,sx - 500,100)
             self.skill.clip_draw(self.skill_frame * 147, 0,147,111,sx - 700,100)

    def get_bb(self):
        sx = self.x - self.fl.left
        return sx - 30, self.y - 60, sx + 100, self.y + 100

    def get_skill_1(self):
        sx = self.x - self.fl.left
        if self.skill_time >= 0.65:
            return sx - 145, self.y- 180 , sx - 55, self.y
    def get_skill_2(self):
        sx = self.x - self.fl.left
        if self.skill_time >= 0.65:
            return sx - 345, self.y- 180 , sx - 255, self.y
    def get_skill_3(self):
        sx = self.x - self.fl.left
        if self.skill_time >= 0.65:
            return sx - 545, self.y- 180 , sx - 455, self.y
    def get_skill_4(self):
        sx = self.x - self.fl.left
        if self.skill_time >= 0.65:
            return sx - 745, self.y- 180 , sx -655, self.y
#
    def get_skill_5(self):
        sx = self.x - self.fl.left
        if self.skill_time >= 1.0:
            return sx - 1025 - 300 , self.y-60 - 150 , sx + 1025 - 300, self.y + 10 - 180

    def draw_bb(self):
        draw_rectangle(*self.get_bb())
        if self.b_skill == True:
            if self.skill_time >= 0.65:
                draw_rectangle(*self.get_skill_1())
                draw_rectangle(*self.get_skill_2())
                draw_rectangle(*self.get_skill_3())
                draw_rectangle(*self.get_skill_4())
        if self.b_skill1 == True:
            if self.skill_time >= 1.0:
                draw_rectangle(*self.get_skill_5())


    def set_floor(self,fl):
        self.fl = fl



