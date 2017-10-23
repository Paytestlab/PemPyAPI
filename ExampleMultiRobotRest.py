from PinRobot import PinRobot
from RestfulThreaded import RESTfulThreadedServer
from os.path import join
from ParseXmlRobotConfiguration import ParseXmlRobotConfiguration, RobotConfiguration
from Exception import Error, ConnectionError, InputError, ParseError
import json
import argparse


def main():
    global robot
    robot = PinRobot()
    _path = "ConfigRest"
    result = False

    parser = argparse.ArgumentParser(description='PIN Robot Rest API')
    parser.add_argument('-config','-configfile", help="path to entry configuration xml',required=False)
    args = (parser.parse_args())

    if(None is args.config):
        config = join("Assets", "EntryConfiguration.xml")
    else:
        config = args.config

    try:
        ConfigurationList = ParseXmlRobotConfiguration.parseXml(config)
        RobotList = {}

        for key, value in ConfigurationList.items():
             robot = PinRobot()
             if(False is robot.InitializeTerminal(join(_path, value.Layout))):
                print(value.Layout + ": Initialization failed, skip...")
                continue

             if(False is robot.InitializeConnection(value.IP, int(value.Port))):
                print(value.Layout + ": robot not reachable, skip...")
                continue

             RobotList.update({key:robot})

        if(not RobotList):
            print(" Fatal error, robot list is empty...")
            raise

        server = RESTfulThreadedServer(doPostWork, doGetWork, RobotList)
        server.start()
        server.waitForThread()
    except (Error):
        pass
    except:
        pass
   

def doPostWork(jsonString, robotList):
    j = json.loads(jsonString)
        
    for command in j["commands"]:
        if(True is robotList[j['id']].SendCommand(command)):
            print(j['id'] + ": execution of " + command + " was succesful")
        else:
            raise InputError
        
def doGetWork(robotList):
    l = list(robotList.keys())
    robot_object = {'id' : l}
    return json.dumps(robot_object)

main()
