from PinRobot import PinRobot
from RestfulThreaded import RESTfulThreadedServer
from os.path import join
from ParseXmlRobotConfiguration import ParseXmlRobotConfiguration, RobotConfiguration
import json


def main():
    global robot
    robot = PinRobot()
    _path = "ConfigRest"
    result = False




    try:
        ConfigurationList = ParseXmlRobotConfiguration.parseXml(join("Assets", "EntryConfiguration.xml"))
        RobotList = {}

        for key, value in ConfigurationList.items():
             robot = PinRobot()
             if(False is robot.InitializeTerminal(join(_path, value.Layout))):
                raise

             if(False is robot.InitializeConnection(value.IP, int(value.Port))):
                raise

             RobotList.update({key:robot})

        server = RESTfulThreadedServer(doPostWork, RobotList)
        server.start()
        server.waitForThread()
    except (InputError,ConnectionError,ParseError):
        pass

def doPostWork(jsonString, robotList):
    j = json.loads(jsonString)
        
    for command in j["commands"]:
        if(True is robotList[j['id']].SendCommand(command)):
            print(j['id'] + ": execution of " + command + " was succesful")
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
