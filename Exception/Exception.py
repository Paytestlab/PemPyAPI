#!/usr/bin/python3

class Error(Exception):
    pass

class InputError(Error):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

class ParseError(Error):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


class ConnectionError(Error):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

class NotImplementedError(Error):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

class DestinationNotFoundError(Error):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

class DeviceStateError(Error):
    def __init__(self, expression, message):
        self.expression = expression;
        self.message = message;