#!/usr/bin/python3

from xml.dom.minidom import parse
import xml.dom.minidom
import logging


class BaseCommand(object):
    def __init__(self, CanonicalName, Value = None):
        self.CanonicalName = CanonicalName;
        self.Value = Value;

class RobotCommand(BaseCommand):
    def __init__(self, CanonicalName, Value, IsButton):
        super().__init__(CanonicalName, Value);
        self.IsButton = IsButton

class MultiplexerCommand(BaseCommand):
    def __init__(self, CanonicalName, Value):
        super().__init__(CanonicalName, Value);

class MagstripeCommand(BaseCommand):
    def __init__(self, CanonicalName, Brand, Track1, Track2, Track3):
        super().__init__(CanonicalName);
        self.Brand = Brand
        self.Track1 = Track1
        self.Track2 = Track2
        self.Track3 = Track3
                
#def main():
#    terminalList = parseXml("Yomani.xml")
#    socket = PEMSocket("localhost", 3000)
#    if(socket.connect() is False):
#      return -1
    
#    socket.send("G0\r\n")
#    receive = socket.receive()
#    print("Recieved:" + receive.decode("utf-8"))

#main()
