from PinRobot import PinRobot
from Utilities import Utilities

def main():
    global robot
    robot = PinRobot()
    _path = "Configuration"
    result = False
    #robot.InitializeTerminal("Yoximo.xml")
    #robot.InitializeConnection("192.168.1.102", 23)
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
