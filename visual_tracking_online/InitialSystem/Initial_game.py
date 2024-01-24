import sys
sys.path.append('.')

from TrainingProcess import TrainingProcess
from OperationSystem.Streaming.NeuroScanEEG import NeuroScanEEGThread
from CommonSystem.Config import Config

# 实验参数
config = Config()
config.expINFO(winLEN=1,lag=0.14)
config.connectINFO(streaming_ip='192.168.31.70',streaming_port=4000)
# config.connectINFO(streaming_ip='10.0.0.5',streaming_port=4000)
config.personName = input('Enter subject\'s name:')
config.blockNUM = 6

# 在线数据
dataStreaming = NeuroScanEEGThread(config=config)
dataStreaming.connect()

# training
trainprocess = TrainingProcess(config=config, dataStreaming=dataStreaming)

while not trainprocess.endFlag:
    trainprocess.collectData()

trainprocess.trainModel()
dataStreaming.disconnect()



