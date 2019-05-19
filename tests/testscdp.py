"""
Unit tests for the InetObject object
"""
# UnitTest Lib
import unittest
import os
# NAStateIO Lib
from stateio.io.text import NAIOTextCiscoIOS
from stateio import NAStateIO
from testsettings import mockCiscoStateFilePath

class Test_CiscoCDP(unittest.TestCase):
    """
    Unit test that ensures CDPFactory is functioning correctly
    """

    def setUp(self):
        """
        Create a connection to a mock inet device
        """
        self.cdp = NAStateIO(
            conn=NAIOTextCiscoIOS(path=os.sep.join([mockCiscoStateFilePath, 'cdp'])),
            base=open('tests/objectjson/cisco/base.json', 'r').read(),
            prefix='CDP',
            json=open('tests/objectjson/cisco/cdp.json', 'r').read(),
            match_type='any')
        return super(Test_CiscoCDP, self).setUp()

    def test_get_neighbours(self):
        """
        Test that CDP neighbour entries were found correctly
        """
        self.assertTrue(
            self.cdp.parse_state(
                pattern='cdp_neighbours',
                cmd_key='sh_cdp_neighbours') == ['SW1', 'SW2', 'SW3'], 'CDP: Neighbours not found')

class Test_CiscoCDPNeighbour(unittest.TestCase):
    """
    Unit test that ensures CDP is functioning correctly
    """

    def setUp(self):
        """
        Create a connection to a mock inet device
        """
        self.cdp = NAStateIO(
            conn=NAIOTextCiscoIOS(path=os.sep.join([mockCiscoStateFilePath, 'cdp'])),
            base=open('tests/objectjson/cisco/base.json', 'r').read(),
            prefix='CDPEntry',
            json=open('tests/objectjson/cisco/cdp.json', 'r').read())
        return super(Test_CiscoCDPNeighbour, self).setUp()

    def test_IP(self):
        """
        Test that CDP neighbour IP was found correctly
        """
        self.assertTrue(
            self.cdp.parse_state(
                pattern='cdp_nei_ip',
                cmd_key='sh_cdp_entry') == '10.228.138.98',
            'CDP Neighbour: Neighbour\'s IP not found')

    def test_LocalInterface(self):
        """
        Test that CDP neighbour local interface was found correctly
        """
        self.assertTrue(
            self.cdp.parse_state(
                pattern='cdp_nei_local_int',
                cmd_key='sh_cdp_entry') == 'GigabitEthernet2/6',
            'CDP Neighbour: local interface not found')

    def test_NeighbourInterfaces(self):
        """
        Test that CDP neighbour remote interface was found correctly
        """
        self.assertTrue(
            self.cdp.parse_state(
                pattern='cdp_nei_remote_int',
                cmd_key='sh_cdp_entry') == 'GigabitEthernet0/1',
            'CDP Neighbour: local interface not found')

    def test_NeighbourChassis(self):
        """
        Test that CDP neighbour chassis was found correctly
        """
        self.assertTrue(
            self.cdp.parse_state(
                pattern='cdp_nei_chassis',
                cmd_key='sh_cdp_entry') == 'IE-3010-16S-8PC',
            'CDP Neighbour: chassis not found')

if __name__ == '__main__':
    unittest.main()
