import numpy as np
import math
import os
import sys
import scipy.io as scio


class StimTargetRect():
    def __init__(self, rectINX, site_point, rect_size, fs, center):
        self.rectINX = rectINX
        self.site_point = site_point
        self.rect_size = rect_size
        self.fs = fs
        self.center = center
        self.form_flag_matrix = np.ones(rect_size, dtype = 'bool')
        self.position = self.covert2psycho()
        
    def cal_brightness(self, frame_no):
        
        color = 0.5    
        cwd = sys.path[0]
        file = os.path.join(cwd, 'Code', 'finalstim.mat')
        stim = scio.loadmat(file)['wn']
        if abs(self.center[0]-self.site_point[0]) + abs(self.center[1]-self.site_point[1]) == 0:
            brightness = -1
            alpha = 1
        else:
            angle = math.atan2(self.site_point[1]-self.center[1], self.site_point[0]-self.center[0])
            if angle <= math.pi/8 and angle > -math.pi/8:
                alpha = stim[frame_no, 0]
                brightness = color
            elif angle <= 3*math.pi/8 and angle > math.pi/8:
                alpha = stim[frame_no, 1]
                brightness = color
            elif angle <= 5*math.pi/8 and angle > 3*math.pi/8:
                alpha = stim[frame_no, 2]
                brightness = color
            elif angle <= 7*math.pi/8 and angle > 5*math.pi/8:
                alpha = stim[frame_no, 3]
                brightness = color
            elif angle <= -7*math.pi/8 or angle > 7*math.pi/8:
                alpha = stim[frame_no, 4]
                brightness = color
            elif angle <= -5*math.pi/8 and angle > -7*math.pi/8:
                alpha = stim[frame_no, 5]
                brightness = color
            elif angle <= -3*math.pi/8 and angle > -5*math.pi/8:
                alpha = stim[frame_no, 6]
                brightness = color
            else:
                alpha = stim[frame_no, 7]
                brightness = color
                      
        return brightness, alpha

    def covert2psycho(self):
        width = self.rect_size/2
        x,y = self.site_point
        x = x-1920/2 + width
        y = y-1080/2 + width

        return [x,y]


