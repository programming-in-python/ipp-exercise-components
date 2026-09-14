##
# MIT License
#
# Copyright (c) 2020 - 2025 Andrew D. King
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

"""
Load and read the course configuration file.

Wraps the standard-library ``configparser`` behind a small Singleton so
every caller shares one loaded configuration.
"""

import configparser
import logging
import os
import traceback
from pathlib import Path

from ipp.common import config_const
from ipp.common.singleton import Singleton


class ConfigUtil(metaclass=Singleton):
    """
    A simple wrapper around the built-in Python configuration infrastructure.

    Implemented as a Singleton via the ``Singleton`` metaclass, so every caller
    shares one loaded configuration.
    """

    enable_config_file_search = True

    config_file = None
    config_parser = configparser.ConfigParser()
    is_loaded = False

    failed_load_counter = 0

    def __init__(self, config_file: str = None):
        """
        Create the utility and load the configuration file.

        Args:
            config_file: The name of the configuration file to load.
        """
        self.config_file = config_file

        logging.info("Creating instance of ConfigUtil: %s", self.config_file)

        self._load_config()

    #
    # public methods
    #
    def get_config_file_name(self) -> str:
        """
        Return the name of the configuration file.
        """
        return self.config_file

    def get_credentials(self, section: str) -> dict:
        """
        Load and return a separate credential file as a dictionary.

        The credential file is referenced by a key that is assumed to be the
        same across all sections, so only the section name is required. When
        the referenced file exists, it is parsed as simple ``key = value``
        pairs and returned as a ``dict``. The key case is preserved, and no
        caching is performed beyond the returned object.

        Args:
            section: The name of the section holding the credential file key.

        Returns:
            The credential properties, or ``None`` when the section or file
            does not exist.
        """
        if self.has_section(section):
            cred_file_name = self.get_property(section, config_const.CRED_FILE_KEY)

            try:
                if os.path.exists(cred_file_name) and os.path.isfile(cred_file_name):
                    logging.info(
                        "Loading credentials from section "
                        + section
                        + " and file "
                        + cred_file_name
                    )

                    # read cred data and dump it into a custom section for parsing
                    file_ref = Path(cred_file_name)
                    cred_data = (
                        "[" + config_const.CRED_SECTION + "]\n" + file_ref.read_text()
                    )

                    # create unique ConfigParser that preserves key case
                    cred_parser = configparser.ConfigParser()
                    cred_parser.optionxform = str

                    # read the stringified file data and generate / return
                    # a dict for the section we just created
                    cred_parser.read_string(cred_data)
                    cred_props = dict(cred_parser.items(config_const.CRED_SECTION))

                    return cred_props
                else:
                    logging.warning("Credential file doesn't exist: " + cred_file_name)
            except Exception as e:
                traceback.print_exc()
                logging.warning(
                    "Failed to load credentials from file: "
                    + cred_file_name
                    + ". Exception: "
                    + str(e)
                )

        return None

    def get_property(
        self,
        section: str,
        key: str,
        default_val: str = None,
        force_reload: bool = False,
    ):
        """
        Return the value of ``key`` from the given config section.

        Args:
            section: The name of the section to parse.
            key: The name of the key to look up in ``section``.
            default_val: The value returned when the key is absent.
            force_reload: If ``True``, reload the config before reading.

        Returns:
            The value associated with ``key`` in ``section``.
        """
        return self._get_config(force_reload).get(section, key, fallback=default_val)

    def get_boolean(self, section: str, key: str, force_reload: bool = False):
        """
        Return the boolean value of ``key`` from the given config section.

        Args:
            section: The name of the section to parse.
            key: The name of the key to look up in ``section``.
            force_reload: If ``True``, reload the config before reading.

        Returns:
            The boolean associated with ``key`` in ``section``, or ``False``
            when it is absent or not truthy.
        """
        return self._get_config(force_reload).getboolean(section, key, fallback=False)

    def get_integer(
        self, section: str, key: str, default_val: int = 0, force_reload: bool = False
    ):
        """
        Return the integer value of ``key`` from the given config section.

        Args:
            section: The name of the section to parse.
            key: The name of the key to look up in ``section``.
            default_val: The value returned when the key is absent or invalid.
            force_reload: If ``True``, reload the config before reading.

        Returns:
            The integer associated with ``key`` in ``section``.
        """
        return self._get_config(force_reload).getint(section, key, fallback=default_val)

    def get_float(
        self,
        section: str,
        key: str,
        default_val: float = 0.0,
        force_reload: bool = False,
    ):
        """
        Return the float value of ``key`` from the given config section.

        Args:
            section: The name of the section to parse.
            key: The name of the key to look up in ``section``.
            default_val: The value returned when the key is absent or invalid.
            force_reload: If ``True``, reload the config before reading.

        Returns:
            The float associated with ``key`` in ``section``.
        """
        return self._get_config(force_reload).getfloat(
            section, key, fallback=default_val
        )

    def has_property(self, section: str, key: str) -> bool:
        """
        Report whether ``key`` exists in the named config section.

        Args:
            section: The name of the section to search.
            key: The name of the key to look up in ``section``.

        Returns:
            ``True`` if ``key`` is found in ``section``; ``False`` otherwise.
        """
        return self._get_config().has_option(section, key)

    def has_section(self, section: str) -> bool:
        """
        Report whether ``section`` exists in the loaded config.

        Args:
            section: The name of the section to search.

        Returns:
            ``True`` if ``section`` exists and has parameters; ``False``
            otherwise.
        """
        return self._get_config().has_section(section)

    def is_config_data_loaded(self) -> bool:
        """
        Report whether the configuration data has been loaded.
        """
        return self.is_loaded

    #
    # private methods
    #

    def _get_config(self, force_reload: bool = False) -> configparser:
        """
        Return the entire configuration object, loading it first if needed.

        Args:
            force_reload: If ``True``, reload the config before returning it.

        Returns:
            The parsed configuration object.
        """
        if not self.is_loaded or force_reload:
            self._load_config()

        return self.config_parser

    def _load_config(self):
        """
        Load the config file named on the constructor, or search for a default.
        """
        if self.failed_load_counter == 0:
            if self.config_file:
                # try to load the config file requested
                self._load_config_file(self.config_file)

            elif self.enable_config_file_search:
                # if no config file is specified, search upwards for the
                # 'config' path and - if found - try to load the default
                # config file name (config_const.CONFIG_FILE)
                logging.info("Attempting to locate %s.", config_const.CONFIG_FILE)
                self._locate_and_init_default_config_file_name()

        if not self.is_loaded:
            self.failed_load_counter += 1

    def _load_config_file(self, config_file: str):
        """
        Load the configuration from ``config_file`` when it exists.

        Args:
            config_file: The path of the configuration file to read.
        """
        if config_file:
            if os.path.exists(config_file):
                logging.info("Attempting to load config file: %s", config_file)

                try:
                    self.config_parser.read(config_file)
                    self.is_loaded = True

                    # set the configuration file
                    self.config_file = config_file

                    logging.info(
                        "Successfully loaded configuration at %s.", self.config_file
                    )
                    logging.debug("Config: %s", str(self.config_parser.sections()))

                except Exception:
                    logging.error(
                        "Failed to load requested config file at %s.", config_file
                    )
            else:
                logging.error(
                    "No file exists for requested config file %s.", config_file
                )

    def _locate_and_init_default_config_file_name(self):
        """
        Search parent paths for the default config file and load the first match.
        """
        module_path = os.path.dirname(__file__)
        parent_paths = Path(module_path).parents
        parent_path_count = len(parent_paths)

        for i in range(parent_path_count):
            config_file = os.path.abspath(
                os.path.join(parent_paths[i], "config", config_const.CONFIG_FILE)
            )

            logging.info("Searching path %s for config file.", config_file)

            if os.path.exists(config_file):
                logging.info("Found configuration file at %s", config_file)

                self._load_config_file(config_file)

                return
