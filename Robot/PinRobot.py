#!/usr/bin/python3


from Robot.Communication import PEMSocket;
from Base.DeviceBase import DeviceBase;
import logging
from Exception.Exception import PemDeviceStateError, PemConnectionError, PemTimeoutError;
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
        except PemConnectionError:
            pass;
        return False;

    def close_connection(self):
        try:
            if(self.socket):
                self.socket.close();
        except OSError:
            pass;

    def send_command(self, key):
        result = False
        try:
           if(self.layout.is_button(key)):
               result = self.__send_key_press(key);
           else:
               result = self.__send_action(key);

           logging.info("robot({}): execution of {} was successful".format(self.id, key))
        except PemTimeoutError:
            logging.error("robot({}): while performing the action {}, the device did not respond in time".format(self.id, key));
            pass;
        except PemDeviceStateError:
            logging.error("robot({}): device is in an error state".format(self.id));
            pass;
        except:
            logging.error("robot({}): unknown exception happened...".format(self.id));
            result = False;
            pass

        return result;

    def __send_key_press(self, key):
        if(self.__send_action(key)):
            return self.__press_button();
        else:
            return False;

    def __send_action(self, key):
        action = self.layout.get_action(key);
        return self.__send_to_robot(action);

    def __press_button(self):
        """press button function"""
        return self.__send_to_robot(self.robotCommands.key_press)

    def get_mac_address(self):
        return self.id;

    def remove_card(self):
        return self.__send_to_robot(self.robotCommands.remove_card);

    def home(self):
        return self.__send_to_robot(self.robotCommands.home);

    def __send_to_robot(self, command):
        logging.debug("robot({}): send to robot ({}):".format(self.id, command.replace('\r\n', ' ')))
        self.socket.send(command)

        return self.__response_evaluate(self.socket.receive())

    def __response_evaluate(self, response):
        logging.debug("robot({}): received {}".format(self.id, response.replace('\r\n', '')))
        Result = False
        if(not response):
            return False;
        elif("ok" in response):
           Result = True
        elif("!!" in response):
            raise PemDeviceStateError("", "Robot error:{}".format(response));
        else:
           return False

        return Result
