"""
Unit tests for the InetObject object
"""
# UnitTest Lib
import unittest
import os
# InetObject Lib
from NAStateIO.io.text import NAIOTextCiscoIOS
from NAStateIO import NAStateIO
from testsettings import mockCiscoStateFilePath


class Test_CiscoNAStateIO(unittest.TestCase):
    """
    Unit test that ensures the base InetObject is functioning correctly
    """

    def setUp(self):
        """
        Create a connection to a mock inet device
        """
        self.naStateIO = NAStateIO(
            conn=NAIOTextCiscoIOS(path=os.sep.join(
                [mockCiscoStateFilePath, 'platform'])),
            base=open('tests/objectjson/cisco/base.json', 'r').read(),
            prefix='',
            json=open('tests/objectjson/cisco/base.json', 'r').read())
        return super(Test_CiscoNAStateIO, self).setUp()

    def test_chassis(self):
        """
        Test that the chassis is found correctly
        """
        self.naStateIO.parse_state(pattern='chassis', cmd_key='sh_version')
        self.assertTrue(self.naStateIO._cache.get_attribute('chassis') == 'WS-C4510R+E', 'Chassis found in cache')
        
    def test_os(self):
        """
        Test that the OS is found correctly
        """
        self.naStateIO.parse_state(pattern='os', cmd_key='sh_version')
        self.assertTrue(self.naStateIO._cache.get_attribute('os') == '03.02.07.SG', 'OS found in cache')

if __name__ == '__main__':
    unittest.main()
