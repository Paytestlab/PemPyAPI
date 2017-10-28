# Copyright (c) 2017 Matija Mazalin
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""Thread safe robot interface."""

__author__ = "Matija Mazalin"
__email__ = "matija.mazalin@abrantix.com"
__license__ = "MIT"

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
