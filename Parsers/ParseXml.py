#!/usr/bin/python3

from xml.dom.minidom import parse
import xml.dom.minidom
import logging

class Terminal(object):

    def __init__(self, CanonicalName, Value, IsButton):
        self.CanonicalName = CanonicalName
        self.Value = Value
        self.IsButton = IsButton

class MultiplexerComand(object):

    def __init__(self, CanonicalName, Value):
        self.CanonicalName = CanonicalName
        self.Value = Value

class MagstripeComand(object):

    def __init__(self, CanonicalName, Brand, Track1, Track2, Track3):
        self.CanonicalName = CanonicalName
        self.Brand = Brand
        self.Track1 = Track1
        self.Track2 = Track2
        self.Track3 = Track3
        
class XmlParser(object):

    def str_to_bool(isButton):
        if (isButton is '1'):
            return True
        else:
            return False

    def parseXmlRobot(filename):
        try:
            logging.info("Robot: Parse: " + filename)
            DOMTree = xml.dom.minidom.parse(filename)
        except IOError as e:
            logging.error("Robot: Parsing Error: " + filename)
            return None
        
        collection = DOMTree.documentElement
        
        positions = collection.getElementsByTagName("Position")
        terminalList = {}
        for position in positions:
           Canonical = position.getElementsByTagName('CanonicalName')[0]
           Value = position.getElementsByTagName('Value')[0]
           isButton = False;
           if(0 < len(position.getElementsByTagName('isButton'))):
               IsButtonNode = position.getElementsByTagName('isButton')[0]
               isButton = XmlParser.str_to_bool(IsButtonNode.childNodes[0].data)
    
           terminal = Terminal(Canonical.childNodes[0].data, Value.childNodes[0].data, isButton)
           terminalList.update({Canonical.childNodes[0].data:terminal})

        return terminalList

    def parseXmlMultiplexer(filename):
        try:
            logging.info("Multiplexer: Parse: " + filename)
            DOMTree = xml.dom.minidom.parse(filename)
        except IOError as e:
            logging.error("Multiplexer: Parsing Error: " + filename)
            return None
        
        collection = DOMTree.documentElement
        
        positions = collection.getElementsByTagName("Position")
        terminalList = {}
        for position in positions:
           Canonical = position.getElementsByTagName('CanonicalName')[0]
           Value = position.getElementsByTagName('Value')[0]
           isButton = False;
           if(0 < len(position.getElementsByTagName('isButton'))):
               IsButtonNode = position.getElementsByTagName('isButton')[0]
               isButton = XmlParser.str_to_bool(IsButtonNode.childNodes[0].data)
    
           terminal = Terminal(Canonical.childNodes[0].data, Value.childNodes[0].data, isButton)
           terminalList.update({Canonical.childNodes[0].data:terminal})

        return terminalList

    def parseXmlMagstriper(XmlFilename):
        try:
            logging.info("Magstriper: Parse: " + XmlFilename)
            DOMTree = xml.dom.minidom.parse(XmlFilename)
        except IOError as e:
            logging.error("Magstriper: Parsing Error: " + XmlFilename)
            return None

        collection = DOMTree.documentElement

        comands = collection.getElementsByTagName("Command")
        comandList = {}
        for comand in comands:
           Canonical = comand.getElementsByTagName('CanonicalName')[0]
           Brand = comand.getElementsByTagName('Brand')[0]
           Track1 = comand.getElementsByTagName('Track1')[0]
           Track2 = comand.getElementsByTagName('Track2')[0]
           Track3 = comand.getElementsByTagName('Track3')[0]

           canonical_data = None;
           if Canonical.childNodes:
               canonical_data = Canonical.childNodes[0].data;

           brand_data = None;
           if Brand.childNodes:
               brand_data = Brand.childNodes[0].data;

           track1_data = None;
           if Track1.childNodes:
               track1_data = Track1.childNodes[0].data;

           track2_data = None;
           if Track2.childNodes:
               track2_data = Track2.childNodes[0].data;

           track3_data = None;
           if Track3.childNodes:
               track3_data = Track3.childNodes[0].data;

           magComand = MagstripeComand(canonical_data, brand_data, track1_data, track2_data, track3_data)
           comandList.update({Canonical.childNodes[0].data: magComand})

        return comandList
        
#def main():
#    terminalList = parseXml("Yomani.xml")
#    socket = PEMSocket("localhost", 3000)
#    if(socket.connect() is False):
#      return -1
    
#    socket.send("G0\r\n")
#    receive = socket.receive()
#    print("Recieved:" + receive.decode("utf-8"))

#main()
