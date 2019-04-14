#!/usr/bin/python3

import socket
from socket import timeout as SocketTimeout;
from socket import error as SocketError;
import errno;
import logging;

class PEMSocket(object):
     
    BUFFER_SIZE = 1024;

    def __init__(self, IP, Port):
        self.IP = IP
        self.Port = Port

    def connect(self):
        try:
            self.Connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.Connection.connect((self.IP, self.Port)) 
            self.Connection.settimeout(10.0)
        except SocketError as e:
            logging.error("robot: could not connect({}) to {}:{}. socket already in use".format(str(e.errno), self.IP, self.Port))
            return False
        except Exception as e:
            logging.error("robot: could not connect({}) to {}:{}".format(str(e.errno), self.IP, self.Port))
            return False;
        
        return True

    def send(self, Message):
        EndMessage = Message + "\r\n"
        data = bytes(EndMessage, 'utf-8')
        try:
            self.Connection.send(data)
        except SocketError as e:
            logging.warning("robot: sending "+ str(len(Message)) + "bytes was not successful")
            return False

        return True

    def receive(self):
        try:
            response = self.Connection.recv(self.BUFFER_SIZE);
            responseString = response.decode("utf-8");
        except SocketTimeout as e:
            raise TimeoutError("robot: the device did not respond in time");
        except SocketError as e:
            logging.warning("robot: could not receive any data(" + str(e.errno) + ")")
            return ''
        return responseString;

    def receiveWithTimeout(self, Timeout):
        try:
            self.Connection.settimeout(Timeout)
            response = self.Connection.recv(self.BUFFER_SIZE).decode("utf-8")
            self.Connection.settimeout(10)
        except SocketError as e:
            logging.warning("robot: could not receive any data(" + str(e.errno) + ")")
            return ''

        return response

    def close(self):
        self.Connection.shutdown(socket.SHUT_RDWR);
        self.Connection.close()
