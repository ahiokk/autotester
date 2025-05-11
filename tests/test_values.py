import pytest
from framework.config_reader import file_parser
from framework.validator import (
    is_int_in_range, is_float_in_range,
    is_valid_uuid, is_valid_locale, is_valid_directory_path
)

@pytest.fixture
def config():
    return file_parser()

@pytest.mark.parametrize("param_name, min_value, max_value", [
    ("ScanMemoryLimit", 1024, 8192),
    ("ExecArgMax", 10, 100),
    ("ExecEnvMax", 10, 100),
    ("MaxInotifyWatches", 1000, 1000000),
    ("MaxInotifyInstances", 1024, 8192),
])
def test_integer_range_parameters(config, param_name, min_value, max_value):
    value = config['General'][param_name]
    assert is_int_in_range(value, min_value, max_value)

@pytest.mark.parametrize("param_name", [
    "AdditionalDNSLookup", "CoreDumps", "RevealSensitiveInfoInTraces",
    "UseFanotify", "KsvlaMode", "StartupTraces"
])
def test_boolean_like_parameters(config, param_name):
    value = config['General'][param_name].lower()
    assert value in ("true", "false", "yes", "no")

def test_package_type(config):
    value = config['General']["PackageType"].lower()
    assert value in ("rpm", "deb")

def test_core_dumps_path_exists(config):
    path = config['General']["CoreDumpsPath"]
    assert is_valid_directory_path(path)

def test_machine_id_is_valid_uuid(config):
    value = config['General']["MachineId"]
    assert is_valid_uuid(value)

def test_locale_format(config):
    value = config['General']["Locale"]
    assert is_valid_locale(value)

def test_connect_timeout_format(config):
    value = config['Watchdog']["ConnectTimeout"]
    assert value.endswith("m")
    assert is_int_in_range(value[:-1], 1, 120)

@pytest.mark.parametrize("param_name", ["MaxVirtualMemory", "MaxMemory"])
def test_memory_limits(config, param_name):
    value = config['Watchdog'][param_name].lower()
    if value in ("off", "auto"):
        assert True
    else:
        assert is_float_in_range(value, 0, 100)

def test_ping_interval(config):
    value = config['Watchdog']["PingInterval"]
    assert is_int_in_range(value, 100, 10000)
