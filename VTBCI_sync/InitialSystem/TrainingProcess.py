import os
import pickle
import numpy as np
from tqdm import tqdm
import math



class TrainingProcess():

    def __init__(self, config, dataStreaming) -> None:

        self.personName = config.personName
        # 默认保存在Operation里
        self.fatherAdd = 'OperationSystem/ResultStored'
        self.prepareFolder()
        self.streaming = dataStreaming

        self.config = config

        self.srate = config.srate
        self.winLEN = config.winLEN
        self.lag = config.lag
        self.n_band=config.n_band

        T = int(self.srate*(self.winLEN+self.lag))
        
        self.epochNUM_I = int(config.classNUM * config.blockNUM)
        self.epochNUM_II = int(config.posNUM * config.blockNUM)
        self.epochNUM = self.epochNUM_I + self.epochNUM_II
        self.classNUM = config.classNUM
        self.epochINX = 0
        self.chnNUM = config.chnNUM
        
        self.stage = 1
        
        w_width, _ = config.window_size
        radius = int(w_width/6)
        self.targetPosition = np.zeros((config.posNUM,2))
        
        for i in range(config.posNUM//2):
            angle = i*math.pi/8
            for j in range(2):
                the_radius = radius*(j+1)
                self.targetPosition[i*2+j, 0] = int(the_radius*math.cos(angle))
                self.targetPosition[i*2+j, 1] = int(the_radius*math.sin(angle))

        self.dataI = dict(
            X=np.zeros((self.epochNUM_I,self.chnNUM,T)),
            y=np.zeros(self.epochNUM_I)
        )
        self.dataII = dict(
            X=np.zeros((self.epochNUM_II,self.chnNUM,T)),
            y=np.zeros(self.epochNUM_II)
        )

        self.streaming.start()
        self.pbar = tqdm(total=self.epochNUM, desc="Progress")
        self.endFlag = False

        pass


    def prepareFolder(self):
        
        fatherAdd = self.fatherAdd
        sonAdd = os.path.join(fatherAdd,self.personName)
        if not os.path.exists(sonAdd):
            os.makedirs(os.path.join(sonAdd, 'models'))
            os.makedirs(os.path.join(sonAdd, 'data'))
            os.makedirs(os.path.join(sonAdd,'test'))
            os.makedirs(os.path.join(sonAdd,'info'))
        self.savepath = sonAdd
        
        return


    def collectData(self):

        while True:
            epoch, event = self.streaming.readFixedData(0, self.winLEN+self.lag)
            if epoch is not None:
                break
        
        if self.stage == 1:
            self.dataI['X'][self.epochINX] = epoch
            self.dataI['y'][self.epochINX] = event
        elif self.stage == 2:
            self.dataII['X'][self.epochINX] = epoch
            self.dataII['y'][self.epochINX] = event

        self.epochINX += 1
        self.pbar.update(1)

        if self.epochINX >= self.epochNUM_I and self.stage == 1:
            self.saveData()
            self.stage = 2
            self.epochINX = 0
            
        elif self.epochINX >= self.epochNUM_II and self.stage == 2:
            self.saveData()
            self.endFlag = True
            self.pbar.close()
            self.streaming.disconnect()


    def saveData(self):
        
        if self.stage == 1:
            with open(os.path.join(self.savepath, 'data/rawI.pickle'), "wb+") as fp:
                pickle.dump(self.dataI, fp, protocol=pickle.HIGHEST_PROTOCOL)
        else:
            with open(os.path.join(self.savepath, 'data/rawII.pickle'), "wb+") as fp:
                pickle.dump(self.dataII, fp, protocol=pickle.HIGHEST_PROTOCOL)


    def trainModel(self):

        from OperationSystem.AnalysisProcess.OperatorMethod.spatialFilter import TRCA
        # load data
        with open(self.savepath+os.sep+'data/rawI.pickle', "rb") as fp:
            dataI = pickle.load(fp)
        with open(self.savepath+os.sep+'data/rawII.pickle', "rb") as fp:
            dataII = pickle.load(fp)
        
        X_trca, y_trca = dataI['X'], dataI['y']
        X, y = dataII['X'], dataII['y']

        model = TRCA(winLEN=self.winLEN, lag=self.lag, srate=self.srate, montage=self.classNUM, n_band=self.n_band)
        model.fit(X_trca, y_trca)
        with open(os.path.join(self.savepath, 'models/model.pickle'), "wb+") as fp:
                pickle.dump(model, fp, protocol=pickle.HIGHEST_PROTOCOL)
        
        V = np.zeros((self.epochNUM_II,2))
        P = np.zeros((self.epochNUM_II,self.classNUM))
        for epochINX in range(self.epochNUM_II):
            epoch = X[epochINX]
            _, rho = model.predict(epoch, p=1)
            P[epochINX] = np.squeeze(np.maximum(rho,0))
            V[epochINX] = self.targetPosition[int(y[epochINX])-1]/0.46
            
        W = (np.linalg.inv(np.dot(P.T,P)).dot(P.T)).dot(V)
        
        with open(os.path.join(self.savepath, 'models/W.pickle'), "wb+") as fp:
                pickle.dump(W, fp, protocol=pickle.HIGHEST_PROTOCOL)

        return
    
