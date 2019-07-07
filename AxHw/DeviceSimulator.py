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

"""Thread safe base card multiplexer interface."""
__author__ = "Matija Mazalin"
__email__ = "matija.mazalin@abrantix.com"
__license__ = "MIT"


from Exception.Exception import Error
from Base.DeviceBase import DeviceBase;
from UDPMessage.UDPMagics import UDPMagics;
from Parsers.MuxLayout import MuxLayout;
from Parsers.SimLayout import SimLayout;
import traceback;


class DeviceSimulator(DeviceBase):

    tag = "simulator";

    def __init__(self, id, enable_statistics=False):
        super().__init__(id, SimLayout, enable_statistics);
  
    def send_command(self, action):
        try:
           action_value = self.layout.get_action(action);
           self.log_info("execution of {} was successful".format(action));
           Result = True;
        except TimeoutError as e:
            self.log_error("device {} did not respond in time".format(self.get_mac_address()));
        except KeyError as e:
            pass;
        except AssertionError as e:
            self.log_error("device {} returned an error".format(self.get_mac_address()));
        except:
            traceback.print_exc()
            self.log_error("device {} returned a general error".format(self.get_mac_address()));

        return Result;

    def get_mac_address(self):
        return self.id;

        






