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

"""Thread safe card multiplexer interface."""
__author__ = "Matija Mazalin"
__email__ = "matija.mazalin@abrantix.com"
__license__ = "MIT"


from Parsers.ParseXml import XmlParser
import threading
import SQL.Statistics
import logging
from UDPMessage.AxUDPCommandSender import AxUDPCommandSender;
from UDPMessage.AxUDPCommandSenderManager import AxUDPCommandSenderManager;
from Exception.Exception import Error
from Base.DeviceBase import DeviceBase;
from UDPMessage.UDPMagics import UDPMagics;
import traceback;


class CardMultiplexer(DeviceBase):

    def __init__(self, mac_address, enable_statistics=False):
        DeviceBase.__init__(self, enable_statistics);
        self.mac_address = bytearray.fromhex(mac_address);

    def device_lookup(self):
        self.device = AxUDPCommandSenderManager(UDPMagics.CardMultiplexerMagic);
        deviceIsPresent = self.device.device_lookup(self.mac_address);
        if deviceIsPresent:
            logging.info("multiplexer ({}) is present".format(self.mac_address))
        else:
            logging.warning("multiplexer ({}) is not present".format(self.mac_address))

        return deviceIsPresent

    def initialize_device(self, filename):
        self.mux_layout = XmlParser.parseXmlMultiplexer(filename)
        if(self.mux_layout is None):
            logging.warning("multiplexer initialization failed, skip...")
            return False;

        logging.info("multiplexer initialization successful...")

    def send_command(self, action):
        Result = False
        try:
           action_value = int(self.mux_layout[action].Value);
           send_to = self.device.get_sender_for_device(self.mac_address);
           Result = send_to.set_port(action_value);
        
        except TimeoutError as e:
            logging.error("The remote host did not respond in time");
        except KeyError as e:
            pass;
        except AssertionError as e:
            logging.error("Remote host returned an error");
        except:
            traceback.print_exc()
            logging.error("general error");

        return Result;

        





