#!/usr/bin/python3

import sys;

class HardwareMessage(object):
    """Message struct"""

    command = 0;
    data = [];

    def __init__(self, magic):
        del self.data[:]
        self.command = 0;
        self.magic = magic;

    @staticmethod
    def parse(expectedMagic, payload):
        """
        Parse received UDP frame
        UDP Frame definition: MAGIC[8] MessageSequence[2] Command[2] DataLength[2] Data[0..512] 
        """

        if(payload is None):
            raise AttributeError();

        if(sys.getsizeof(payload) < 12):
            raise BufferError("Length must be at least 12 bytes");

        command_type = (payload[9] << 8) | payload[8]; 
        data_length = (payload[11] << 8) | payload[10];

        if((payload[:8] == bytearray(expectedMagic)) is False):
            raise RuntimeError();

        msg = HardwareMessage(expectedMagic);

        msg.command = command_type;

        for a in payload[12:]:
            msg.data.append(a);

        return msg;

    def get_bytes(self):

        if(self.data is None):
            #TODO
            pass;
        
        list = [];

        for single_value in self.magic:
            list.append(single_value);

        list.append(self.command);
        list.append(self.command >> 8);
        list.append(len(self.data));
        list.append(len(self.data) >> 8);
        if(len(self.data) > 0):
            for value in self.data:
                list.append(value);

        return bytearray(list);
