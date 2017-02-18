from PinRobot import PinRobot
from Restful import RESTfulServer

def main():
    global robot
    robot = PinRobot()
    #robot.InitializeTerminal("Yoximo.xml")
    #robot.InitializeConnection("192.168.1.102", 23)
    try:
        #name = input("Enter path to XML: ")
        #if(False is robot.InitializeTerminal(name)):
        #    raise ParseError("InitializeTerminal", "Parsing Error")

        #IP = input("Enter IP: ")
        #Port = input("Enter Port: ")
        #if(False is robot.InitializeConnection(IP, int(Port))):
        #    raise ConnectionError("InitializeConnection", "Could not connect")

        server = RESTfulServer()
        server.start_server2(robot)
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
