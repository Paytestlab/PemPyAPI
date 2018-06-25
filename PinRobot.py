from ParseXml import XmlParser;
from Communication import PEMSocket;
from DeviceBase import DeviceBase;
import logging

class PinRobot(DeviceBase):
    """Initializes the robot class"""
    def __init__(self, enable_statistics=False, empower_card=False):
        DeviceBase.__init__(self, enable_statistics);
        self.empower_card = empower_card;
        

    def InitializeTerminal(self, Filename):
        self.terminalList = XmlParser.parseXml(Filename)
        if(self.terminalList is None):
            return False
        return True

    def InitializeConnection(self, IP, Port):
        self.socket = PEMSocket(IP, Port)
   
        return self.socket.connect()

    def connect(self):
        return self.socket.connect();

    def close_connection(self):
        try:
            self.socket.close() 
        except OSError:
            pass;

    def __ResponseEvaluate(self, response):
        logging.debug("received from robot {}".format(response.replace('\r\n', '')))
        Result = False
        if("ok" in response):
           Result = True
        elif(response in "Smoothie"):
           Result = self.__ResponseEvaluate(self.socket.receiveWithTimeout(2))
        elif("!!" in response):
            Result = self.send_command("Reset")
            Result |= self.send_command("Home")
        else:
           return False

        return Result



    def send_command(self, action):
        Result = False
        try:

           if(not self.terminalList[action].IsButton):
               self.__increaseZCurrent();
                             
           actionValue = self.terminalList[action].Value;
           logging.debug("send to robot({}):".format(actionValue.replace('\r\n', ' ')))
           self.socket.send(actionValue);
                         
           Result = self.__ResponseEvaluate(self.socket.receive());
           shouldPress = Result and self.terminalList[action].IsButton;

           if(shouldPress):
              Result = self.__pressButton();
           else:
              self.__reduceZCurrent();
        except:
            pass

        return Result;

    def SendString(self, command):
        logging.debug("send to robot({}):".format(command.replace('\r\n', ' ')))
        self.socket.send(command)

        return self.__ResponseEvaluate(self.socket.receive())

    def ReceiveResponse(self):
        self.__ResponseEvaluate(self.socket.receive())

    def __pressButton(self):
        """press button function"""
       
        #There are 2 possibilities to control the speed of the button press:
        #1. Remove the "G4 S1.1" and listen to Smoothie responses in the function SendString.
        #2. Try to reduce the value in the command S1.1. The value 1.1 is in seconds. The lower the value (in seconds), the faster the button will be pressed.
        pressButtonCommands = [
            "M42", 
            "G4 P30", 
            "M43", 
            "G4 P800"
            ]

        fullCommand =  "\r\n".join(pressButtonCommands) + "\r\n";
           
        return self.SendString(fullCommand)

       
    def __increaseZCurrent(self):
        """Increases the current for Z Axis if enabled"""
        if(self.empower_card is True):
            increaseCurrent = "M907 Z1.3\r\n"
            return self.SendString(increaseCurrent)
        else:
            return True;


    def __reduceZCurrent(self):
        """Decreases the current for Z Axis"""
        if(self.empower_card is True):
            reduceCurrent = "M907 Z0.5\r\n"
            return self.SendString(reduceCurrent)
        else:
            return True;
        



   
                
        





