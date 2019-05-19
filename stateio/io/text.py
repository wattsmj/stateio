"""
This module contains all the classes for NAStateIO to read local text
files with saved device states, i.e. the output of "show version"
"""
import os
from ._abc import NAIO

class NAIOText(NAIO):
    """
    Reads local text files with saved device states and allows the
    NAStateIO object to retrieve state via getState(). This class is
    abstract and should be inherited from and the getState() method added
    """

    def __init__(self, **kwargs):
        """
        Saves values path
        """
        # Path to the folder that contains the state text files.
        self._path = kwargs['path']

    def _find_file(self, filename):
        # Add file type suffix
        filename = self._path + os.sep + filename + '.ist'
        if os.path.exists(filename):
            with open(filename, 'r') as cmd_text:
                return cmd_text.read()
        else:
            return None


class NAIOTextCiscoIOS(NAIOText):
    """
    An implementation of NAIOText for a Cisco IOS internetworking devices
    """

    def get_state(self, cmd):
        """
        Read a text file with the same name as the command without spaces and return it's content
        """
        filename = cmd.split('|')[0].replace(' ', '').strip()
        cmd_text = self._find_file(filename)
        return cmd_text
