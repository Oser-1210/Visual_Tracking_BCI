import sys
sys.path.append('.')

import time
from CommonSystem.Config import Config
from StimulationSystem.stimulationOperator import stimulationOperator
from StimulationSystem.StimulationProcess.VTbciStiController import StiController 
from CommonSystem.MessageReceiver.ExchangeMessageManagement import ExchangeMessageManagement

# ----
config = Config()
config.displayINFO(target_size=0.1)
config.addSTI = 'StimulationSystem/pics'
config.addTG = 'StimulationSystem/target/green_point_10.png'
# 并口号
config.COM = '3100'
config.stiLEN = 1
config.blockNUM = 12
config.personName = 'Oser'



stimulationOperator = stimulationOperator()

messenager = ExchangeMessageManagement('server',stimulationOperator,config)
messenager.start()


stimulationOperator.messenager = messenager


stimulator = StiController().initial(config,messenager)
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
