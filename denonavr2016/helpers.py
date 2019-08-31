#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Classes and functions for denonavr.
"""

import xml.etree.ElementTree as ET

class XmlCommand:
    """
    This class is a representation of XML commands from the Denon AVR 2016 App.

    Attributes:
        friendly_name (string): The friendly name of the command.
        cmd_id (string): "1" or "3" according to Denon API.
        name (string): name according to Denon API.
        bounds (tuple(int, int)): the (lower, upper) bounds of the command.
        param (string): The paramater name according to Denon API, defaults to
            None.
        values (list[strings]): A list indexed by the integer value expected by
            the Denon API containing the friendly names associated with each
            value. For example ["Off", "On"]. Defaults to None.
    """
    def __init__(self, friendly_name, cmd_id, name, bounds, param=None,
                 values=None):
        """
        The constructor for the XmlCommand class.

        If the values attribute was provided then the constructor will
        translate those fields into a dictionary so that the integer value can
        be accessed by referring to the friendly name of the command.
        """
        self.friendly_name = friendly_name
        self.cmd_id = cmd_id
        self.name = name
        self.bounds = bounds
        self.param = param
        self.values = values

        if values:
            self.value_dict = {}
            for number, key in enumerate(self.values):
                self.value_dict[key] = str(number)

def make_xml_command(command, value):
    """
    Package a command and value into XML for the Denon API.

    Args:
        command (XmlCommand): An instance of the XmlCommand class.
        value (string): The value that the command is to bet set to.

    Returns:
        string: Formatted XML string ready to POST.
    """
    xml_root = ET.Element("tx")
    xml_cmd_id = ET.SubElement(xml_root, "cmd", {"id": command.cmd_id})
    xml_name = ET.SubElement(xml_cmd_id, "name")
    xml_name.text = command.name

    if command.param:
        xml_list = ET.SubElement(xml_cmd_id, "list")
        xml_param = ET.SubElement(xml_list, "param", {"name": command.param})
        try:
            xml_param.text = command.value_dict[value]
        except KeyError:
            xml_param.text = str(value)
    else:
        xml_value = ET.SubElement(xml_cmd_id, "value")
        try:
            xml_value.text = command.value_dict[value]
        except KeyError:
            xml_value.txt = str(value)

    return ET.dump(xml_root)
