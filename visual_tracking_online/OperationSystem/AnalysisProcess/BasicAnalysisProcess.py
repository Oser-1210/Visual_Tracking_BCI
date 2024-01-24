from abc import ABCMeta, abstractmethod
import os

class BasicAnalysisProcess:
    def __init__(self) -> None:
        pass


    @abstractmethod
    def initial(self, controller=None, config=None, streaming=None, messenager=None):

        # 3 essentials: controller, config, and data streaming client
        self.controller = controller
        self.config = config
        self.streaming = streaming
        self.messenager = messenager
        
        self.blockNUM = config.blockNUM
        
        # 初始化算法，提供所需参数
        self.winLEN = config.winLEN
        self.stepLEN = config.stepLEN
        self.srate = config.srate
        self.personName = config.personName
        self.n_band = config.n_band
        self.lag = config.lag
        self.p = config.p
        self.montage = config.classNUM
        
        self.prepareFolder()

    def prepareFolder(self):
        fatherAdd = 'OperationSystem/ResultStored'
        sonAdd = os.path.join(fatherAdd, self.personName)
        if not os.path.exists(sonAdd):
            os.makedirs(os.path.join(sonAdd,'models'))
            os.makedirs(os.path.join(sonAdd,'data'))
            os.makedirs(os.path.join(sonAdd,'test'))
        self.savepath = sonAdd
        return


    @abstractmethod
    def run(self):

        pass
    
            
    @abstractmethod
    def clear(self):
        self.cacheData = None
        return
        
    @abstractmethod
    def getResult(self,data):
        result = self.algorithm.predict(data, self.p)
        return result[0]

