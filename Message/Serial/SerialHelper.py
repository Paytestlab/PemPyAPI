import serial
from Message.HardwareMessage import HardwareMessage;
from Message.Base.BaseHelper import BaseHelper;
import logging;
import traceback;

class SerialHelper(BaseHelper):
    
    """udp class for sending/receiving data"""
    BAUD_RATE = 115200;
    TIMEOUT = 2.0;


    def __init__(self, port, magic):
        self.port = port
        self.magic = magic

    def send_message(self, message):
        try:
            ser = serial.Serial(self.port, self.BAUD_RATE, timeout=self.TIMEOUT);
            ser.write(message);

            header = ser.read(12);
            message_length = (header[11] << 8) | header[10];
            message = ser.read(message_length);
            response = header + message;
            if response:
                return HardwareMessage.parse(self.magic, response);
            else:
                logging.warning('no answer received from the endpoint {}'.format(self.port));
                raise TimeoutError('no answer received from the endpoint {}'.format(self.port))
        except serial.SerialTimeoutException:
            logging.warning('no answer received from the endpoint {}'.format(self.port));
            raise TimeoutError('no answer received from the endpoint {}'.format(self.port))
            raise;
    