#!/usr/bin/python3
from Configuration.BaseConfiguration import BaseConfiguration;

class RobotConfiguration(BaseConfiguration):
    def __init__(self, Id, Ip, Port, layout):
        super().__init__(Id, layout);
        self.IP = Ip
        self.Port = Port