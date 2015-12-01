__author__ = '사랑마을'

from pico2d import *

class Time:
    def __init__(self):
        self.font = load_font('Resource/Ui/ConsolaMalgun.ttf',40)

    def update(self,frame_time):
        self.time = get_time()

    def draw(self):
        self.font.draw(300,550,"Time : %f " % self.time)
