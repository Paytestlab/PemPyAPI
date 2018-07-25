#!/usr/bin/python3

from Mux.AxUDPCommandSender import AxUDPCommandSender;
from Mux.UDPHelper import UDPHelper;

class AxUDPCommandSenderManager(object):
    """Manages all \ref AxUDPCommandSender"""

    #Always just one
    AxUDPCommandSenders = {};

    def __init__(self):
        pass;    

    def get_sender_for_device(self, mac_address):
        return AxUDPCommandSenderManager.AxUDPCommandSenders[bytes(mac_address)];

    def device_lookup(self, mac_address, magic):
        if(self.device_exists(mac_address)):
            return True;
        else:
            messages = UDPHelper.fill_devices(magic);

            for info in messages:
                self.add_or_update_device_address(info.RemoteIpAddress, info.MacAddress, info.iface, info.magic);

            if(self.device_exists(mac_address)):
                return True;
            else:
                return False;

    def device_exists(self, mac_address):
        return bytes(mac_address) in AxUDPCommandSenderManager.AxUDPCommandSenders;

    def add_or_update_device_address(self, remote_ip_address, mac_address, iface, magic):
        if(self.device_exists(mac_address)):
            AxUDPCommandSenderManager.AxUDPCommandSenders[bytes(mac_address)].UdpHelper.Target = remote_ip_address;
        else:
            AxUDPCommandSenderManager.AxUDPCommandSenders[bytes(mac_address)] = AxUDPCommandSender(remote_ip_address, iface, magic);
