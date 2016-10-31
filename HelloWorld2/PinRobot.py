from ParseXml import XmlParser
from Communication import PEMSocket

class PinRobot(object):
    """Initializes the robot class"""
    def InitializeTerminal(self, Filename):
        self.terminalList = XmlParser.parseXml(Filename)
        if(self.terminalList is None):
            return False
        return True

    def InitializeConnection(self, IP, Port):
        self.socket = PEMSocket(IP, Port)
   
        return self.socket.connect()

    def CloseConnection(self):
        self.socket.close() 

    def __ResponseEvaluate(self, response):
        Result = False
        if("ok" in response):
           Result = True
        elif(response in "Smoothie"):
           Result = self.__ResponseEvaluate(self.socket.receiveWithTimeout(2))
        else:
           return False

        return Result

    def SendCommand(self, action):
        try:
           isButton = False
           self.socket.send(self.terminalList[action].Value)
           if(self.terminalList[action].IsButton is "1"):
               isButton = True
        except  (ValueError,IndexError):
            return False
        
        Result = self.__ResponseEvaluate(self.socket.receive())
        if(isButton is False):
            return Result
        elif(Result):
            return self.__pressButton()
        else:
            return False

    def SendString(self, command):
        self.socket.send(command)
        return self.__ResponseEvaluate(self.socket.receive())


    def __pressButton(self):
        """press button"""
        if(self.SendString("M42\r\n") is False):
            return False
        if(self.SendString("G4 P30\r\n") is False):
            return False
        if(self.SendString("M43\r\n") is False):
            return False
        return self.SendString("G4 S0.2\r\n")
            
            
        



   
                
        





