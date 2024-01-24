from cmath import sqrt
from numpy import random
import numpy as np
import math
import time

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
        # distance是track和target的初始距离
        self.distance = []


        self.takeConfig(config)
        self.createTargetPosition()
        
        pass

    def takeConfig(self, config):

        self.windowSize = config.window_size
        self.targetSize = config.target_size
        pass

    def createTargetPosition(self):
        
        w_width, _ = self.windowSize
        radius = int(w_width/6)
        targetPosition = np.zeros((32, 2))
        for i in range(16):
            angle = i*math.pi/8
            for j in range(2):
                the_radius = radius*(j+1)
                targetPosition[i*2+j, 0] = int(the_radius*math.cos(angle))
                targetPosition[i*2+j, 1] = int(the_radius*math.sin(angle))
        self.targetPosition = targetPosition
        
        random.seed(1)
        targetRandom = np.arange(targetPosition.shape[0])
        random.shuffle(targetRandom)
        self.targetRandom = targetRandom
        
        return
    
    def gettargetPos(self, cueINX):
        
        targetINX = self.targetRandom[cueINX % self.targetPosition.shape[0]]
        self.targetPos = self.targetPosition[targetINX]
        
        return
    
    def getdistance(self):
        
        x = abs(self.trackPos[0]-self.targetPos[0])
        y = abs(self.trackPos[1]-self.targetPos[1])
        self.distance.append(sqrt(x*x+y*y))