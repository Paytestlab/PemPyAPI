from Mux.AxUDPCommandSender import AxUDPCommandSender;
from Mux.UDPHelper import UDPHelper;

class AxUDPCommandSenderManager(object):
    """Manages all \ref AxUDPCommandSender"""

    AxUDPCommandSenders = {};

    def __init__(self):
        pass;    

    def get_sender_for_device(self, mac_address):
        return self.AxUDPCommandSenders[bytes(mac_address)];

    def device_lookup(self, mac_address):
        if(self.device_exists(mac_address)):
            return True;
        else:
            info_message = UDPHelper.get_info_message_by_broadcast(mac_address);
            if(None is not info_message):
                self.add_or_update_device_address(info_message.RemoteIpAddress, mac_address, info_message.iface);
                return True;
            else:
                return False;
    
    def device_exists(self, mac_address):
        return bytes(mac_address) in self.AxUDPCommandSenders;


    def add_or_update_device_address(self, remote_ip_address, mac_address, iface):
        if(self.device_exists(mac_address)):
            self.AxUDPCommandSenders[bytes(mac_address)].UdpHelper.Target = remote_ip_address;
        else:
            self.AxUDPCommandSenders[bytes(mac_address)] = AxUDPCommandSender(remote_ip_address, iface);


    


