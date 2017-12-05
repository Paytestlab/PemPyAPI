from ParseXml import XmlParser
from Communication import PEMSocket
import threading
import Statistics

class PinRobot(object):
    """Initializes the robot class"""
    def __init__(self, enable_statistics=False):
        self.mutex = threading.Lock()
        if(enable_statistics is True):
            self.statistics = Statistics.Statistics() 
        else:
            self.statistics = None

    def InitializeTerminal(self, Filename):
        self.terminalList = XmlParser.parseXml(Filename)
        if(self.terminalList is None):
            return False
        return True

    def InitializeConnection(self, IP, Port):
        self.socket = PEMSocket(IP, Port)
   
        return self.socket.connect()

    def Connect(self):
        self.socket.connect();

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

    def UpdateTable(self, id, action):
        if(self.statistics is not None):
            self.statistics.insert(id, action, self.terminalList[action].Value)

    def SendCommand(self, action):
        Result = False
        self.mutex.acquire()
      
        try:
           actionValue = self.terminalList[action].Value
           self.socket.send(actionValue)
                         
           Result = self.__ResponseEvaluate(self.socket.receive())
           shouldPress = Result and self.terminalList[action].IsButton

           if(shouldPress):
              Result = self.__pressButton()
        except:
            pass
        finally:
            self.mutex.release()
        return Result

    def SendString(self, command):
        self.socket.send(command)
        return True
        #self.__ResponseEvaluate(self.socket.receive())


    def __pressButton(self):
        """press button function"""
        try:
       
            #There are 2 possibilities to control the speed of the button press:
            #1. Remove the "G4 S1.1" and listen to Smoothie responses in the function SendString.
            #2. Try to reduce the value in the command S1.1. The value 1.1 is in seconds. The lower the value (in seconds), the faster the button will be pressed.
            pressButtonCommands = ["M42", "G4 P30", "M43", "G4 S1.0"]

            for command in pressButtonCommands:
                fullCommand = command + "\r\n"
                if(self.SendString(fullCommand) is False):
                    raise
            return True

        except:
            return False
            
            
        



   
                
        





