from math import floor


class Config():

    def __init__(self) -> None:
        self.defaultConfig()
        pass

    def defaultConfig(self,):

        self.displayINFO()
        self.subINFO()
        self.expINFO()
        self.connectINFO()
        self.tkinterINFO()

        pass

    def subINFO(self, personName='Oser', age='21', gender='m'):
        self.personName = personName
        self.age = age
        self.gender = gender
        pass

    def displayINFO(self, refreshRate=60, stiLEN=3, window_size=[800, 800], step=69, full=0.95, real_wz=(22.5, 22.5)):

        self.refreshRate = refreshRate
        self.stiLEN = stiLEN

        self.resolution = (2*window_size[0], 2*window_size[1])
        self.window_size = (window_size[0], window_size[1])
        self.step = step
        # compute layout
        layout_x = floor(2*window_size[0]/step)
        if layout_x % 2 == 0: layout_x -= 1
        layout_y = floor(2*window_size[1]/step)
        if layout_y % 2 == 0: layout_y -= 1
        self.layout = (layout_x, layout_y)
        cubicSize = round(step*full)
        self.cubicSize = cubicSize
        self.interval = step - cubicSize
        self.trim = ((2*window_size[0]-layout_x*step)/2 + self.interval/2, (2*window_size[1]-layout_y*step)/2 + self.interval/2)
        self.target_size = round(cubicSize*0.7)
        
        self.real_wz = real_wz
        self.addSTI = None
        self.addTG = None
        self.addMap = None

        pass

    def expINFO(self, COM='abcd', classNUM=8, blockNUM=6, srate=250, winLEN=1, stepLEN=None, chnNUM=9, saveAdd='picFolder', lag=0.14, n_band=5, p=0.01):

        self.saveAdd = saveAdd
        self.COM = COM
        self.classNUM = classNUM
        self.blockNUM = blockNUM
        self.srate = srate
        self.winLEN = winLEN
        self.stepLEN = stepLEN
        self.chnNUM = chnNUM
        self.lag = lag
        self.n_band = n_band
        self.p = p

        pass

    def connectINFO(self, streaming_ip='10.0.0.2', streaming_port=4000, record_srate=1000, client_ip='10.0.0.3', client_port=11000):

        self.streaming_ip = streaming_ip
        self.streaming_port = streaming_port
        self.record_srate = record_srate

        self.client_ip = client_ip
        self.client_port = client_port

        pass
    
    def tkinterINFO(self, pen=2, color='#000000', multiple=5):
        
        self.color = color
        self.pen = pen
        self.multiple = multiple

        pass

if __name__ == '__main__':

    config = Config()

 
