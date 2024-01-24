import numpy as np
import sys
import scipy.io as scio
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import os
import matplotlib
from tqdm import tqdm
import math
matplotlib.use('agg')
    
class frameLoader():
    def __init__(self) -> None:

        self.frameSet = None
        self.displayFrame = None

        pass


def fig2data(f):
    """
    fig = plt.figure()
    image = fig2data(fig)
    @brief Convert a Matplotlib figure to a 4D numpy array with RGBA channels and return it
    @param fig a matplotlib figure
    @return a numpy 3D array of RGBA values
    """
    import PIL.Image as Image
    # draw the renderer
    f.canvas.draw()

    # Get the RGBA buffer from the figure
    w, h = f.canvas.get_width_height()
    buf = np.fromstring(f.canvas.tostring_argb(), dtype=np.uint8)
    buf.shape = (w, h, 4)

    # canvas.tostring_argb give pixmap in ARGB mode. Roll the ALPHA channel to have it in RGBA mode
    buf = np.roll(buf, 3, axis=2)
    image = Image.frombytes("RGBA", (w, h), buf.tostring())
    image = np.asarray(image)
    return image


class UIFactory:

    def __init__(self,config):
        
        x_resolution, y_resolution = config.resolution
        self.refreshRate = config.refreshRate
        self.stiLEN = config.stiLEN
        
        self.maxFrames = int(self.refreshRate*self.stiLEN)
        self.resolution = math.ceil(math.sqrt(x_resolution*x_resolution+y_resolution*y_resolution))

        self.saveFolder = os.path.join(
            os.getcwd(),'StimulationSystem', 'pics')
        if os.path.exists(self.saveFolder) is False:
            os.makedirs(self.saveFolder)
        
    
    def getFrames(self):

        pieSet = []
        # 刺激
        cwd = sys.path[0]
        file = os.path.join(cwd, 'Code', 'finalstim.mat')
        stim = scio.loadmat(file)['wn']
        # 角度
        angles = [22.5, 67.5, 112.5, 157.5, 202.5, 247.5, 292.5, 337.5]
        stimINX = [0, 1, 3, 4, 5, 6, 7, 8]
        color = 0.5
        pointSize = 0.002

        frameSet = []
        for N in tqdm(range(self.maxFrames+1)):
            # 从此循环进入每一帧
            f = plt.figure(figsize=(self.resolution/100, self.resolution/100), facecolor='none', dpi=100)
            plt.xlim(0, 1)
            plt.ylim(0, 1)
            plt.gca().xaxis.set_major_locator(plt.NullLocator())
            plt.gca().yaxis.set_major_locator(plt.NullLocator())
            plt.subplots_adjust(top=1, bottom=0, left=0,
                                right=1, hspace=0, wspace=0)

            plt.rcParams['axes.unicode_minus'] = False  # 这两行需要手动设置
            current_axis = plt.gca()

            
            if N == 0:
                target = patches.Wedge((0.5,0.5), pointSize, 0, 360, facecolor=[1, 0, 0], alpha=1)
                current_axis.add_patch(target)
            else:
                for pieINX in range(len(angles)):
                    
                    if pieINX == len(angles) - 1:
                        start_angle = angles[pieINX]
                        end_angle = angles[0]
                    else:
                        start_angle = angles[pieINX]
                        end_angle = angles[pieINX+1]
    
                    pie = patches.Wedge((0.5,0.5), 0.5, start_angle, end_angle, facecolor=[color, color, color], alpha=stim[N-1, stimINX[pieINX]])
                    current_axis.add_patch(pie)
                target = patches.Wedge((0.5,0.5), pointSize, 0, 360, facecolor=[1, 0, 0], alpha=1)
                current_axis.add_patch(target)

            plt.axis('off')
            frameSet.append(fig2data(f))
            plt.close(f)

        frames = frameLoader()
        frames.displayFrame = frameSet.pop(0)
        frames.frameSet = frameSet

        return frames


    def saveFrames(self,frames):

        frameSet = frames.frameSet
        for i, frame in enumerate(frameSet):
            plt.imsave(self.saveFolder+os.sep+'%i.png' % i, frame)
            
        displayFrame = frames.displayFrame
        plt.imsave(self.saveFolder+os.sep+'display_frame.png', displayFrame)



        



