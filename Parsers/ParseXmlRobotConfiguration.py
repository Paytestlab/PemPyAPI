#!/usr/bin/python3

from xml.dom.minidom import parse
import xml.dom.minidom
import logging

class RobotConfiguration(object):

    def __init__(self, Id, Ip, Port, layout):
        self.Id = Id
        self.IP = Ip
        self.Port = Port
        self.Layout = layout

class MuxConfiguration(object):

    def __init__(self, Id, mac_address, layout):
        self.Id = Id
        self.mac_address = mac_address
        self.Layout = layout

class MagConfiguration(object):

    def __init__(self, Id, mac_address, layout):
        self.Id = Id
        self.mac_address = mac_address
        self.Layout = layout

class ParseXmlRobotConfiguration(object):

    def parseXml(XmlFilename):
        try:
            logging.info("Configuration: Parse: " + XmlFilename)
            DOMTree = xml.dom.minidom.parse(XmlFilename)
        except IOError as e:
            logging.error("Configuration: Parsing Error: " + XmlFilename)
            return None
        
        collection = DOMTree.documentElement

        robots = collection.getElementsByTagName("Robot")
        robot_list = {}
        for robot in robots:
           id = robot.getAttribute('id')
           Ip = robot.getElementsByTagName('IpAddress')[0]
           IpPort = robot.getElementsByTagName('IpPort')[0]
           Layout = robot.getElementsByTagName('Layout')[0]
           robot_configuration = RobotConfiguration(id, Ip.childNodes[0].data, IpPort.childNodes[0].data, Layout.childNodes[0].data)
           robot_list.update({id:robot_configuration})

        muxs = collection.getElementsByTagName("CardMultiplexer")
        mux_list = {}
        for mux in muxs:
            id = mux.getAttribute('id')
            mac_address = mux.getElementsByTagName('MacAddress')[0]
            Layout = mux.getElementsByTagName('Layout')[0]
            mux_configuration = MuxConfiguration(id, mac_address.childNodes[0].data, Layout.childNodes[0].data)
            mux_list.update({id:mux_configuration})

        mags = collection.getElementsByTagName("CardMagstriper")
        mag_list = {}
        for mag in mags:
            id = mag.getAttribute('id')
            mac_address = mag.getElementsByTagName('MacAddress')[0]
            Layout = mag.getElementsByTagName('Layout')[0]
            mag_configuration = MagConfiguration(id, mac_address.childNodes[0].data, Layout.childNodes[0].data)
            mag_list.update({id:mag_configuration})

        return (robot_list, mux_list, mag_list)

#def main():
#    terminalList = ParseXmlRobotConfiguration.parseXml("Assets/EntryConfiguration.xml")
    
#    print("blabla")

#main()
