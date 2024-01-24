from cmath import sqrt
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
        self.targetPosition = []
        # trackPos是追踪点在屏幕上的位置
        self.trackPos = [0, 0]
        self.trackPosition = []
        # distance是track和target的初始距离
        self.distance = []


        self.takeConfig(config)
        self.gettargetPos()
        self.getdistance()
        
        pass

    def takeConfig(self, config):

        self.windowSize = config.window_size
        self.targetSize = config.target_size
        pass

    
    
    def gettargetPos(self):
        
        win_x, win_y = self.windowSize
        x = int(random.randint(round(3/4*win_x)) - (3/4*win_x)/2)
        y = int(random.randint(round(3/4*win_y)) - (3/4*win_x)/2)
        
        if math.sqrt((self.trackPos[0]-x)**2+(self.trackPos[1]-y)**2) <= self.targetSize/2:
            self.gettargetPos()
            
        self.targetPos = [x, y]
        self.targetPosition.append(self.targetPos)
        return
    
    def getdistance(self):
        
        x = abs(self.trackPos[0]-self.targetPos[0])
        y = abs(self.trackPos[1]-self.targetPos[1])
        self.distance.append(sqrt(x*x+y*y))