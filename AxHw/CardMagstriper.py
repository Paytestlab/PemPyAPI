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


from UDPMessage.AxUDPCardMagstriperCommand import AxUDPCardMagstriperCommand
from Parsers.ParseXml import XmlParser
from Exception.Exception import Error
from Base.DeviceBase import DeviceBase;
from UDPMessage.UDPMagics import UDPMagics;

__author__ = "Matija Mazalin"
__email__ = "matija.mazalin@abrantix.com"
__license__ = "MIT"

class CardMagstriper(DeviceBase):
    """Thread safe card magstripe interface."""
    tag = "mag";
    magic = UDPMagics.CardMagstriperMagic;
    
    def __init__(self, id, mac_address, enable_statistics=False):
        super().__init__(id, XmlParser.parse_magstripes, enable_statistics);
        self.mac_address = bytearray.fromhex(mac_address);
   
    def send_command(self, action):
        Result = False;

        try:
            if(self.set_tracks(action)):
                send_to = self.device.get_sender_for_device(self.mac_address);
                Result = send_to.send_tracks();
           
            self.log_info("execution of {} was successful".format(action))
        except TimeoutError as e:
            self.log_error("device {} did not respond in time".format(self.get_mac_address()));
            Result = False;
            pass;
        except KeyError as e:
            Result = False;
        except AssertionError as e:
            self.log_error("device {} returned an error".format(self.get_mac_address()));
            Result = False;
        except:
            self.log_error("device {} returned a general error".format(self.get_mac_address()));
            Result = False;

        return Result;

    def set_tracks(self, action):
        Result = False;
        try:
            send_to = self.device.get_sender_for_device(self.mac_address);

            if(self.layout[action].Track1 is not None):
                track_value = self.layout[action].Track1;
                
                #special use case for track1. Reduce all characters for 0x20;
                track_byte_array = [(x - 0x20) for x in bytearray(str.encode(track_value))];

                track_bytes = bytes(track_byte_array);
                Result = send_to.set_card_magstripe_track(AxUDPCardMagstriperCommand.SetTrack1, track_bytes);

            if(self.layout[action].Track2 is not None):
                track_value = self.layout[action].Track2;
                track_bytes = str.encode(track_value);
                Result = send_to.set_card_magstripe_track(AxUDPCardMagstriperCommand.SetTrack2, track_bytes);

            if(self.layout[action].Track3 is not None):
                track_value = self.layout[action].Track3;
                track_bytes = str.encode(track_value);
                Result = send_to.set_card_magstripe_track(AxUDPCardMagstriperCommand.SetTrack3, track_bytes);

        except Error: 
            Result = False;

        return Result;

    def get_mac_address(self):
        return ''.join('{:02x}:'.format(x) for x in self.mac_address)[:-1];
