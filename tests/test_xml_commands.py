#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test make_xml_command.py
"""

import unittest
from denonavr2016.helpers import make_xml_command, XmlCommand1, XmlCommand3

SET_DYNAMIC_VOL = XmlCommand3(
    "Dynamic Volume", "SetAudyssey",
    (0, 3), param="dynamicvol",
    values=[
        "Off",
        "Light",
        "Medium",
        "Heavy"]
)
SET_LFE = XmlCommand3(
    "LFE Level", "SetSurroundParameter",
    (-10, 0), param="lfe") #left values field blank
SET_CENTER_LEVEL = XmlCommand1(
    "Center Level", "SetChLevel",
    (0, 48), name="C"
)
SET_DIALOG_LEVEL = XmlCommand1(
    "Dialog Level", "SetDialogLevel",
    (0, 48)
)

class TestXmlCommands(unittest.TestCase):

    def test_dict(self):
        """
        Test the friendly_name to integer value conversion.
        """
        self.assertEqual(make_xml_command(SET_DYNAMIC_VOL, "Off"),
b'<?xml version=\'1.0\' encoding=\'utf8\'?>\n\
<tx><cmd id="3"><name>SetAudyssey</name><list>\
<param name="dynamicvol">0</param></list></cmd></tx>')

        self.assertEqual(make_xml_command(SET_DYNAMIC_VOL, "Light"),
b'<?xml version=\'1.0\' encoding=\'utf8\'?>\n\
<tx><cmd id="3"><name>SetAudyssey</name><list>\
<param name="dynamicvol">1</param></list></cmd></tx>')

        self.assertEqual(make_xml_command(SET_DYNAMIC_VOL, "Medium"),
b'<?xml version=\'1.0\' encoding=\'utf8\'?>\n\
<tx><cmd id="3"><name>SetAudyssey</name><list>\
<param name="dynamicvol">2</param></list></cmd></tx>')

        self.assertEqual(make_xml_command(SET_DYNAMIC_VOL, "Heavy"),
b'<?xml version=\'1.0\' encoding=\'utf8\'?>\n\
<tx><cmd id="3"><name>SetAudyssey</name><list>\
<param name="dynamicvol">3</param></list></cmd></tx>')

    def test_int_instead_of_string(self):
        """
        Test the Try/Except that handles entering an int instead of string.
        """
        self.assertEqual(make_xml_command(SET_DYNAMIC_VOL, 0),
b'<?xml version=\'1.0\' encoding=\'utf8\'?>\n\
<tx><cmd id="3"><name>SetAudyssey</name><list>\
<param name="dynamicvol">0</param></list></cmd></tx>')

    def test_missing_values(self):
        """
        Test handling missing values field.
        """
        self.assertEqual(make_xml_command(SET_LFE, -5),
b'<?xml version=\'1.0\' encoding=\'utf8\'?>\n\
<tx><cmd id="3"><name>SetSurroundParameter</name><list>\
<param name="lfe">-5</param></list></cmd></tx>')

    def test_cmd_id_1_commands(self):
        """
        Test the slightly different syntax when cmd_id = 1.
        """
        self.assertEqual(make_xml_command(SET_CENTER_LEVEL, 30),
b'<?xml version=\'1.0\' encoding=\'utf8\'?>\n\
<tx><cmd id="1">SetChLevel</cmd><name>C</name><value>30</value></tx>')

        self.assertEqual(make_xml_command(SET_DIALOG_LEVEL, "-11.5dB"),
b'<?xml version=\'1.0\' encoding=\'utf8\'?>\n\
<tx><cmd id="1">SetDialogLevel</cmd><value>1</value></tx>')

if __name__ == '__main__':
    unittest.main()