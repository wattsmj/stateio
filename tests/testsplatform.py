"""
Unit tests for the InetObject object
"""
# UnitTest Lib
import unittest
from collections import namedtuple
import os
# InetObject Lib
from NAStateIO.io.text import NAIOTextCiscoIOS
from NAStateIO import NAStateIO
from testsettings import mockCiscoStateFilePath


class Test_CiscoPlatform(unittest.TestCase):
    """
    Test platform.json state parsing
    """

    def setUp(self):
        self.platform = NAStateIO(
            conn=NAIOTextCiscoIOS(path=os.sep.join(
                [mockCiscoStateFilePath, 'platform'])),
            base=open('tests/objectjson/cisco/base.json', 'r').read(),
            prefix='',
            json=open('tests/objectjson/cisco/platform.json', 'r').read())
        return super(Test_CiscoPlatform, self).setUp()

    def test_serial(self):
        """
        Test that the serial number is found correctly
        """
        self.assertTrue(
            self.platform.parse_state(
                pattern='serial',
                cmd_key='sh_version') == 'FXS11111111', 'Platform found not Serial')

    def test_PSUAstatus(self):
        """
        Test that the PSU A status is found correctly
        """
        self.assertTrue(
            self.platform.parse_state(
                pattern='psu_a_status',
                cmd_key='sh_env') == 'good', 'Platform found PSU A Status')

    def test_PSUBstatus(self):
        """
        Test that the PSU A status is found correctly
        """
        self.assertTrue(
            self.platform.parse_state(
                pattern='psu_b_status',
                cmd_key='sh_env') == 'good', 'Platform found PSU B Status')

    def test_temp(self):
        """
        Test that the system temperature is found correctly
        """
        self.assertTrue(
            self.platform.parse_state(
                pattern='sys_temp',
                cmd_key='sh_env') == 'no temperature alarms', 'Platform found temperature status')

    def test_STPMode(self):
        """
        Test that the STP mode is found correctly
        """
        self.assertTrue(
            self.platform.parse_state(
                pattern='stp_mode',
                cmd_key='sh_stp_sum') == 'pvst', 'Platform found STP mode')

    def test_STPPortfast(self):
        """
        Test that the STP PortFast mode is found correctly
        """
        self.assertTrue(self.platform.parse_state(
            pattern='stp_portfast',
            cmd_key='sh_stp_sum') == 'disabled', 'Platform found STP Portfast mode')

    def test_STPBPDUguard(self):
        """
        Test that the STP BPDU guard mode is found correctly
        """
        self.assertTrue(
            self.platform.parse_state(
                pattern='stp_bpduguard',
                cmd_key='sh_stp_sum') == 'disabled', 'Platform found STP BPDU Guard')

    def test_STPVlans(self):
        """
        Test that the STP VLAN list is found correctly
        """
        self.assertTrue(
            self.platform.parse_state(
                pattern='stp_vlans',
                cmd_key='sh_stp_sum',
                match_type='any') == ['VLAN0001', 'VLAN0002'], 'Platform: STP Vlans not found')

    def test_VlanSTPRoot(self):
        """
        Test that the STP root bridge is found correctly
        """
        self.assertTrue(
            [vlan.strip() for vlan in self.platform.parse_state(
                pattern='stp_root_vlans',
                cmd_key='sh_stp_sum').split(',')] == ['VLAN0001', 'VLAN0002'],
            'Platform found STP Root')

    def test_STPPriority(self):
        """
        Test that the STP bridge priority is found correctly
        """
        self.assertTrue(
            int(self.platform.parse_state(
                pattern='stp_vlan_priority',
                cmd_key='sh_stp_vlan')) == 4098, 'Platform: STP priority not found')

    def test_vlans(self):
        """
        Test that the VLAN database is found correctly
        """
        vlans = []
        for number, name in self.platform.parse_state(
                pattern='vlan',
                cmd_key='sh_vlan',
                match_type='any'):
            item = namedtuple('vlans', 'name, number')
            item.name = name
            item.number = int(number)
            vlans.append(item)
        if len(vlans) > 0:
            for index, vlan in enumerate(vlans):
                index += 1
                if index == 1:
                    self.assertTrue(vlan.number == 1,
                                    'Platform: Vlan 1 number not found')
                    self.assertTrue(vlan.name == 'default',
                                    'Vlan 2 name not found')
                elif index == 2:
                    self.assertTrue(vlan.number == 2,
                                    'Platform: Vlan 2 number not found')
                    self.assertTrue(vlan.name == 'VLAN0002',
                                    'Vlan 2 name not found')
                elif index == 3:
                    self.assertTrue(vlan.number == 3,
                                    'Platform: Vlan 3 number not found')
                    self.assertTrue(vlan.name == 'VLAN0003',
                                    'Vlan 3 name not found')
                elif index == 4:
                    self.assertTrue(vlan.number == 4,
                                    'Platform: Vlan 4 number not found')
                    self.assertTrue(vlan.name == 'VLAN0004',
                                    'Vlan 4 name not found')
                elif index == 5:
                    self.assertTrue(vlan.number == 5,
                                    'Platform: Vlan 5 number not found')
                    self.assertTrue(vlan.name == 'VLAN0005',
                                    'Vlan 5 name not found')
                elif index == 6:
                    self.assertTrue(vlan.number == 6,
                                    'Platform: Vlan 5 number not found')
                    self.assertTrue(vlan.name == 'VLAN0006',
                                    'Vlan 5 name not found')
                elif index == 7:
                    self.assertTrue(vlan.number == 1004,
                                    'Vlan 1004 number not found')
                    self.assertTrue(
                        vlan.name == 'fddinet-default', 'Vlan 1004 name not found')
                elif index == 8:
                    self.assertTrue(vlan.number == 1005,
                                    'Vlan 1005 number not found')
                    self.assertTrue(vlan.name == 'trbrf-default',
                                    'Vlan 1005 name not found')

    def test_TACACSServers(self):
        """
        Test that the TACACS+ server list is found correctly
        """
        self.assertTrue(
            self.platform.parse_state(
                pattern='tacacs_server',
                cmd_key='sh_tacacs',
                match_type='any') == ['1.1.1.1', '2.2.2.2'], 'Platform: TACACS servers not found')

    def test_TACACSTimeout(self):
        """
        Test that the TACACS+ server timeout is found correctly
        """
        self.assertTrue(
            int(self.platform.parse_state(
                pattern='tacacs_timeout',
                cmd_key='sh_run')) == 5, 'Platform: TACACS server timeout not found')

    def test_TACACSSrc(self):
        """
        Test that the TACACS+ source interface is found correctly
        """
        self.assertTrue(
            self.platform.parse_state(
                pattern='tacacs_src',
                cmd_key='sh_run') == 'Loopback0', 'Platform: TACACS source interface not found')


if __name__ == '__main__':
    unittest.main()
