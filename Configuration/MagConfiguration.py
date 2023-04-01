#!/usr/bin/python3

from Configuration.BaseConfiguration import BaseConfiguration;

class MagConfiguration(BaseConfiguration):

    def __init__(self, Id, mac_address, layout, serial_port):
        super().__init__(Id, layout);
        self.mac_address = mac_address
        self.port = serial_port
