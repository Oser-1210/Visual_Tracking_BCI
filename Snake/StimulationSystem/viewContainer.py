import math
from numpy import random
import math

class viewContainer():
    # container 应该包含所有刺激所需的要素
    def __init__(self, config) -> None:

        # w 代表window,所有的刺激都要在win上显示
        self.w = None
        # displayFrame是呈现最终结果的刺激帧
        self.displayFrame = None
        # frameSet是ImageStim的集合,是刺激帧
        self.frameSet = None
        # targetFrame是目标图案
        self.targetFrame = None
        # targetPos是注视点在屏幕上的位置
        self.targetPos = None
        # trackPos是追踪点在屏幕上的位置
        self.trackPos = [0, 0]
        # 蛇身
        self.snakebody = []
        # 蛇身图案
        self.snakeFrame = []



        self.takeConfig(config)
        self.getTGPos()
        
        pass

    def takeConfig(self, config):

        self.resolution = config.resolution
        self.step = config.step
        self.window_size = config.window_size
        self.stiLEN = config.stiLEN
        self.cubSize = config.cubicSize
        window_x, window_y = config.window_size
        self.boundary = [math.floor(window_x/2), math.floor(window_y/2)]


        pass
    
    def getTGPos(self,):
        
        window_x, window_y = self.window_size
        x = int(random.randint(math.floor(window_x/(2*self.step))*2-1) - (math.floor(window_x/(2*self.step))-1))
        y = int(random.randint(math.floor(window_y/(2*self.step))*2-1) - (math.floor(window_y/(2*self.step))-1))
        self.targetPos = [x*self.step, y*self.step]
        
        if abs(self.trackPos[0]-self.targetPos[0]) + abs(self.trackPos[1]-self.targetPos[1]) == 0:
            self.getTGPos()
        if self.targetPos in self.snakebody: 
            self.getTGPos()
    
