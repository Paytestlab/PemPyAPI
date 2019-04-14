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


__author__ = "Matija Mazalin"
__email__ = "matija.mazalin@abrantix.com"
__license__ = "MIT"

from xml.dom.minidom import parse
import xml.dom.minidom
import logging


class BaseLayout(object):

    def __init__(self, filename, id):
        self.filename = filename;
        self.id = id;
        self.list = {};

    def str_to_bool(isButton):
        if (isButton is '1'):
            return True
        else:
            return False

    def populate(self):
        raise NotImplementedError();    
    

    def __initialize__(self):
        try:
            logging.info("robot({}): parse {}".format(self.id, self.filename))
            DOMTree = xml.dom.minidom.parse(self.filename);
            return DOMTree.documentElement;

        except IOError as e:
            logging.error("robot({}): parsing of {} returned an error".format(self.id, self.filename))
            return None;

    @property
    def is_initialized(self):
        if(self.list):
            return True;
        else:
            return False;

    @property
    def get_action(self, key):
        return self.list[key].Value;