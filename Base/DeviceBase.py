#!/usr/bin/python3
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

import threading
from SQL.Statistics import Statistics;
from Message.CommandSenderManager import CommandSenderManager;
import logging

__author__ = "Matija Mazalin"
__email__ = "matija.mazalin@abrantix.com"
__license__ = "MIT"

class DeviceBase(object):
    
    tag = "invalid";

    def __init__(self, id, xml_parser, enable_statistics=False):
        self.mutex = threading.Lock()
        self.xml_parse = xml_parser;
        if(enable_statistics is True):
            self.statistics = Statistics();
        else:
            self.statistics = None;
        self.id = id;
        self.log_info("initialization start...");

    def UpdateTable(self, action):
        if(self.statistics is not None):
            self.statistics.insert(self.id, action, self.layout[action].Value);

    def device_lookup(self):
       self.device = CommandSenderManager(self.magic);
       deviceIsPresent = self.device.device_lookup(self.mac_address);
       if deviceIsPresent:
           self.log_info("device {} is present".format(self.get_mac_address()));
       else:
           self.log_warning("device {} is not present".format(self.get_mac_address()));

       return deviceIsPresent;

    def initialize_device(self, filename):
        self.layout = self.xml_parse(filename, self.id);
        if(self.layout is None):
            self.log_warning("initialization of {} failed, skip...".format(self.get_mac_address()));
            return False;

        self.log_info("initialization of {} successful...".format(self.get_mac_address()));
        return True;

    def connect(self):
        pass;

    def close_connection(self):
        pass;

    def __log_final_text(self, text):
        return "{}({}): {}".format(self.tag, self.id, text);

    def log_debug(self, text):
        logging.debug(self.__log_final_text(text));

    def log_info(self, text):
        logging.info(self.__log_final_text(text));

    def log_warning(self, text):
        logging.warning(self.__log_final_text(text));

    def log_error(self, text):
        logging.error(self.__log_final_text(text));



