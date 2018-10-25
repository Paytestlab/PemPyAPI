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
from UDPMessage.AxUDPCardMagstriperCommand import AxUDPCardMagstriperCommand
from Parsers.ParseXml import XmlParser
import threading
import SQL.Statistics
import logging
from UDPMessage.AxUDPCommandSender import AxUDPCommandSender;
from UDPMessage.AxUDPCommandSenderManager import AxUDPCommandSenderManager;
from Exception.Exception import Error
from Base.DeviceBase import DeviceBase;
from UDPMessage.UDPMagics import UDPMagics;

__author__ = "Matija Mazalin"
__email__ = "matija.mazalin@abrantix.com"
__license__ = "MIT"

class CardMagstriper(DeviceBase):

    def __init__(self, mac_address, enable_statistics=False):
        DeviceBase.__init__(self,enable_statistics);
        self.mac_address = bytearray.fromhex(mac_address);

    def device_lookup(self):
        self.device = AxUDPCommandSenderManager(UDPMagics.CardMagstriperMagic);
        deviceIsPresent = self.device.device_lookup(self.mac_address)
        if deviceIsPresent:
            logging.info("CardMagstriper ({}) is present".format(', '.join(hex(x) for x in self.mac_address)))
        else:
            logging.warning("CardMagstriper ({}) is not present".format(', '.join(hex(x) for x in self.mac_address)))

        return deviceIsPresent

    def initialize_device(self, filename):
        self.mag_layout = XmlParser.parseXmlMagstriper(filename)
        if(self.mag_layout is None):
            logging.warning("Initialization of magstriper failed, skip...")
            return False;

        logging.info("Initialization of magstriper successful...")
        return True;

    def send_command(self, action):
        Result = False;

        try:
            if(self.set_tracks(action)):
                send_to = self.device.get_sender_for_device(self.mac_address);
                Result = send_to.send_tracks();
           

        except TimeoutError as e:
            logging.error("The remote host did not respond in time");
            Result = False;
            pass;
        except KeyError as e:
            Result = False;
        except AssertionError as e:
            logging.error("Remote host returned an error");
            Result = False;
        except:
            logging.error("general error");
            Result = False;

        return Result;


    def set_tracks(self, action):
        Result = False;
        try:
            send_to = self.device.get_sender_for_device(self.mac_address);

            if(self.mag_layout[action].Track1 is not None):
                track_value = self.mag_layout[action].Track1;
                track_bytes = str.encode(track_value);
                for char in track_bytes:
                    char = char - 0x20;
                Result = send_to.set_card_magstripe_track(AxUDPCardMagstriperCommand.SetTrack1, track_bytes);

            if(self.mag_layout[action].Track2 is not None):
                track_value = self.mag_layout[action].Track2;
                track_bytes = str.encode(track_value);
                Result = send_to.set_card_magstripe_track(AxUDPCardMagstriperCommand.SetTrack2, track_bytes);

            if(self.mag_layout[action].Track3 is not None):
                track_value = self.mag_layout[action].Track3;
                track_bytes = str.encode(track_value);
                Result = send_to.set_card_magstripe_track(AxUDPCardMagstriperCommand.SetTrack3, track_bytes);

        except Error: 
            Result = False;

        return Result;
