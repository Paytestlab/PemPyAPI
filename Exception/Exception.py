#!/usr/bin/python3

class Error(Exception):
    pass

class PemInputError(Error):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

class PemParseError(Error):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

class PemTimeoutError(Error):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

class PemConnectionError(Error):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

class PemNotImplementedError(Error):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

class PemDestinationNotFoundError(Error):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

class PemDeviceStateError(Error):
    def __init__(self, expression, message):
        self.expression = expression;
        self.message = message;