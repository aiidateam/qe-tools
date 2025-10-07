from __future__ import annotations

from importlib.resources import files
from xml.etree import ElementTree

from xmlschema import XMLSchema

from qe_tools.outputs.parsers import schemas
from qe_tools.outputs.parsers.base import BaseOutputFileParser, BaseStdoutParser


class PwXMLParser(BaseOutputFileParser):
    """
    Class for parsing the XML output of pw.x.
    """

    @staticmethod
    def parse(content):
        """Parse the XML output of Quantum ESPRESSO pw.x."""

        try:
            element_root = ElementTree.fromstring(content)
        except ElementTree.ParseError:
            raise ValueError(
                "Unable to parse the XML file!\n"
                "Double-check that the file is the correct one, and is not incomplete/corrupted."
            ) from None

        str_filename = element_root.get(
            "{http://www.w3.org/2001/XMLSchema-instance}schemaLocation"
        )
        if str_filename is None:
            raise ValueError(
                "There was an error while reading the version of QE in the provided xml file."
            )

        schema_filename = str_filename.split()[1].split("/")[-1]

        # Fix issue for QE v7.0: The scheme file name was not updated to `qes_211101.xsd` in the `xsi.schemaLocation`
        # element, see https://github.com/aiidateam/aiida-quantumespresso/pull/774
        try:
            if (
                element_root.find("general_info").find("creator").get("VERSION")
                == "7.0"
            ):  # type: ignore
                schema_filename = "qes_211101.xsd"
        except AttributeError:
            pass

        return XMLSchema(str(files(schemas) / schema_filename)).to_dict(element_root)


class PwStdoutParser(BaseStdoutParser):
    """
    Class for parsing the standard output of pw.x.
    """
