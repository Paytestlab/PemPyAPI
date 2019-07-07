#!/usr/bin/python3

from xml.dom.minidom import parse
import xml.dom.minidom
import logging

class BaseConfiguration(object):
    def __init__(self, id, layout):
        self.Id = id;
        self.Layout = layout

class SimConfiguration(BaseConfiguration):
    def __init__(self, Id, layout):
        super().__init__(Id, layout);

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
    def __init__(self, Id, mac_address, layout):
        super().__init__(Id, layout);
        self.mac_address = mac_address

class ParseXmlRobotConfiguration(object):

    __robot_list = {}
    __mux_list = {}
    __mag_list = {}
    __ctl_mux_list = {}
    __sim_list = {};
    __xml_file_name = "";

    def __init__(self, xml_file_name):
        self.__xml_file_name = xml_file_name;
        self.__parse_xml__();

    def __parse_xml__(self):
        try:
            logging.info("parsing {} for devices... ".format(self.__xml_file_name))
            DOMTree = xml.dom.minidom.parse(self.__xml_file_name)
        except IOError as e:
            logging.error("parsing error: " + self.__xml_file_name)
            return None
        
        collection = DOMTree.documentElement
        self.__parse_robot_xml(collection);
        self.__parse_magstripe_xml(collection);
        self.__parse_multiplexer_xml(collection);
        self.__parse_ctl_multiplexer_xml(collection);
        self.__parse_simulator_xml(collection);

    def __parse_robot_xml(self, collection):
        robots = collection.getElementsByTagName("Robot")
        for robot in robots:
           id = robot.getAttribute('id')
           Ip = robot.getElementsByTagName('IpAddress')[0]
           IpPort = robot.getElementsByTagName('IpPort')[0]
           Layout = robot.getElementsByTagName('Layout')[0]
           robot_configuration = RobotConfiguration(id, Ip.childNodes[0].data, IpPort.childNodes[0].data, Layout.childNodes[0].data)
           self.__robot_list.update({id:robot_configuration})

    def __parse_magstripe_xml(self, collection):
        mags = collection.getElementsByTagName("CardMagstriper")
        for mag in mags:
            id = mag.getAttribute('id')
            mac_address = mag.getElementsByTagName('MacAddress')[0]
            Layout = mag.getElementsByTagName('Layout')[0]
            mag_configuration = MagConfiguration(id, mac_address.childNodes[0].data, Layout.childNodes[0].data)
            self.__mag_list.update({id:mag_configuration})

    def __parse_multiplexer_xml(self, collection):
        muxs = collection.getElementsByTagName("CardMultiplexer")
        for mux in muxs:
            id = mux.getAttribute('id')
            mac_address = mux.getElementsByTagName('MacAddress')[0]
            Layout = mux.getElementsByTagName('Layout')[0]
            mux_configuration = MuxConfiguration(id, mac_address.childNodes[0].data, Layout.childNodes[0].data)
            self.__mux_list.update({id:mux_configuration})

    def __parse_ctl_multiplexer_xml(self, collection):
        ctl_muxs = collection.getElementsByTagName("ContactlessMultiplexer")
        for ctl_mux in ctl_muxs:
            id = ctl_mux.getAttribute('id')
            mac_address = ctl_mux.getElementsByTagName('MacAddress')[0]
            Layout = ctl_mux.getElementsByTagName('Layout')[0]
            ctl_mux_configuration = CtlMuxConfiguration(id, mac_address.childNodes[0].data, Layout.childNodes[0].data)
            self.__ctl_mux_list.update({id:ctl_mux_configuration})

    def __parse_simulator_xml(self, collection):
        sims = collection.getElementsByTagName("Simulator")
        for sim in sims:
            id = sim.getAttribute('id')
            Layout = sim.getElementsByTagName('Layout')[0];
            sim_configuration = SimConfiguration(id, Layout.childNodes[0].data);
            self.__sim_list.update({id:sim_configuration});

    @property
    def robots(self):
        return self.__robot_list;

    @property
    def magstripers(self):
        return self.__mag_list;

    @property
    def multiplexers(self):
        return self.__mux_list;

    @property
    def contactless_multiplexers(self):
        return self.__ctl_mux_list;
    
    @property
    def simulators(self):
        return self.__sim_list;

