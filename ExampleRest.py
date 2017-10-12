from PinRobot import PinRobot
from Restful import RESTfulServer
from Utilities import Utilities
import os
from os import listdir
from os.path import isfile, join
import json


def main():
    global robot
    robot = PinRobot()
    _path = "ConfigRest"
    result = False

    try:
        files = Utilities.get_and_print_conf_list(_path)
        while result is False:
            index = int(input())
            if(index > len(files) or index <= 0):
                print("Wrong input, retry")
                continue

            config = Utilities.select_conf(_path, index);

            result = robot.InitializeTerminal(config)
            
            if(False is result):
                print("Could not initialize the terminal, please try again")

        IP = input("Enter Robot IP: ")

        if(False is robot.InitializeConnection(IP, 23)):
            raise ConnectionError("InitializeConnection", "Could not connect")

        server = RESTfulServer(doPostWork, robot)
    except (InputError,ConnectionError,ParseError):
        pass

def doPostWork(jsonString, Robot):
    j = json.loads(jsonString)
        
    for command in j["commands"]:
        if(True is Robot.SendCommand(command)):
            print("post : execution of " + command + " was succesful")
        else:
            raise         

    
    
class Error(Exception):
    pass

class InputError(Error):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

class ParseError(Error):
      def __init__(self, expression, message):
        self.expression = expression
        self.message = message


class ConnectionError(Error):
      def __init__(self, expression, message):
        self.expression = expression
        self.message = message

main()
