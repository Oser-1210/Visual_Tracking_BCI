import sys
sys.path.append('.')

import time
from CommonSystem.Config import Config
from StimulationSystem.stimulationOperator import stimulationOperator
from StimulationSystem.StimulationProcess.StimulationController import StimulationController 
from CommonSystem.MessageReceiver.ExchangeMessageManagement import ExchangeMessageManagement

# ----
config = Config()
config.displayINFO()
config.addSTI = 'StimulationSystem/pics'
config.addTG = 'StimulationSystem/target/cake.png'
# 并口号
config.COM = '3100'
config.stiLEN = 1

stimulationOperator = stimulationOperator()

messenager = ExchangeMessageManagement('server',stimulationOperator,config)
messenager.start()


stimulationOperator.messenager = messenager


stimulator = StimulationController().initial(config,messenager)
# stimulation准备好后给op发消息
message = 'STON'
messenager.send_exchange_message(message)

while messenager.state.status != 'TNOK':
    time.sleep(0.1)

stimFlag = True
while stimFlag:
    stimFlag = stimulator.run()

message = 'EXIT'
messenager.send_exchange_message(message)

time.sleep(2)
messenager.stop()
