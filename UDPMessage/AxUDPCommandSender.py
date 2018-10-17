#!/usr/bin/python3

from UDPMessage.UDPHelper import UDPHelper;
from UDPMessage.AxUDPMessage import AxUDPMessage;
from UDPMessage.AxUDPCommand import AxUDPCommand;
from UDPMessage.AxUDPCardMultiplexerCommand import AxUDPCardMultiplexerCommand;
from UDPMessage.AxUDPCardMagstriperCommand import AxUDPCardMagstriperCommand;
from UDPMessage.UDPMagics import UDPMagics;

class AxUDPCommandSender(object):
    """Send a specific command to the Device. The commands will be transmitted over UDP"""

    udp_helper  = object();
    
    def __init__(self, ip_address, iface, magic):
        self.udp_helper = UDPHelper(ip_address, iface, magic);
        self.magic = magic;

    def set_mac_address(self, mac_address):
        if(mac_address is None):
            raise AttributeError();

        request = AxUDPMessage(self.magic);
        request.command = int(AxUDPCommand.SET_MAC_ADDRESS);
        request.data = mac_address;
        response = self.udp_helper.send_message(request.get_bytes());
        self.validate_response(request, response);

    def set_port(self, port_number):
        """
        Set port 1 - 16. 0 Disables all ports
        """

        if(port_number > 16):
            raise OverflowError();

        request = AxUDPMessage(self.magic);
        request.command = int(AxUDPCardMultiplexerCommand.SET_PORT);
        request.data = bytes([port_number]);
        response = self.udp_helper.send_message(request.get_bytes());
        return self.validate_response(request, response);

    def set_card_magstripe_track(self, command :  AxUDPCardMagstriperCommand, track_data : bytes):

        request = AxUDPMessage(self.magic);
        request.command = int(command);
        request.data = track_data;
        response = self.udp_helper.send_message(request.get_bytes());
        return self.validate_response(request, response);


    def send_tracks(self):
        request = AxUDPMessage(self.magic);
        request.command = int(AxUDPCardMagstriperCommand.SendTracks);
        response = self.udp_helper.send_message(request.get_bytes());
        return self.validate_response(request, response);


    def enable_or_disable_card_trace(self, enable):
        raise NotImplementedError();

    def get_port(self):
        raise NotImplementedError();

    def validate_response(self, request : AxUDPMessage, response : AxUDPMessage):
        if(response.command == int(AxUDPCommand.ERROR)):
            raise AssertionError("Error occured");

        if(response.command != request.command):
            raise AssertionError("Expected command: {}, got {}".format(request.command, response.command));

        return True;
