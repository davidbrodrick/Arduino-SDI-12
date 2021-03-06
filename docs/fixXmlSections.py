#!/usr/bin/env python
import fileinput
import re
import os
import glob
import xml.etree.ElementTree as ET

fileDir = os.path.dirname(os.path.realpath("__file__"))
# print("Program Directory: {}".format(fileDir))
relative_dir = "../../Arduino-SDI-12Doxygen/xml/"
abs_file_path = os.path.join(fileDir, relative_dir)
abs_file_path = os.path.abspath(os.path.realpath(abs_file_path))
# print("XML Directory: {}".format(fileDir))

output_file = "examples.dox"
read_mes = [
    # '../Arduino-SDI-12Doxygen/xml_8ino-example.xml',
    "../../Arduino-SDI-12Doxygen/xml/a_wild_card_8ino-example.xml",
    "../../Arduino-SDI-12Doxygen/xml/b_address_change_8ino-example.xml",
    "../../Arduino-SDI-12Doxygen/xml/c_check_all_addresses_8ino-example.xml",
    "../../Arduino-SDI-12Doxygen/xml/d_simple_logger_8ino-example.xml",
    "../../Arduino-SDI-12Doxygen/xml/e_simple_parsing_8ino-example.xml",
    "../../Arduino-SDI-12Doxygen/xml/f_basic_data_request_8ino-example.xml",
    "../../Arduino-SDI-12Doxygen/xml/g_terminal_window_8ino-example.xml",
    "../../Arduino-SDI-12Doxygen/xml/h_SDI-12_slave_implementation_8ino-example.xml",
    "../../Arduino-SDI-12Doxygen/xml/i_SDI-12_interface_8ino-example.xml",
    "../../Arduino-SDI-12Doxygen/xml/j_external_pcint_library_8ino-example.xml",
    "../../Arduino-SDI-12Doxygen/xml/k_concurrent_logger_8ino-example.xml",
]
all_files = [f for f in os.listdir(abs_file_path) if os.path.isfile(os.path.join(abs_file_path, f))]

for filename in all_files:
    # print(filename)

    tree = ET.parse(os.path.join(abs_file_path, filename))
    root = tree.getroot()

    needs_to_be_fixed = False
    for definition in root.iter("compounddef"):
        # print(definition.attrib)
        compound_id = definition.attrib["id"]
        # print(compound_id)
        # print("---")

        for i in range(6):
            for section in definition.iter("sect" + str(i)):
                # print(section.attrib)
                section_id = section.attrib["id"]
                if not section_id.startswith(compound_id):
                    # print("problem!")
                    needs_to_be_fixed = True
                    dox_loc = section_id.find(".dox_")
                    section_suffix = section_id[dox_loc + 6 :]
                    # print(section_suffix)
                    corrected_id = compound_id + "_" + section_suffix
                    # print(corrected_id)
                    section.attrib["id"] = corrected_id

    if needs_to_be_fixed:
        tree.write(os.path.join(abs_file_path, filename + "_fixed"))
        os.rename(os.path.join(abs_file_path, filename), os.path.join(abs_file_path, filename + "_original"))
        os.rename(os.path.join(abs_file_path, filename + "_fixed"), os.path.join(abs_file_path, filename))
    # print()
