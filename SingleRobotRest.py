from PinRobot import PinRobot
from Restful import RESTfulServer
from Utilities import Utilities
from Exception import Error, ConnectionError, InputError, ParseError, NotImplementedError
import os
from os import listdir
from os.path import isfile, join
import json
import logging


def main():
    global robot
    robot = PinRobot()
    _path = "ConfigRest"
    result = False

    FORMAT = "%(asctime)-15s %(levelname)s: %(message)s";

    logging.basicConfig(format=FORMAT, level=logging.WARNING);

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

        server = RESTfulServer(doPostWork, doGetWork, robot)
    except Error as e:    
        logging.critical(e)
        pass

def doPostWork(jsonString, Robot):
    j = json.loads(jsonString)
        
    for command in j["commands"]:
        if(True is Robot.SendCommand(command)):
            logging.INFO("post : execution of " + command + " was succesful")
        else:
            raise    
        
def doGetWork(Robot):
    raise NotImplementedError


main()
