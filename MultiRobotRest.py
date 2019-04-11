#!/usr/bin/python3

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

from Robot.PinRobot import PinRobot;
from Rest.RestfulThreaded import RESTfulThreadedServer;
from os.path import join;
from Parsers.ParseXmlRobotConfiguration import ParseXmlRobotConfiguration, RobotConfiguration;
from Exception.Exception import Error, ConnectionError, InputError, ParseError, DestinationNotFoundError, DeviceStateError;
import json;
import argparse;
from SQL.Statistics import Statistics;
import logging;
import traceback;
from AxHw.CardMultiplexer import CardMultiplexer;
from AxHw.CardMagstriper import CardMagstriper;
from AxHw.CtlMultiplexer import CtlMultiplexer;
from Base.DeviceBase import DeviceBase;

#----------------------------------------------------------------------------------------------------------------#

__major__ = 1
__minor__ = 5
__service__ = 0
__build__ = 51
__path = "ConfigRest"

__intro__= (
    "AX Robot Integration Layer\n"
    "Version {}.{}.{}.{}\n" 
    "Copyright (C) {} - {} Abrantix AG\n"
    "{}".format(__major__, __minor__, __service__, __build__, 2015, 2018, "#" * 50)
    )

#----------------------------------------------------------------------------------------------------------------#

def main():

    args = EnableAndParseArguments()
  
    config = args.config
    port = int(args.port)
        
    enable_statistics=args.enable_statistics
    empower = args.empower_card

    SetLoggingLevel(args)

    print(__intro__)

    print("Initialising...")

    try:
        (robot_conf_list, mux_conf_list, mag_conf_list, ctl_mux_conf_list) = ParseXmlRobotConfiguration.parseXml(config)

        device_list = {}
        error = 0

        for key, robotConfiguration in robot_conf_list.items():
             try:
                robot = PinRobot(key, enable_statistics, empower)

                if(False is initialize_robot(key, robot, robotConfiguration)):
                    error += 1
                    continue

                device_list.update({key: robot})
             except DeviceStateError:
                pass;


        for key, mux_configuration in mux_conf_list.items():
            mux = CardMultiplexer(key, mux_configuration.mac_address, enable_statistics)

            if(False is initialize_mux(key, mux, mux_configuration)):
                error += 1
                continue

            device_list.update({key: mux})

        for key, mag_configuration in mag_conf_list.items():
            mag = CardMagstriper(key, mag_configuration.mac_address, enable_statistics)

            if(False is initialize_mux(key, mag, mag_configuration)):
                error += 1
                continue

            device_list.update({key: mag})

        for key, ctl_mux_configuration in ctl_mux_conf_list.items():
           ctl_mux = CtlMultiplexer(key, ctl_mux_configuration.mac_address, enable_statistics)
           
           if(False is initialize_mux(key, ctl_mux, ctl_mux_configuration)):
                error += 1
                continue

           device_list.update({key: ctl_mux})

        if(not device_list):
            logging.critical("general: fatal error, device list is empty!");
            raise Error("", "Fatal error, device list is empty!");

        logging.info("general: initialization success! warnings: {}".format(error))

        start_rest_server(doPostWork, doGetWork, device_list, port)

    except Error as e:
        traceback.print_exc()

#---------------------------------------------------------------------------------------------------------------#

def SetLoggingLevel(args):
    FORMAT = "%(asctime)-15s %(levelname)s: %(message)s"

    if(args.debug):
        logging.basicConfig(format=FORMAT, level=logging.DEBUG)
    elif(args.verbose):
        logging.basicConfig(format=FORMAT, level=logging.INFO)
    else:
        logging.basicConfig(format=FORMAT, level=logging.WARNING)

#------------------------------------------------------------------------------------------------------------------------#

def EnableAndParseArguments():
    parser = argparse.ArgumentParser(description="AX Robot Integration Layer v{}.{}.{}".format(__major__, __minor__, __service__))
    parser.add_argument("-c", "--config", default=join("Assets", "EntryConfiguration.xml"), help="path to entry configuration xml", required=False)
    parser.add_argument("-p", "--port", default='8000', help="port for the http listener, default is 8000", required=False)
    parser.add_argument("--enable-statistics", nargs='?', const=True, default=False, help="enable tracking of the button press to the local DB", required=False)
    parser.add_argument("-v", "--verbose", nargs='?', const=True, default=False, help="increase trace verbosity to the INFO level", required=False)
    parser.add_argument("-d", "--debug", nargs='?', const=True, default=False, help="increase trace verbosity to the DEBUG level", required=False)
    parser.add_argument("--empower-card", nargs='?', const=True, default=False, help="increase the current on the card for the terminals with tighter card reader", required=False)

    return parser.parse_args()

#------------------------------------------------------------------------------------------------------------------------#

def initialize_mux(key, mux : DeviceBase, configuration):
    if(False is mux.device_lookup()):
        return False;

    if(False is mux.initialize_device(join(__path, configuration.Layout))):
        return False;

    return True;

#---------------------------------------------------------------------------------------------------------------#

def initialize_robot(key, robot : PinRobot, configuration):
    """Initializes the robot, and perfoms home"""
    try:
        if(False is robot.initialize_device(join(__path, configuration.Layout))):
            robot.log_warning("Initialization of robot failed, skip...");
            return False

        if(False is robot.initialize_connection(configuration.IP, int(configuration.Port))):
            robot.log_warning("robot not reachable, skip...");
            return False

        if (False is robot.home()):
            robot.log_warning("robot calibration could not be executed");
            return False;

        if (False is robot.remove_card()):
            robot.log_warning("card could not be removed");
            return False;


    finally:
        robot.close_connection()

    return True

#---------------------------------------------------------------------------------------------------------------#

def start_rest_server(postWork, getWork, robotList, port):
    server = RESTfulThreadedServer(postWork, getWork, robotList, port)
    server.start()
    server.waitForThread()

#---------------------------------------------------------------------------------------------------------------#

def executeCommands(device : DeviceBase, commands, key):
    """
    Execute a request, protected by a lock. Every request on a single robot 
    must be processed till the end before the next may be processed
    """
    try:
        device.mutex.acquire()

        if(False is device.connect()):
            device.log_error("device is unreachable")
            raise ConnectionError("", "could not connect to the device: " + key)

        for command in commands:
            if(True is device.send_command(command)):
                device.UpdateTable(command)
            else:
                device.log_warning("device could not execute '{}'. Abort further execution".format(command))
                raise InputError("", key + ": could not execute: " + command)

    finally:
        device.close_connection()
        device.mutex.release()

#-----------------------------------------------------------------------------------------------------------------#

def getRequest(jsonString):
    try:
        request = json.loads(jsonString)
    except json.JSONDecodeError:
        logging.error("json could not be loaded:\n" + jsonString)
        raise ParseError("", "json could not be parsed")

    return request

#----------------------------------------------------------------------------------------------------------------#   

def doPostWork(jsonString, robotList):
    
    request = getRequest(jsonString)
    try:
        key = request['id']

        if(key not in robotList):
            logging.error("robot {} not in list".format(key))
            raise DestinationNotFoundError("" , key + ": robot not found")

        executeCommands(robotList[key], request['commands'], key)
    except KeyError as e:
        raise ParseError("", str(e));
    return True

#----------------------------------------------------------------------------------------------------------------#
        
def doGetWork(robotList):
    l = list(robotList.keys())
    robot_object = {'id' : l}
    return json.dumps(robot_object)

#----------------------------------------------------------------------------------------------------------------#

main()
