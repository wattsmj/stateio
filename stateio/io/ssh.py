"""
This module contains all the classes for NAStateIO to retrieve device
states over a netmiko connection, i.e. the output of "show version"
"""
# Python Lib
from socket import _socket
# Netmiko Lib
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException, NetMikoAuthenticationException
from ._abc import NAIO

class MissingCommandException(Exception):
    """
    Custom exception for Netmiko authentication and timeout exceptions
    combined.
    """

    def __init__(self, *args):
        super(MissingCommandException, self).__init__(*args)


class NAIONetmiko(NAIO):
    """
    Creates a connection to a remote device via Netmiko and allows the
    NAStateIO object to retrieve state via get_state(). The class also
    automatically switches back to a local user account if the primary
    account fails to login.
    """
    user = 'USER'
    admin = 'ADMIN'

    def __init__(self, **kwargs):
        """
        Save ip, user and admin account information
        """
        self._ip = kwargs.get('ip')
        self._user_account = kwargs.get('user_account')
        self._admin_account = kwargs.get('admin_account')
        self._conn = None

    def _initialise_conn(self, device):
        """
        A helper method that handles the netmiko SSH connection logic
        """
        conn = ConnectHandler(**device)
        conn.find_prompt()
        return conn

    def login(self):
        """
        Netmiko login logic
        """
        # Make sure the ip, user account and admin accounts are provided.
        if self._ip is None or self._user_account is None or self._admin_account is None:
            raise ValueError('ip, user or admin account not provided')
        # ip, user_account and admin_account is provided, log into internetworking
        # device
        try:
            device = {'ip': self._ip,
                      'device_type': 'cisco_ios',
                      'username': self._user_account['username'],
                      'password': self._user_account['password'],
                      'verbose': False}
            self._conn = self._initialise_conn(device)
            return self.user
        except NetMikoTimeoutException as exception:
            raise exception
        except NetMikoAuthenticationException as exception:
            device.update({
                'username': self._admin_account['username'],
                'password': self._admin_account['password']
            })

            try:
                self._conn = self._initialise_conn(device)
                return self.admin
            except NetMikoAuthenticationException as exception:
                raise exception
        except _socket.error as exception:
            raise exception

    def disconnect(self):
        """
        Disconnect the netmiko connection
        """
        self._conn.disconnect()

    def get_state(self, cmd):
        """
        Send the command to the netmiko connection
        """
        return self._conn.send_command(cmd)
