#!/usr/bin/python3

from Message.CommandSender import CommandSender;
from Message.UDP.UDPBroadcast import UDPBroadcast;
from Message.UDP.UDPHelper import UDPHelper;
from Message.Serial.SerialHelper import SerialHelper;
from Message.Serial.SerialBroadcast import SerialBroadcast;

class CommandSenderManager(object):
    """Manages all \ref AxUDPCommandSender"""

    #Always just one
    CommandSenders = {};

    def __init__(self, magic):
        self.magic = magic;
        pass;    

    def get_sender_for_device(self, mac_address):
        return CommandSenderManager.CommandSenders[bytes(mac_address)];

    def __device_add_serial(self, mac_address):
        messages = SerialBroadcast.fill_devices(self.magic);
        for info in messages:
            self.add_or_update_device_serial(info.port, info.MacAddress);
        if(self.device_exists(mac_address)):
            return True;
        else:
            return False;

    def __device_add_broadcast(self, mac_address):
        messages = UDPBroadcast.fill_devices(self.magic);
        for info in messages:
            self.add_or_update_device_address(info.RemoteIpAddress, info.MacAddress, info.iface);
        if(self.device_exists(mac_address)):
            return True;
        else:
            return False;

    def device_lookup(self, mac_address):
        if(self.device_exists(mac_address)):
            return True;
        elif(False is self.__device_add_broadcast(mac_address)):
            return self.__device_add_serial(mac_address);
                 
    def device_exists(self, mac_address):
        return bytes(mac_address) in CommandSenderManager.CommandSenders;

    def add_or_update_device_serial(self, port, mac_address):
        if(self.device_exists(mac_address)):
            CommandSenderManager.CommandSenders[bytes(mac_address)].sender_helper.port = port;
        else:
            CommandSenderManager.CommandSenders[bytes(mac_address)] = CommandSender(SerialHelper(port, self.magic), self.magic);
        
    def add_or_update_device_address(self, remote_ip_address, mac_address, iface):
        if(self.device_exists(mac_address)):
            CommandSenderManager.CommandSenders[bytes(mac_address)].sender_helper.target_ip = remote_ip_address;
        else:
            
            CommandSenderManager.CommandSenders[bytes(mac_address)] = CommandSender(UDPHelper(remote_ip_address, iface, self.magic), self.magic);
