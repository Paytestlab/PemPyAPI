#!/usr/bin/python3

from Message.Command import Command;
from Message.Base.BaseHelper import BaseHelper;
import socket;
import sys;
from Message.HardwareMessage import HardwareMessage;
from Message.UDP.Interfaces import Interfaces;
from AxHw.InfoMessage import InfoMessage;
import logging;
import traceback;

class UDPHelper(BaseHelper):
    """udp class for sending/receiving data"""
    
    PORT = 8005;
    TIMEOUT = 2.0;

    target_ip = "";
    iface = "";
    sock = None;

    def __init__(self, target, iface, magic):
        self.target_ip = target
        self.iface = iface
        self.magic = magic

    def send_message(self, message):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.bind((Interfaces.get_local_ip_from_interface(self.iface), 0));
                sock.sendto(message, self.target_ip);
                sock.settimeout(UDPHelper.TIMEOUT);
                (data, server) = sock.recvfrom(10100);

        except socket.timeout:
            logging.warning('no answer received from the endpoint {}'.format(self.target_ip));
            raise TimeoutError('no answer received from the endpoint {}'.format(self.target_ip))
            pass;
        except Exception as e :
            logging.warning('got an exception in the discovery mechanism...');
            traceback.print_exc()
            raise e;

        return HardwareMessage.parse(self.magic, data);

    def receive(self):
        #TODO
        data, server = sock.recvfrom(UDPHelper.TIMEOUT);

   

#a = UDPHelper("10.30.10.88");
#UDPHelper.send_broadcast();
