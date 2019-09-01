#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Classes and functions for denonavr.
"""

import xml.etree.ElementTree as ET

class XmlCommand1:
    """
    This class is a representation of XML commands from the Denon AVR 2016 App.
    The commands all have cmd_id=1 and AppCommand.xml as endpoint.
    """
    def __init__(self, friendly_name, cmd_id_text, bounds, name=None,
                 values=None):
        """
        The constructor for the XmlCommand1 class.

        Attributes:
            friendly_name (string): The friendly name of the command.
            cmd_id_text (string): text between <cmd id=1> and </cmd>
            bounds (tuple(int, int)): the (lower, upper) bounds of the command.
            name (string): The paramater name according to Denon API, defaults to
                None.
            values (list[strings]): A list indexed by the integer value expected by
                the Denon API containing the friendly names associated with each
                value. For example ["Off", "On"]. Defaults to None.

        If the values attribute was provided then the constructor will
        translate those fields into a dictionary so that the integer value can
        be accessed by referring to the friendly name of the command.
        """
        self.friendly_name = friendly_name
        self.cmd_id = "1"
        self.cmd_id_text = cmd_id_text
        self.bounds = bounds
        self.name = name
        self.values = values
        if values:
            self.value_dict = {}
            for number, key in enumerate(self.values):
                self.value_dict[key] = str(number)
        
        elif bounds[0] is 0 and bounds[1] is 48:
            self.value_dict = {}
            decibel = -12
            for number in range(49):
                if number % 2 is 0:
                    key = str(int(decibel)) + "dB"
                else:
                    key = str(decibel) + "dB"
                self.value_dict[key] = str(number)
                decibel += 0.5


class XmlCommand3:
    """
    This class is a representation of XML commands from the Denon AVR 2016 App.
    The commands all have cmd_id=3 and AppCommand0300.xml as endpoint.
    """
    def __init__(self, friendly_name, name, bounds, param=None, values=None):
        """
        The constructor for the XmlCommand3 class.

        Attributes:
            friendly_name (string): The friendly name of the command.
            name (string): name according to Denon API.
            bounds (tuple(int, int)): the (lower, upper) bounds of the command.
            param (string): The paramater name according to Denon API, defaults to
                None.
            values (list[strings]): A list indexed by the integer value expected by
                the Denon API containing the friendly names associated with each
                value. For example ["Off", "On"]. Defaults to None.

            If the values attribute was provided then the constructor will
            translate those fields into a dictionary so that the integer value can
            be accessed by referring to the friendly name of the command.
        """
        self.friendly_name = friendly_name
        self.cmd_id = "3"
        self.name = name
        self.bounds = bounds
        self.param = param
        self.values = values

        if values:
            self.value_dict = {}
            for number, key in enumerate(self.values):
                self.value_dict[key] = str(number)
        
        elif bounds[0] is 0 and bounds[1] is 48:
            self.value_dict = {}
            decibel = -12
            for number in range(49):
                if number % 2 is 0:
                    key = str(int(decibel)) + "dB"
                else:
                    key = str(decibel) + "dB"
                self.value_dict[key] = str(number)
                decibel += 0.5


def make_xml_command(command, value, zone=None):
    """
    Package a command and value into XML for the Denon API.

    Args:
        command (XmlCommand): An instance of the XmlCommand class.
        value (string): The value that the command is to bet set to.

    Returns:
        bytes: UTF-8 encoded XML string ready to POST.
    """
    xml_root = ET.Element("tx")
    xml_cmd_id = ET.SubElement(xml_root, "cmd", {"id": command.cmd_id})

    if command.cmd_id is "1":
        xml_cmd_id.text = command.cmd_id_text
        if command.name:
            xml_name = ET.SubElement(xml_root, "name")
            xml_name.text = command.name
        if command.zone:
            xml_zone = ET.SubElement(xml_root, "zone")
            xml_zone.text = zone

    elif command.cmd_id is "3":
        xml_name = ET.SubElement(xml_cmd_id, "name")
        xml_name.text = command.name
        if command.param:
            xml_list = ET.SubElement(xml_cmd_id, "list")
            xml_param = ET.SubElement(xml_list, "param", {"name": command.param})
            try:
                xml_param.text = command.value_dict[value]
            except (AttributeError, KeyError):
                xml_param.text = str(value)
            return ET.tostring(xml_root, encoding='utf8', method='xml')
    
    if command.cmd_id is "1":
        xml_value = ET.SubElement(xml_root, "value")
    elif command.cmd_id is "3":
        xml_value = ET.SubElement(xml_cmd_id, "value")

    try:
        xml_value.text = command.value_dict[value]
    except (AttributeError, KeyError):
        xml_value.text = str(value)

    return ET.tostring(xml_root, encoding='utf8', method='xml')
