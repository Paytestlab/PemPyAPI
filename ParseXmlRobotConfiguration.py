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
        RobotList = {}

        # Save detail of each button.
        for position in positions:
           Id = position.getAttribute('id')
           Ip = position.getElementsByTagName('IpAddress')[0]
           IpPort = position.getElementsByTagName('IpPort')[0]
           Layout = position.getElementsByTagName('Layout')[0]
           robot = RobotConfiguration(Id, Ip.childNodes[0].data, IpPort.childNodes[0].data, Layout.childNodes[0].data)
           RobotList.update({Id:robot})

        return RobotList

   

#def main():
#    terminalList = ParseXmlRobotConfiguration.parseXml("Assets/EntryConfiguration.xml")
    
#    print("blabla")
    


#main()





