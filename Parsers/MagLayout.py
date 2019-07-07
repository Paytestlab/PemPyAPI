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

from Parsers.BaseLayout import BaseLayout;
from xml.dom.minidom import parse
import xml.dom.minidom
import logging
from Parsers.LayoutCommands.LayoutCommands import MagstripeCommand

__author__ = "Matija Mazalin"
__email__ = "matija.mazalin@abrantix.com"
__license__ = "MIT"

class MagLayout(BaseLayout):

        def populate(self):
            collection = self.__initialize__();

            if(collection is None):
                raise ValueError();

            commands = collection.getElementsByTagName("Command")
            for command in commands:
                Canonical = command.getElementsByTagName('CanonicalName')[0]
                Brand = command.getElementsByTagName('Brand')[0]
                Track1 = command.getElementsByTagName('Track1')[0]
                Track2 = command.getElementsByTagName('Track2')[0]
                Track3 = command.getElementsByTagName('Track3')[0]

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

            magstripe = MagstripeCommand(canonical_data, brand_data, track1_data, track2_data, track3_data)
            self.list.update({Canonical.childNodes[0].data: magstripe})
        
        def get_track1(self, key):
            if(self.list):
                return self.list[key].Track1;
            else:
                return None;

        def get_track2(self, key):
            if(self.list):
                return self.list[key].Track2;
            else:
                return None;

        def get_track3(self, key):
            if(self.list):
                return self.list[key].Track3;
            else:
                return None;

