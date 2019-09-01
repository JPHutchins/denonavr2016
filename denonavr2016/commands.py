#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module contains instances of the XmlCommand class that are representations
of the Denon AVR 2016 XML command structure.  Refer to ./XML_data_dump.txt for
more information or to find out how to sniff commands on your own AVR.
"""
from .helpers import XmlCommand

SET_DYNAMIC_VOL = XmlCommand(
    "Dynamic Volume", "3", "SetAudyssey",
    (0, 3), param="dynamicvol",
    values=[
        "Off",
        "Light",
        "Medium",
        "Heavy"]
)
SET_LFE = XmlCommand(
    "LFE Level", "3", "SetSurroundParameter",
    (-10, 0), param="lfe")
    