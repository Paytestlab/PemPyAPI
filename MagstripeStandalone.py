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

from os.path import join;
from Exception.Exception import Error, ConnectionError, InputError, ParseError, DestinationNotFoundError, DeviceStateError;
import json;
import re
import argparse;
import logging;
import traceback;
from AxHw.CardMagstriper import CardMagstriper;
from Configuration.MagConfiguration import MagConfiguration
from Base.DeviceBase import DeviceBase;

#----------------------------------------------------------------------------------------------------------------#

__major__ = 1
__minor__ = 0
__service__ = 0
__build__ = 52
__path = "ConfigRest"

__intro__= (
    "AX magstripe Integration Layer\n"
    "Version {}.{}.{}.{}\n" 
    "Copyright (C) {} - {} Abrantix AG\n"
    "{}".format(__major__, __minor__, __service__, __build__, 2015, 2023, "#" * 50)
    )

#----------------------------------------------------------------------------------------------------------------#

def main():

    args = EnableAndParseArguments()
  
    config = args.config

    SetLoggingLevel(args)

    print(__intro__)

    print("Initialising...")

    try:
        mag_configuration = MagConfiguration(id, args.mac_address, "CardMagstriper.xml", None)

        device_list = {}
        error = 0

        mag = CardMagstriper("mag", mag_configuration.mac_address, False)
        if(False is initialize_mux("mag", mag, mag_configuration)):
            raise InterruptedError("mag initialization failed")

        device_list.update({"mag": mag})

        if(not device_list):
            logging.critical("general: fatal error, device list is empty!");
            raise Error("", "Fatal error, device list is empty!");

        logging.info("general: initialization success! warnings: {}".format(error))

        executeCommands(mag, args.command, "mag");

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
    parser.add_argument("-v", "--verbose", nargs='?', const=True, default=False, help="increase trace verbosity to the INFO level", required=False)
    parser.add_argument("-d", "--debug", nargs='?', const=True, default=False, help="increase trace verbosity to the DEBUG level", required=False)
    parser.add_argument("-m", "--mac_address", nargs='?', const=True, help="mac address of the robot", required=True)                 
    parser.add_argument("-cmd", "--command", nargs='?', const=True, help="conanical command, out of Magstriper.xml", required=False)
 
    return parser.parse_args()

#------------------------------------------------------------------------------------------------------------------------#

def initialize_mux(key, mux : DeviceBase, configuration):
    if(False is mux.device_lookup()):
        return False;

    if(False is mux.initialize_device(join(__path, configuration.Layout))):
        return False;

    return True;

def executeCommands(device : DeviceBase, command, key):
    try:
        device.mutex.acquire()

        if(False is device.connect()):
            device.log_error("device is unreachable")
            raise ConnectionError("", "could not connect to the device: " + key)
        
        if(True is device.send_command(command)):
            device.UpdateTable(command)
        else:
            device.log_warning("device could not execute '{}'. Abort further execution".format(command))
            raise InputError("", "{}: could not execute: {}".format(key, command))

    finally:
        device.close_connection()
        device.mutex.release()

main()