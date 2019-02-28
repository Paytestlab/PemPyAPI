#!/usr/bin/python3

from Parsers.ParseXml import XmlParser;
from Robot.Communication import PEMSocket;
from Base.DeviceBase import DeviceBase;
import logging
from Exception.Exception import DeviceStateError, ConnectionError;

class PinRobot(DeviceBase):

    def __init__(self, id, enable_statistics=False, empower_card=False):
        DeviceBase.__init__(self, id, enable_statistics);
        self.empower_card = empower_card;
        logging.info("robot({}): initialization start...".format(self.id));

    def initialize_device(self, filename):
        self.terminalList = XmlParser.parse_terminals(filename, self.id)
        if(self.terminalList is None):
            logging.warning("robot({}): initialization failed, skip...".format(self.id));
            return False
        
        logging.info("robot({}): initialization successful...".format(self.id));
        return True

    def initialize_connection(self, IP, Port):
        self.socket = PEMSocket(IP, Port)
   
        return self.connect()

    def connect(self):
        try:

            if(self.socket.connect() is True):
                response = self.socket.receive();
                logging.debug("robot({}): received {}".format(self.id, response.replace('\r\n', '')));
                if("Smoothie command shell" in response):
                    return True;
        except TimeoutError:
            pass;
        return False;

    def close_connection(self):
        try:
            self.socket.close() 
        except OSError:
            pass;

    def __ResponseEvaluate(self, response):
        logging.debug("robot({}): received {}".format(self.id, response.replace('\r\n', '')))
        Result = False
        if(not response):
            return False;
        if("ok" in response):
           Result = True
        elif("!!" in response):
            raise DeviceStateError("", "Robot error:{}".format(response));
        else:
           return False

        return Result

    def send_command(self, action):
        Result = False
        try:

           if(not self.terminalList[action].IsButton):
               self.__increaseZCurrent();
                             
           actionValue = self.terminalList[action].Value;
           logging.debug("robot({}): send to robot({}):".format(self.id, actionValue.replace('\r\n', ' ')))
           self.socket.send(actionValue);
                         
           Result = self.__ResponseEvaluate(self.socket.receive());
           shouldPress = Result and self.terminalList[action].IsButton;

           if(shouldPress):
              Result = self.__pressButton();
           elif(Result):
              self.__reduceZCurrent();

           logging.info("robot({}): execution of {} was successful".format(self.id, action))
        except TimeoutError:
            logging.error("robot({}): while performing the action {}, the device did not respond in time".format(self.id, action));
            pass;
        except DeviceStateError as e:
            logging.error("robot({}): device is in an error state".format(self.id));
            pass;
        except:
            logging.error("robot({}): unknown exception happened...".format(self.id));
            pass

        return Result;

    def SendString(self, command):
        logging.debug("robot({}): sending ({}):".format(self.id, command.replace('\r\n', ' ')))
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
