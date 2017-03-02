from PinRobot import PinRobot
from Restful import RESTfulServer
import os

def main():
    global robot
    robot = PinRobot()
    robot.InitializeTerminal(os.path.join("Configuration", "YoximoRest.xml"))
    robot.InitializeConnection("172.20.50.177", 23)
    try:
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
