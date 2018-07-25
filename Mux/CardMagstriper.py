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

"""Thread safe card magstripe interface."""
__author__ = "Matija Mazalin"
__email__ = "matija.mazalin@abrantix.com"
__license__ = "MIT"


from ParseXml import XmlParser
import threading
import Statistics
import logging
from Mux.AxUDPCommandSender import AxUDPCommandSender;
from Mux.AxUDPCommandSenderManager import AxUDPCommandSenderManager;
from ParseXml import XmlParser;
from Exception import Error
from DeviceBase import DeviceBase;
from Mux.UDPMagics import UDPMagics;

class CardMagstriper(DeviceBase):

    def __init__(self, mac_address, enable_statistics=False):
        DeviceBase.__init__(self,enable_statistics);
        self.mac_address = bytearray.fromhex(mac_address);

    def device_lookup(self):
        self.device = AxUDPCommandSenderManager();
        return self.device.device_lookup(self.mac_address, UDPMagics.CardMagstriperMagic);

    def initialize_device(self, file_name):
        self.mag_layout = XmlParser.parseXmlMagstriper(file_name)
        if(self.mag_layout is None):
            return False;

        return True;

    def send_command(self, action):
        Result = False;

        try:
           action_value = int(self.mag_layout[action].Value);
           send_to = self.device.get_sender_for_device(self.mac_address);
           Result = send_to.set_port(action_value);
        except KeyError as e:
            Result = False;
        except AssertionError as e:
            logging.ERROR("Remote host returned an error");
            Result = False;
        except:
            logging.ERROR("general error");
            Result = False;

        return Result;
