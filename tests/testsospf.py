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


class Test_CiscoOSPF(unittest.TestCase):
    """
    Unit test that ensures OSPF is functioning correctly
    """

    def setUp(self):
        """
        Create a connection to a mock inet device
        """
        self.ospf = NAStateIO(
            conn=NAIOTextCiscoIOS(path=os.sep.join(
                [mockCiscoStateFilePath, 'ospf'])),
            base=open('tests/objectjson/cisco/base.json', 'r').read(),
            prefix='OSPF',
            json=open('tests/objectjson/cisco/ospf.json', 'r').read(),
            match_type='any')
        return super(Test_CiscoOSPF, self).setUp()

    def test_Interfaces(self):
        """
        Test that CDP neighbour entries were found correctly
        """
        self.assertTrue(
            self.ospf.parse_state(
                pattern='ospf_ints',
                cmd_key='sh_ospf_ints') == ['Ethernet0'], 'OSPF: interfaces not found')


class Test_CiscoOSPFInterface(unittest.TestCase):
    """
    Unit test that ensures OSPF interface is functioning correctly
    """

    def setUp(self):
        """
        Create a connection to a mock inet device
        """
        self.ospf = NAStateIO(
            conn=NAIOTextCiscoIOS(path=os.sep.join(
                [mockCiscoStateFilePath, 'ospf'])),
            base=open('tests/objectjson/cisco/base.json', 'r').read(),
            prefix='OSPFInterface',
            json=open('tests/objectjson/cisco/ospf.json', 'r').read())
        return super(Test_CiscoOSPFInterface, self).setUp()

    def test_processid(self):
        """
        Test that OSPF interface process ID entry was found correctly
        """
        self.assertTrue(
            int(self.ospf.parse_state(
                pattern='processid',
                cmd_key='sh_ospf_ints')) == 1, 'OSPF Interface: process ID not found')

    def test_routerid(self):
        """
        Test that OSPF interface router ID entry was found correctly
        """
        self.assertTrue(
            self.ospf.parse_state(
                pattern='routerid',
                cmd_key='sh_ospf_ints') == '192.168.45.1', 'OSPF Interface: router ID not found')

    def test_cost(self):
        """
        Test that OSPF interface cost entry was found correctly
        """
        self.assertTrue(
            int(self.ospf.parse_state(
                pattern='cost',
                cmd_key='sh_ospf_ints')) == 10, 'OSPF Interface: cost not found')

    def test_areaid(self):
        """
        Test that OSPF interface area ID entry was found correctly
        """
        self.assertTrue(
            int(self.ospf.parse_state(
                pattern='areaid',
                cmd_key='sh_ospf_ints')) == 0, 'OSPF Interface: area ID not found')

    def test_routed(self):
        """
        Test that OSPF interface is routed (sending OSPF hellos)
        """
        self.assertTrue(
            self.ospf.parse_state(
                pattern='routed',
                cmd_key='sh_ospf_ints') == 'Hello due', 'OSPF Interface: OSPF hellos not found')


if __name__ == '__main__':
    unittest.main()
