#!/usr/bin/python

from xml.dom.minidom import parse
import xml.dom.minidom

from Communication import PEMSocket

class Terminal(object):
    """description of class"""
    def __init__(self, CanonicalName, Value, IsButton):
        self.CanonicalName = CanonicalName
        self.Value = Value
        self.IsButton = IsButton


class XmlParser(object):
    def parseXml(XmlFilename):
        try:

        # Open XML document using minidom parser
            DOMTree = xml.dom.minidom.parse(XmlFilename)
        except IOError as e:
            print("Could not parse the "+ XmlFilename +"...")
            return None
        
        collection = DOMTree.documentElement
        positions = collection.getElementsByTagName("Position")

        #create the dictionary
        terminalList = {}

        # Print detail of each movie.
        for position in positions:
           Canonical = position.getElementsByTagName('CanonicalName')[0]
           Value = position.getElementsByTagName('Value')[0]
           IsButton = position.getElementsByTagName('isButton')[0]
           terminal = Terminal(Canonical.childNodes[0].data, Value.childNodes[0].data, IsButton.childNodes[0].data)
           terminalList.update({Canonical.childNodes[0].data:terminal})
           #TerminalList[Canonical.childNodes[0].data] = terminal

        return terminalList

   

#def main():
#    terminalList = parseXml("Yomani.xml")
#    socket = PEMSocket("localhost", 3000)
#    if(socket.connect() is False):
#      return -1
    

#    socket.send("G0\r\n")
#    receive = socket.receive()
#    print("Recieved:" + receive.decode("utf-8"))




#main()


