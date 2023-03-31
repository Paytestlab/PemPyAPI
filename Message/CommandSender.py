#!/usr/bin/python3

from Message.UDP.UDPHelper import UDPHelper;
from Message.HardwareMessage import HardwareMessage;
from Message.Command import Command;
from Message.CardMultiplexerCommand import CardMultiplexerCommand;
from Message.CardMagstriperCommand import CardMagstriperCommand;

class CommandSender(object):
    """Send a specific command to the Device. The commands will be transmitted over UDP"""

    sender_helper  = object();
    
    def __init__(self, sender_helper, magic):
        self.sender_helper = sender_helper;
        self.magic = magic;

    def set_mac_address(self, mac_address):
        if(mac_address is None):
            raise AttributeError();

        request = HardwareMessage(self.magic);
        request.command = int(Command.SET_MAC_ADDRESS);
        request.data = mac_address;
        response = self.sender_helper.send_message(request.get_bytes());
        self.validate_response(request, response);

    def set_port(self, port_number):
        """
        Set port 1 - 16. 0 Disables all ports
        """

        if(port_number > 16):
            raise OverflowError();

        request = HardwareMessage(self.magic);
        request.command = int(CardMultiplexerCommand.SET_PORT);
        request.data = bytes([port_number]);
        response = self.sender_helper.send_message(request.get_bytes());
        return self.validate_response(request, response);

    def set_card_magstripe_track(self, command :  CardMagstriperCommand, track_data : bytes):

        request = HardwareMessage(self.magic);
        request.command = int(command);
        request.data = track_data;
        response = self.sender_helper.send_message(request.get_bytes());
        return self.validate_response(request, response);


    def send_tracks(self):
        request = HardwareMessage(self.magic);
        request.command = int(CardMagstriperCommand.SendTracks);
        response = self.sender_helper.send_message(request.get_bytes());
        return self.validate_response(request, response);


    def enable_or_disable_card_trace(self, enable):
        raise NotImplementedError();

    def get_port(self):
        raise NotImplementedError();

    def validate_response(self, request : HardwareMessage, response : HardwareMessage):
        if(response.command == int(Command.ERROR)):
            raise AssertionError("Error occured");

        if(response.command != request.command):
            raise AssertionError("Expected command: {}, got {}".format(request.command, response.command));

        return True;
