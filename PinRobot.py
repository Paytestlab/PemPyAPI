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
        elif("!!" in response):
            Result = self.SendCommand("Reset")
            Result |= self.SendCommand("Home")
        else:
           return False

        return Result

    def SendCommand(self, action):
        try:
           isButton = False
           value = self.terminalList[action].Value
           self.socket.send(value)
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
        return True
    #self.__ResponseEvaluate(self.socket.receive())


    def __pressButton(self):
        """press button function"""
        #There are 2 possibilities to control the speed of the button press:
        #1. Remove the "G4 S1.1" and listen to Smoothie responses in the function SendString.
        #2. Try to reduce the value in the comman S1.1. The value 1.1 is in seconds. The less seconds set, the faster the button will be pressed.

        if(self.SendString("M42\r\n") is False):
            return False
        if(self.SendString("G4 P30\r\n") is False):
            return False
        if(self.SendString("M43\r\n") is False):
            return False
        #return True
        return self.SendString("G4 S1.1\r\n")
            
            
        



   
                
        





