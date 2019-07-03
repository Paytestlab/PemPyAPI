#!/usr/bin/python3


from Robot.Communication import PEMSocket;
from Base.DeviceBase import DeviceBase;
import logging
from Exception.Exception import DeviceStateError, ConnectionError;
from Robot.BasicRobotCommands import BasicRobotCommands;
from Parsers.RobotLayout import RobotLayout;

class PinRobot(DeviceBase):

    robotCommands = BasicRobotCommands();
    tag = "robot";
    def __init__(self, id, enable_statistics=False):
        super().__init__(id, RobotLayout, enable_statistics);
        self.robotCommands = BasicRobotCommands();

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
           actionValue = self.layout.get_action(action);
           logging.debug("robot({}): send to robot({}):".format(self.id, actionValue.replace('\r\n', ' ')))
           self.socket.send(actionValue);
                         
           Result = self.__ResponseEvaluate(self.socket.receive());
           shouldPress = Result and self.layout.is_button(action);

           if(shouldPress):
              Result = self.__pressButton();

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
        return self.SendString(self.robotCommands.key_press)

    def get_mac_address(self):
        return self.id;

    def remove_card(self):
        return self.SendString(self.robotCommands.remove_card);

    def home(self):
        return self.SendString(self.robotCommands.home);
