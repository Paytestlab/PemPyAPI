#!/usr/bin/python3

import sys;

class UDPMagics(object):

    """Magic bytes which precede all UDP datagrams being sent and received."""

    CardMultiplexerMagic = [0xD9, 0xC5, 0xAE, 0x42, 0xF8, 0x9F, 0x71, 0x8B]
    CardMagstriperMagic = [0xD9, 0xC5, 0xAE, 0x42, 0xF8, 0x9F, 0x71, 0x8C]
