"""
Configular - config and secrets management

All files use INI format, as in:

[Section]
param1 = abc
param2 = 123

Read config parameter or secret with the following hierarchy:

  1. Environment variables, if available (defined as {section}_{param})
  2. Override file, if available (file stored outside of project)
  3. Config file (typically stored in project)

If a parameter is not found, ParameterNotFoundException is thrown, unless disabled in call to
constructor
"""

import os
from configparser import ConfigParser
from typing import Optional


class ParameterNotFoundException(Exception):
    """
    Thrown when parameter does not exist in environment variables or secrets file
    """
    def __init__(self, section: str, parameter: str):
        message = 'Parameter not found in env vars, override file, or config file: ' \
                f'section={section}, parameter={parameter}'
        super(ParameterNotFoundException, self).__init__(message)


class Configular:
    """
    Configular - config and secrets manager
    """
    def __init__(self, filename: str, override_filename: Optional[str] = None,
                 raise_on_not_found: bool = True):
        self.config = ConfigParser()
        self.config.read(os.path.expanduser(filename))
        if override_filename:
            self.override_config = ConfigParser()
            self.override_config.read(os.path.expanduser(override_filename))
        else:
            self.override_config = None
        self.raise_on_not_found = raise_on_not_found

    def get(self, section: str, parameter: str, default: Optional[str] = None) -> Optional[str]:
        """
        Get param value
        """
        value = self.get_from_env(section, parameter) or \
                self.get_from_config(self.override_config, section, parameter) or \
                self.get_from_config(self.config, section, parameter)
        if value:
            return value
        if default is None and self.raise_on_not_found:
            raise ParameterNotFoundException(section, parameter)
        return default

    @staticmethod
    def get_from_env(section: str, parameter: str) -> Optional[str]:
        """
        Return param from environment variable if available, else None
        """
        env_var_name = f'{section}_{parameter}'
        env_var_param = os.environ.get(env_var_name)
        if env_var_param:
            return env_var_param
        return None

    @staticmethod
    def get_from_config(config: ConfigParser, section: str, parameter: str) -> Optional[str]:
        """
        Return param from override file if available, else None
        """
        if config and config.has_option(section, parameter):
            config_param = config.get(section, parameter)
            if config_param:
                return config.get(section, parameter)
        return None
