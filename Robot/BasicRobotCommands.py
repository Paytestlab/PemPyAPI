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

class BasicRobotCommands(object):
    """basic command, independent from the layouts"""
    
    __key_press = [ "M42", "G4 P30",  "M43", "G4 P800" ];
    
    __increase_current = "M907 Z1.3";
    __reduce_current = "M907 Z0.7";
    __insert_card = "G28 Z0";
    __remove_card = "G0 Z50";
    __home = "G28";

    def _format_command(self, command):
        return "{}\r\n".format(command); 

    @property
    def key_press(self):
        return "\r\n".join(self.__key_press) + "\r\n";

    @property
    def increase_current(self):
        return self._format_command(self.__increase_current);

    @property
    def reduce_current(self):
        return self._format_command(self.__reduce_current);

    @property
    def insert_card(self):
        return self._format_command(self.__insert_card);
    
    @property
    def remove_card(self):
        return self.format_command(self.__remove_card);
        
    @property
    def home(self):
        return self._format_command(self.__home);


