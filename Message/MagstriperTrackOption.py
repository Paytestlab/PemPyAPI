#!/usr/bin/python3

from enum import IntEnum;

class MagstripeCardEmulatorTrackOption():
    """
    Possible track options
    Must be aligned with axCardMux firmware
    """

    NONE = 0

   # bSends a wrong lrc to the card reader which should provoke an LRC error
    WRONG_LRC = 1
