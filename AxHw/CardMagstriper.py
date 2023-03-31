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
from Message.CardMagstriperCommand import CardMagstriperCommand
from Parsers.ParseXml import XmlParser
from Exception.Exception import Error
from Base.DeviceBase import DeviceBase;
from Message.HardwareMagics import HardwareMagics;

__author__ = "Matija Mazalin"
__email__ = "matija.mazalin@abrantix.com"
__license__ = "MIT"

class CardMagstriper(DeviceBase):

    tag = "mag";
    magic = HardwareMagics.CardMagstriperMagic;
    
    def __init__(self, id, mac_address, enable_statistics=False):
        super().__init__(id, XmlParser.parse_magstripes, enable_statistics);
        self.mac_address = bytearray.fromhex(mac_address);
   
    def send_command(self, action):
        Result = False;

        try:
            if(self.do_action(action)):
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

    def do_action(self, action):
        if type(action) is dict:
            if action["action"] != "trackset":
                return False
            
            tracks = []
            for track in ["track1", "track2", "track3"]:
                track = action[track] if track in action else None
                tracks.append(track if track else None) # remove empty "" values

            return self.set_tracks(tracks)

        elif type(action) is str and action in self.layout:
            layout = self.layout[action]
            return self.set_tracks([layout.Track1, layout.Track2, layout.Track3])

        else:
            return False

    def set_tracks(self, layout):
        Result = False;
        track_pointers = [CardMagstriperCommand.SetTrack1, CardMagstriperCommand.SetTrack2, CardMagstriperCommand.SetTrack3]

        try:
            send_to = self.device.get_sender_for_device(self.mac_address);

            for track_pointer, track_value in zip(track_pointers, layout):
                if track_value is None:
                    continue

                track_bytes = str.encode(track_value)

                #special use case for track1. Reduce all characters for 0x20;
                if track_pointer is CardMagstriperCommand.SetTrack1:
                    track_bytes = bytes([(x - 0x20) for x in bytearray(track_bytes)])

                Result = send_to.set_card_magstripe_track(track_pointer, track_bytes)

        except Error: 
            Result = False;

        return Result;

    def get_mac_address(self):
        return ''.join('{:02x}:'.format(x) for x in self.mac_address)[:-1];
