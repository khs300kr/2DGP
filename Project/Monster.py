from pico2d import*


class Monster:
    PIXEL_PER_METER = (10.0 / 0.3)           # 10 pixel 30 cm
    RUN_SPEED_KMPH = 20.0                    # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 4

    image = None
    jump = None
    attack = None

    R_STAND, R_WALK, L_STAND, L_WALK = 0, 1, 2, 3

    def __init__(self):
        self.x = 100
        self.y = 145
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

        if Character.image == None:
            Character.image = load_image('Resource/Character/Moving.png')
        if Character.jump == None:
            Character.jump = load_image('Resource/Character/jump.png')
        if Character.attack == None:
            Character.attack = load_image('Resource/Character/attack.png')

    def update(self, frame_time):
        def clamp(minimum, x, maximum):
            return max(minimum, min(x, maximum))

        self.life_time += frame_time
        distance = Character.RUN_SPEED_PPS * frame_time
        self.total_frames += Character.FRAMES_PER_ACTION * Character.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 4
        self.x += (self.dir * distance)

        self.x = clamp(0, self.x, 2048)

        if self.b_jump == True:
            self.j_time += 0.5
            self.y -= -15 + (0.98 * self.j_time * self.j_time) / 2
            if self.y <= 145:
                self.j_time = 0
                self.b_jump = False
                self.y = 145
        if self.b_attack == True:
            self.a_time += 0.5
            if self.a_time >= 2:
                self.a_time = 0
                self.b_attack = False

        delay(0.04)

    def draw(self):
        if self.b_jump == True:
            self.jump.clip_draw(0,self.frame_jump * 100, 100, 100, self.x,self.y)
        elif self.b_attack == True:
            self.attack.clip_draw(0,self.frame_attack * 100 , 100 ,100 ,self.x, self.y)
        else:
            self.image.clip_draw(self.frame * 100, self.state * 125, 100, 100, self.x, self.y)

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
        elif event.key == SDLK_c:
                self.b_jump = True
        elif event.key == SDLK_x:
                self.b_attack = True

    def get_bb(self):
        return self.x - 40, self.y - 50, self.x + 10, self.y + 50

    def draw_bb(self):
        draw_rectangle(*self.get_bb())
