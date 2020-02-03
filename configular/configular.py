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
    def __init__(self, env_var_name):
        message = f'Parameter not found in env vars, override file, or config file: {env_var_name}'
        super(ParameterNotFoundException, self).__init__(message)


class Configular(object):
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

    def get(self, section: str, parameter: str, default: Optional[str] = None) -> str:
        """
        Get param value
        """
        env_var_name = f'{section}_{parameter}'
        env_var_param = os.environ.get(env_var_name)
        if env_var_param:
            return env_var_param
        if self.override_config and self.override_config.has_option(section, parameter):
            override_config_param = self.override_config.get(section, parameter)
            if override_config_param:
                return override_config_param
        if self.config.has_option(section, parameter):
            config_param = self.config.get(section, parameter)
            if config_param:
                return self.config.get(section, parameter)
        if default is None and self.raise_on_not_found:
            raise ParameterNotFoundException(env_var_name)
        return default
