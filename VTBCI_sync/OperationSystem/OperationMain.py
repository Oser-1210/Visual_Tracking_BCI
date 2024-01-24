import sys
sys.path.append('.')

import time
from CommonSystem.MessageReceiver.ExchangeMessageManagement import ExchangeMessageManagement
from CommonSystem.Config import Config
from OperationSystem.operationOperator import operationOperator
from OperationSystem.AnalysisProcess.AnalysisController import AnalysisController
from OperationSystem.Streaming.NeuroScanEEG import NeuroScanEEGThread

# 创建实验信息从脚本函数中生成
config = Config()
config.expINFO(winLEN=1,lag=0.14, p=0.1)
config.connectINFO(streaming_ip='192.168.31.70',streaming_port=4000, client_ip='192.168.31.89', client_port=11000)
# config.connectINFO(streaming_ip='10.0.0.2',streaming_port=4000, client_ip='10.0.0.3', client_port=11000)
config.personName = 'Oser'

# 启动控制接收及结果管理器
operationOperator = operationOperator()  # 处理端接收消息处理函数

# 交换信息中心管理器
messenager = ExchangeMessageManagement('client',operationOperator, config)
# 启动与刺激系统数据交换器
messenager.start()


# 放大器设置
dataStreaming = NeuroScanEEGThread(config=config)
dataStreaming.connect()

operationOperator.messenager = messenager
operationOperator.streaming = dataStreaming

# 分析检测控制器
controller = AnalysisController().initial(config, dataStreaming, messenager)

# 启动采集端数据接收
dataStreaming.start()

print('Put on hold for stimulation,current state:%s'%messenager.state.control_state)

while messenager.state.control_state != 'STON':
    # 等待开始处理标识
    time.sleep(0.1)

while messenager.state.control_state != 'EXIT':
    controller.run()

messenager.stop()
dataStreaming.disconnect()