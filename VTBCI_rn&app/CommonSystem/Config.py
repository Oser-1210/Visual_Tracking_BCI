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

    def displayINFO(self, refreshRate=60, stiLEN=3, window_size=(800, 800), target_size=0.1, screen=(1920, 1080)):

        self.refreshRate = refreshRate
        self.stiLEN = stiLEN
        win_x, win_y = window_size
        self.resolution = (2*win_x, 2*win_y)
        self.window_size = window_size
        self.target_size = round(win_x*target_size)
        self.screen = screen

        self.addSTI = None
        self.addTG = None

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

 
