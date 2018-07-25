#!/usr/bin/python3

class AxUDPCommandError(Enum):
    """
    Possible error codes returned by the device in case of a \ref AxUDPCommand.ERROR
    Must be aligned with axCardMux firmware
    """
    CommandUnknown = 1,
    CommandSyntax
