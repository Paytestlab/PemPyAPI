#!/usr/bin/python3

from enum import IntEnum;

class CommandError(IntEnum):
    """
    Possible error codes returned by the device in case of a \ref AxUDPCommand.ERROR
    Must be aligned with axCardMux firmware
    """
    CommandUnknown = 1,
    CommandSyntax = 2
