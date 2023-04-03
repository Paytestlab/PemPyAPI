from Message.Command import Command;
import socket;
from Message.HardwareMessage import HardwareMessage;
from Message.UDP.Interfaces import Interfaces;
from AxHw.InfoMessage import InfoMessage;
from Message.UDP.UDPHelper import UDPHelper;
import logging;
import traceback;

class UDPBroadcast(object):
    
    @staticmethod
    def fill_devices(magic):
        return UDPBroadcast.send_broadcast(magic);

    @staticmethod
    def get_info_message_by_broadcast(mac_address, magic):
        info_messages = UDPBroadcast.send_broadcast(magic);

        for message in info_messages:
            if(bytearray(message.MacAddress) == mac_address):
                return message;
        return None;

    @staticmethod
    def __parse_message(iface, magic, responses, buffer, address):
        msg = HardwareMessage.parse(magic, buffer);
        info = InfoMessage();
        info.MacAddress = msg.data[2:8];
        info.RemoteIpAddress = address;
        info.Major = msg.data[0];
        info.Minor = msg.data[1];
        info.iface = iface;
        info.magic = magic;
        logging.debug('received ip:{} from mac:{}'.format(info.RemoteIpAddress, ''.join('{:02x}:'.format(x) for x in info.MacAddress)[:-1]));
        responses.append(info);

    @staticmethod
    def __transmit_message(s, bytes_array, dest, iface, magic, responses):
        try:
            respondingDevices = 0;
            s.bind((Interfaces.get_local_ip_from_interface(iface), 0));
            s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1);
            logging.debug('broadcasting to {}'.format(dest));
            s.sendto(bytes_array, dest);
            
            s.settimeout(UDPHelper.TIMEOUT);
            while True:
                (buf, addr) = s.recvfrom(10100)
                if(len(buf)):
                    UDPHelper.__parse_message(iface, magic, responses, buf, addr);
                    respondingDevices +=1;

        except socket.timeout:
            if(respondingDevices == 0):
                logging.debug('no answer received from any endpoint in the broadcast {}'.format(dest));
            pass;
        except TimeoutError:
            logging.debug('no answer received');
            pass;
        except Exception as e :
            logging.warning('got an exception in the discovery mechanism...');
            traceback.print_exc()
            pass;

    @staticmethod
    def send_broadcast(magic):
        responses = [];
        udp_message = HardwareMessage(magic);
        udp_message.command = int(Command.INFO);
        bytes_array = udp_message.get_bytes();
        
        for iface in Interfaces.get_all_network_interfaces_with_broadcast():
            destIP = Interfaces.get_broadcast_address(iface);

            if(destIP is None):
                continue;

            dest = (destIP, UDPHelper.PORT);
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                UDPBroadcast.__transmit_message(s, bytes_array, dest, iface, magic, responses);
            
        return responses;