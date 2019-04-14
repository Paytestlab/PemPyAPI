#!/usr/bin/python3

# Copyright (c) 2019 Matija Mazalin
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from Parsers.BaseLayout import BaseLayout
from xml.dom.minidom import parse
import logging
from Parsers.LayoutCommands.LayoutCommands import RobotCommand;

__author__ = "Matija Mazalin"
__email__ = "matija.mazalin@abrantix.com"
__license__ = "MIT"

class RobotLayout(BaseLayout):

    def populate(self):
        collection = self.__initialize__();

        if(collection is None):
            raise ValueError();

        positions = collection.getElementsByTagName("Position")
        self.__list = {}
        for position in positions:
           Canonical = position.getElementsByTagName('CanonicalName')[0]
           Value = position.getElementsByTagName('Value')[0]
           isButton = False;
           if(0 < len(position.getElementsByTagName('isButton'))):
               IsButtonNode = position.getElementsByTagName('isButton')[0]
               isButton = XmlParser.str_to_bool(IsButtonNode.childNodes[0].data)
    
           robot_command = RobotCommand(Canonical.childNodes[0].data, Value.childNodes[0].data, isButton)
           self.__list.update({Canonical.childNodes[0].data:robot_command})

    
        