import pytest
from tests.fixtures import sections

def test_parameter_count(sections):
    """Проверка количества параметров"""
    assert len(sections['General']) + len(sections['Watchdog']) == 19, 'Неверное количество параметров'

@pytest.mark.parametrize(
    'parameter_name, section',
    [
        ('ScanMemoryLimit', 'General'),
        ('PackageType', 'General'),
        ('ExecArgMax', 'General'),
        ('AdditionalDNSLookup', 'General'),
        ('CoreDumps', 'General'),
        ('RevealSensitiveInfoInTraces', 'General'),
        ('ExecEnvMax', 'General'),
        ('MaxInotifyWatches', 'General'),
        ('CoreDumpsPath', 'General'),
        ('UseFanotify', 'General'),
        ('KsvlaMode', 'General'),
        ('MachineId', 'General'),
        ('StartupTraces', 'General'),
        ('MaxInotifyInstances', 'General'),
        ('Locale', 'General'),
        ('ConnectTimeout', 'Watchdog'),
        ('MaxVirtualMemory', 'Watchdog'),
        ('MaxMemory', 'Watchdog'),
        ('PingInterval', 'Watchdog'),
    ]
)
def test_parameters_exist(sections, parameter_name, section):
    """Проверка, что параметры есть в секциях"""
    assert parameter_name in sections[section], f"Параметр {parameter_name} не найден в секции {section}"
