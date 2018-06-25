#!/usr/bin/python3

from xml.dom.minidom import parse
import xml.dom.minidom

class RobotConfiguration(object):
    """description of class"""

    def __init__(self, Id, Ip, Port, Layout):
        self.Id = Id
        self.IP = Ip
        self.Port = Port
        self.Layout = Layout


class MuxConfiguration(object):
    def __init__(self, Id, mac_address):
        self.Id = Id;
        self.mac_address = mac_address;


class ParseXmlRobotConfiguration(object):
    def parseXml(XmlFilename):
        try:

        # Open XML document using minidom parser
            DOMTree = xml.dom.minidom.parse(XmlFilename)
        except IOError as e:
            print("Could not parse the "+ XmlFilename +"...")
            return None
        
        collection = DOMTree.documentElement
        positions = collection.getElementsByTagName("Robot")

        #create the dictionary
        robot_list = {}

        # Save detail of each button.
        for position in positions:
           Id = position.getAttribute('id')
           Ip = position.getElementsByTagName('IpAddress')[0]
           IpPort = position.getElementsByTagName('IpPort')[0]
           Layout = position.getElementsByTagName('Layout')[0]
           robot = RobotConfiguration(Id, Ip.childNodes[0].data, IpPort.childNodes[0].data, Layout.childNodes[0].data)
           robot_list.update({Id:robot})


        muxs = collection.getElementsByTagName("CardMultiplexer");
        mux_list = {};
        for mux in muxs:
            id = mux.getAttribute('id');
            mac_address = mux.getElementsByTagName('MacAddress')[0];
            mux_configuration = MuxConfiguration(id, mac_address.childNodes[0].data);
            mux_list.update({id:mux_configuration});

        return (robot_list, mux_list);

   

#def main():
#    terminalList = ParseXmlRobotConfiguration.parseXml("Assets/EntryConfiguration.xml")
    
#    print("blabla")
    


#main()





