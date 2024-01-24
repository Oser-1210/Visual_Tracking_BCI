from psychopy import parallel


class EventController():
    def __init__(self, COM='3EFC') -> None:
        # hex 2 dec
        self.address = int(COM, 16)
        # self.address = 12544
        self.port = parallel.ParallelPort(self.address)
        self.clearEvent()

    def sendEvent(self, eventType):
        self.port.setData(eventType)

    def clearEvent(self):
        self.port.setData(0)
