from Message.Command import Command;
import serial;
import logging;
import traceback;
import sys
import glob
from Message.HardwareMessage import HardwareMessage;
from AxHw.InfoMessage import InfoMessage;

class SerialBroadcast:
    TIMEOUT = 1

    @staticmethod
    def fill_devices(magic):
        return SerialBroadcast.send_broadcast(magic)

    @staticmethod
    def get_info_message_by_broadcast(mac_address, magic):
        info_messages = SerialBroadcast.send_broadcast(magic)

        for message in info_messages:
            if(bytearray(message.MacAddress) == mac_address):
                return message
        return None

    @staticmethod
    def __parse_message(port, magic, responses, buffer):
        msg = HardwareMessage.parse(magic, buffer)
        info = InfoMessage()
        info.MacAddress = msg.data[2:8]
        info.Major = msg.data[0]
        info.Minor = msg.data[1]
        info.port = port
        info.magic = magic
        logging.debug('received data from port {}'.format(info.port))
        responses.append(info)

    @staticmethod
    def __transmit_message(port, bytes_array, magic, responses):
        try:
            port.write(bytes_array)
            port.timeout = SerialBroadcast.TIMEOUT
            while True:
                header = port.read(12);
                message_length = (header[11] << 8) | header[10];
                message = port.read(message_length);
                response = header + message;

                if response:
                    SerialBroadcast.__parse_message(port.portstr, magic, responses, response)
                    break;
        except serial.SerialTimeoutException:
            logging.debug('no answer received from port {}'.format(port.device))
            pass
        except Exception as e:
            logging.warning('got an exception in the discovery mechanism...')
            traceback.print_exc()
            pass

    @staticmethod
    def send_broadcast(magic):
        responses = []
        serial_message = HardwareMessage(magic);
        serial_message.command = int(Command.INFO);
        bytes_array = serial_message.get_bytes()

        # List available serial ports
        available_ports = SerialBroadcast.serial_ports()

        # Loop through each available port
        for port in available_ports:
            try:
                # Open serial port
                ser = serial.Serial(port, 115200, timeout=SerialBroadcast.TIMEOUT)

                # Transmit message
                SerialBroadcast.__transmit_message(ser, bytes_array, magic, responses)

                # Close serial port
                ser.close()

            except serial.SerialException:
                pass  # Ignore errors with this port

        return responses

    @staticmethod
    def serial_ports():
        """ Lists serial port names

            :raises EnvironmentError:
                On unsupported or unknown platforms
            :returns:
                A list of the serial ports available on the system
        """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result
