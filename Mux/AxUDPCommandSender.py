from Mux.UDPHelper import UDPHelper;
from Mux.AxUDPMessage import AxUDPMessage;
from Mux.AxUDPCommand import AxUDPCommand;

class AxUDPCommandSender(object):
    """Send a specific command to the Device. The commands will be transmitted over UDP"""

    udp_helper  = object();
    def __init__(self, ip_address, iface):
        self.udp_helper = UDPHelper(ip_address, iface);
        

    def set_mac_address(self, mac_address):
        if(mac_address is None):
            raise AttributeError();

        request = AxUDPMessage();
        request.command = int(AxUDPCommand.SET_MAC_ADDRESS);
        request.data = mac_address;
        response = self.udp_helper.send_message(request);
        self.validate_response(request, response);


    def set_port(self, port_number):
        """
        Set port 1 - 16. 0 Disables all ports
        """

        if(port_number > 16):
            raise OverflowError();

        request = AxUDPMessage();
        request.command = int(AxUDPCommand.SET_PORT);
        request.data = bytes([port_number]);
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
