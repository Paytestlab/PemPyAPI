#!/usr/bin/python3

from xml.dom.minidom import parse
import xml.dom.minidom
import logging

class BaseConfiguration(object):
    def __init__(self, id, layout):
        self.Id = id;
        self.Layout = layout

class RobotConfiguration(BaseConfiguration):
    def __init__(self, Id, Ip, Port, layout):
        super().__init__(Id, layout);
        self.IP = Ip
        self.Port = Port

class MuxConfiguration(BaseConfiguration):
    def __init__(self, Id, mac_address, layout):
        super().__init__(Id, layout);
        self.mac_address = mac_address

class CtlMuxConfiguration(BaseConfiguration):
    def __init__(self, Id, mac_address, layout):
        super().__init__(Id, layout);
        self.mac_address = mac_address

class MagConfiguration(BaseConfiguration):

    def __init__(self, Id, mac_address, layout, serial_port):
        super().__init__(Id, layout);
        self.mac_address = mac_address
        self.port = serial_port

class ParseXmlRobotConfiguration(object):

    def parseXml(XmlFilename):
        try:
            logging.info("parsing {} for devices... ".format(XmlFilename))
            DOMTree = xml.dom.minidom.parse(XmlFilename)
        except IOError as e:
            logging.error("parsing error: " + XmlFilename)
            return None
        
        collection = DOMTree.documentElement

        robots = collection.getElementsByTagName("Robot")
        robot_list = {}
        mux_list = {}
        mag_list = {}
        ctl_mux_list = {}

        for robot in robots:
           id = robot.getAttribute('id')
           Ip = robot.getElementsByTagName('IpAddress')[0]
           IpPort = robot.getElementsByTagName('IpPort')[0]
           Layout = robot.getElementsByTagName('Layout')[0]
           robot_configuration = RobotConfiguration(id, Ip.childNodes[0].data, IpPort.childNodes[0].data, Layout.childNodes[0].data)
           robot_list.update({id:robot_configuration})

        muxs = collection.getElementsByTagName("CardMultiplexer")
        for mux in muxs:
            id = mux.getAttribute('id')
            mac_address = mux.getElementsByTagName('MacAddress')[0]
            Layout = mux.getElementsByTagName('Layout')[0]
            mux_configuration = MuxConfiguration(id, mac_address.childNodes[0].data, Layout.childNodes[0].data)
            mux_list.update({id:mux_configuration})

        mags = collection.getElementsByTagName("CardMagstriper")
        for mag in mags:
            id = mag.getAttribute('id')
            mac_address = mag.getElementsByTagName('MacAddress')[0]
            layout = mag.getElementsByTagName('Layout')[0]
            serial_port = mag.getElementsByTagName('SerialPort')[0]
            mag_configuration = MagConfiguration(id, mac_address.childNodes[0].data, layout.childNodes[0].data, serial_port.childNodes[0].data)
            mag_list.update({id:mag_configuration})

        ctl_muxs = collection.getElementsByTagName("ContactlessMultiplexer")
        for ctl_mux in ctl_muxs:
            id = ctl_mux.getAttribute('id')
            mac_address = ctl_mux.getElementsByTagName('MacAddress')[0]
            Layout = ctl_mux.getElementsByTagName('Layout')[0]
            ctl_mux_configuration = CtlMuxConfiguration(id, mac_address.childNodes[0].data, Layout.childNodes[0].data)
            ctl_mux_list.update({id:ctl_mux_configuration})

        return (robot_list, mux_list, mag_list, ctl_mux_list)

#def main():
#    terminalList = ParseXmlRobotConfiguration.parseXml("Assets/EntryConfiguration.xml")
    
#    print("blabla")

#main()
