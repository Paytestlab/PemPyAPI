#!/usr/bin/python3

from enum import IntEnum;

class AxUDPCardMagstriperCommand(IntEnum):
    
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
    Error = 3,

    """
    Set track 1.
    """
    SetTrack1 = 4,

    """
    Set track 1.
    """
    SetTrack2 = 5,

    """
    Set track 1.
    """
    SetTrack3 = 6,

    """
    Clear all track data
    """
    ClearTracks = 7,

    """
    Sends configured tracks. After sending the tracks, all track information will be cleared
    """
    SendTracks = 8,

    """
    Sets the desired track clock for tracks 1..3  
    """
    SetTrackClock = 9,

    """
    Sets the desired options for track 1..3
    """
    SetTrackOptions = 10,
