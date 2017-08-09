from PinRobot import PinRobot
from Restful import RESTfulServer
import os
from os import listdir
from os.path import isfile, join


def main():
    global robot
    robot = PinRobot()

    try:
        onlyfiles = [f for f in listdir("ConfigRest") if isfile(join("ConfigRest", f))]
        print("Select the terminal Layout and press Enter:")
        i = 0;
        for files in onlyfiles:
            i += 1
            print(str(i) + ": " + files[:-4])
            

        name = int(input())
       
        if(False is robot.InitializeTerminal(join("ConfigRest", onlyfiles[name - 1]))):
            raise ParseError("InitializeTerminal", "Parsing Error")

        IP = input("Enter Robot IP: ")

        if(False is robot.InitializeConnection(IP, 23)):
            raise ConnectionError("InitializeConnection", "Could not connect")

        server = RESTfulServer(robot)
    except (InputError,ConnectionError,ParseError):
        pass

    
    
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
