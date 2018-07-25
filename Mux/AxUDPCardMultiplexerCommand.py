#!/usr/bin/python3

from enum import IntEnum;


class AxUDPCardMultiplexerCommand(IntEnum):
    
    """
    Get device information of type \ref InfoMessage.
    Can be sent as UDP broadcast to enumerate all devices within one network
    """
    INFO = 1,
    
    """
    Stores the MAC address into EEPROM of the device. 
    The MAC-address according device label is already factory-programmed, so there is no need to call this method at any time by customer.
    """
    SET_MAC_ADDRESS = 2,
    
    """
    Error message received from device. 
    See message data for given \ref AxUDPCommandError
    """
    ERROR = 3,

    """
    Set desired port.
    """
    SET_PORT = 4,

    """
    Get active port
    """
    GET_PORT = 5,

    """
    Use this command to enable or disable card tracing
    """
    CARD_TRACE = 6,
