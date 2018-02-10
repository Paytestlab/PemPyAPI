#!/usr/bin/env python

import socket
from socket import error as SocketError
import errno
import logging

class PEMSocket(object):
     def __init__(self, IP, Port):
        self.IP = IP
        self.Port = Port
     def connect(self):
         try:
            self.Connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.Connection.connect((self.IP, self.Port)) 
            self.Connection.settimeout(2.5)
            receive = self.Connection.recv(self.BUFFER_SIZE)
            self.Connection.settimeout(10)
         except SocketError as e:
            logging.error("could not connect({}) to {}:{}. Socket already in use".format(str(e.errno), self.IP, self.Port))
            return False
         except Exception as e:
            logging.error("could not connect({}) to {}:{}".format(str(e.errno), self.IP, self.Port))
            return False;
         if("Smoothie" in receive.decode("utf-8")):
            return True
         return False

     def send(self, Message):
         EndMessage = Message + "\r\n"
         data = bytes(EndMessage, 'utf-8')
         try:
            self.Connection.send(data)
         except SocketError as e:
             logging.warning("sending of "+ str(len(Message)) + "bytes was not succesful")
             return False

         return True

     def receive(self):
         try:
             response = self.Connection.recv(self.BUFFER_SIZE).decode("utf-8")
         except SocketError as e:
             logging.warning("could not receive any data(" + str(e.errno) + ")")
             return ''
         return response

     def receiveWithTimeout(self, Timeout):
          try:
              self.Connection.settimeout(Timeout)
              response = self.Connection.recv(self.BUFFER_SIZE).decode("utf-8")
              self.Connection.settimeout(10)
          except SocketError as e:
             logging.warning("could not receive any data(" + str(e.errno) + ")")
             return ''
          return response
        

     def close(self):
        self.Connection.shutdown(socket.SHUT_RDWR);
        self.Connection.close()

     BUFFER_SIZE = 1024

        
