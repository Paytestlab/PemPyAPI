#!/usr/bin/python3

from Configuration.BaseConfiguration import BaseConfiguration;

class CtlMuxConfiguration(BaseConfiguration):
    def __init__(self, Id, mac_address, layout):
        super().__init__(Id, layout);
        self.mac_address = mac_address