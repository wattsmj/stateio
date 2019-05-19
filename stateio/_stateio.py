"""
Core module for sending/receving from devices.
"""
# Imports
# Core Python lib
import re
import _socket
import json as jsonProcessor
from .util import NAStateCache


class StateIO(object):
    """
    Base Internetworking Object
    """

    def __init__(self, conn, base, prefix, json, match_type='first'):
        """
        Prepares this object for use based on what we're connected to
        """

        self._match_type = match_type
        self._prefix = prefix
        self._conn = conn
        self._cache = NAStateCache()

        # Load JSON into dictionary
        try:
            self._json = jsonProcessor.loads(json)
            self._base = jsonProcessor.loads(base)

        except Exception as exception:
            raise exception

        # Prepare the _regexMap and _commandMap data structures
        # based on the device we're connected to.
        try:
            self._patterns = {}
            self._commands = {}
            self.load()

        except Exception as exception:
            raise exception

    def load(self):
        """
        Loads the dictionaries out of JSON objects
        """

        # Prefill generic command, pattern and template maps.
        data = {}
        for section in ['patterns', 'commands']:
            try:
                if self._prefix != '':
                    data = self._json[self._prefix][section]['Any']
                else:
                    data = self._json[section]['Any']

                # Add in querier json data for OS and chassis
                data.update(self._base[section]['Any'])
                setattr(self, '_' + section, data)

            except KeyError as exception:
                raise exception

        # Lookup essential details used to customise the map data.
        chassis = str(self.parse_state("chassis", "sh_version")).strip()
        OS = str(self.parse_state("os", "sh_version")).strip()
        data = {}
        for section in ['patterns', 'commands']:
            try:
                if self._prefix != '':
                    data = self._json[self._prefix][section]
                else:
                    data = self._json[section]

                if chassis in data:  # No else, if chassis isn't a key, then we're already done
                    if OS in data[chassis]:
                        getattr(self, '_' + section).update(data[chassis][OS])
                    else:
                        getattr(
                            self, '_' + section).update(data[chassis]['Any'])

            except KeyError as exception:
                raise exception

    def remove_from_cache(self, attribute):
        'Remove an attribute from the cache'
        self._cache.delete_attribute(attribute)

    def get_state(self, **kwargs):
        """
        Runs the commands on the device and stores the output.
        """

        # Grab the function params
        cmd_key = kwargs.get('cmd_key', None)
        cmd = kwargs.get('cmd', None)
        cmd_option = kwargs.get('cmd_option', None)
        no_cache = kwargs.get('no_cache', False)

        # Make sure that custom commands are not cached
        if cmd is not None:
            no_cache = True
        # Quickly return the cached result if possible
        if not no_cache:
            if self._cache.has_attribute(cmd_key):
                return self._cache.get_attribute(cmd_key)

        # Fill out the command either from a JSON key or a direct
        # command provided
        cmd_string = None
        if cmd_key in self._commands:
            cmd_string = self._commands[cmd_key]
        elif cmd is not None:
            cmd_string = cmd
        else:
            return None

        # Add command option if one was provided.
        if cmd_option is not None:
            if not cmd_option == "":
                cmd_string = cmd_string + " " + cmd_option
            else:
                return None

        # Send the command using NetMiko library
        try:
            resp_string = self._conn.get_state(cmd_string)
            resp_string = resp_string.strip()
        except _socket.error:
            return None
        except Exception:
            return None

        # Save result into the cache
        if not no_cache:
            self._cache.store_attribute(cmd_key, resp_string)

        # Return the response string
        return resp_string

    def parse_state(self, pattern, cmd_key, **kwargs):
        """
        Performs a regex match either first match or any match and stores the output in self.
        """

        # Grab the function params
        match_type = kwargs.get('match_type', False)
        no_cache = kwargs.get('no_cache', False)

        # Pull out the regex to use from the JSON map installed by load()
        if pattern in self._patterns:
            regex = self._patterns[pattern]
        else:
            return None

        # Run the match logic.
        try:
            # Command has been run previously, return the known answer from
            # cache.
            if not no_cache:
                if self._cache.has_attribute(pattern):
                    return self._cache.get_attribute(pattern)

            # Run the command to find the information to match against
            attr_cmd_value = self.get_state(cmd_key=cmd_key, no_cache=no_cache)

            # Check if the device was able to run the command.
            if attr_cmd_value is None or attr_cmd_value == "":
                return None

            # Determine what type of match to run.
            if match_type == 'any' or self._match_type == 'any':
                device_attr_value = re.findall(regex, attr_cmd_value)
            elif match_type == 'first' or self._match_type == 'first':
                device_attr_value = re.search(regex, attr_cmd_value).group(1)
            else:
                device_attr_value = re.search(regex, attr_cmd_value).group(1)

            if device_attr_value is not None:
                # Store the new output for later use.
                if not no_cache:
                    self._cache.store_attribute(pattern, device_attr_value)
                # Return the newly found value.
                return device_attr_value
            else:
                return device_attr_value

        except Exception:
            return None
