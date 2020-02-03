"""
Tests for configular
"""

import os

import pytest

from configular import Configular
from configular import ParameterNotFoundException


CONFIG_FILE = 'tests/resources/config_file.cfg'
OVERRIDE_FILE = 'tests/resources/override_file.cfg'


@pytest.fixture
def config():
    return Configular(CONFIG_FILE, override_filename=OVERRIDE_FILE)


def setup_module():
    os.environ['Slack_token'] = 'yowutup'
    os.environ['EmptyValue_nothing_here'] = ''
    os.environ['JIRA_api_key'] = 'yayjirayay'
    os.environ['Github_instance_id'] = 'irregularengineering'
    os.environ['Github_username'] = 'bojack'


def teardown_module():
    del os.environ['Slack_token']
    del os.environ['EmptyValue_nothing_here']
    del os.environ['JIRA_api_key']
    del os.environ['Github_instance_id']
    del os.environ['Github_username']


def test_env_var_only(config: Configular):
    assert config.get('Slack', 'token') == 'yowutup'


def test_config_only(config: Configular):
    assert config.get('Github', 'username') == 'bojack'


def test_override_only(config: Configular):
    assert config.get('Salesforce', 'api_key') == 'notagoodkey'


def test_not_found(config: Configular):
    with pytest.raises(ParameterNotFoundException):
        config.get('BananaStand', 'money')


def test_not_found_no_throw():
    config = Configular(CONFIG_FILE, override_filename=OVERRIDE_FILE, raise_on_not_found=False)
    assert not config.get('BananaStand', 'money')


def test_env_var_override(config: Configular):
    assert config.get('JIRA', 'api_key') == 'yayjirayay'


def test_env_var_override_from_empty(config: Configular):
    assert config.get('Github', 'instance_id') == 'irregularengineering'


def test_env_var_override_to_empty(config: Configular):
    assert config.get('Github', 'username') == 'bojack'


def test_config_override(config: Configular):
    assert config.get('Github', 'password') == 'xyz789'


def test_config_override_from_empty(config: Configular):
    assert config.get('Github', 'token') == 'whenislunch'


def test_config_override_to_empty(config: Configular):
    assert config.get('Github', 'client_id') == 'irregular'


def test_all_empty(config: Configular):
    with pytest.raises(ParameterNotFoundException):
        config.get('EmptyValue', 'nothing_here')
