from PinRobot import PinRobot

def main():
    global robot
    robot = PinRobot()
    #robot.InitializeTerminal("Yoximo.xml")
    #robot.InitializeConnection("192.168.1.102", 23)
    try:
        name = input("Enter path to XML: ")
        if(False is robot.InitializeTerminal(name)):
            raise ParseError("InitializeTerminal", "Parsing Error")

        IP = input("Enter IP: ")
        Port = input("Enter Port: ")
        if(False is robot.InitializeConnection(IP, int(Port))):
            raise ConnectionError("InitializeConnection", "Could not connect")


        Keypress = input("Enter key[0-9][Ok][Menu][Stop][.][*][#]: ")
        while('x' not in Keypress):
            if(False is robot.SendCommand(Keypress)):
                raise InputError(Keypress, "No command found")
            Keypress = input("Enter key[0-9][Ok][Menu][Stop][.][*][#]: ") 
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
