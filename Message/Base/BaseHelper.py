#!/usr/bin/python3

from Message.Command import Command;
import socket;
from Message.HardwareMessage import HardwareMessage;
from Message.UDP.Interfaces import Interfaces;
from AxHw.InfoMessage import InfoMessage;
import logging;
import traceback;

class BaseHelper(object):
    def __init__(self, magic):
        self.magic = magic

    def send_message(self, message):
       raise NotImplementedError("base helper does not implement sending");


    def receive(self):
        raise NotImplementedError("base helper does not implement receiving");
