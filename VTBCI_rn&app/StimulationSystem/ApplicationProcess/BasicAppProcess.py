from abc import ABCMeta, abstractmethod
from EventController import EventController

class BasicAppProcess:

    def __init__(self) -> None:
        pass

    @abstractmethod
    def initial(self, controller, viewcontainer, messenager):

        self.controller = controller
        self.messenager = messenager
        self.viewcontainer = viewcontainer
        self.messenager.exchange_message_operator.controller = self.controller
        
        self.w = viewcontainer.w

        COM = self.controller.COM
        self.eventController = EventController(COM)

        pass

    
