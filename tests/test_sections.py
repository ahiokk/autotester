import pytest
from framework.config_reader import file_parser

@pytest.fixture
def config():
    return file_parser()

def test_sections_exist(config):
    """Проверка наличия нужных секций"""
    assert "General" in config
    assert "Watchdog" in config

def test_no_duplicate_sections(config):
    """Проверка на отсутствие дубликатов секций"""
    assert config.get("Duplicate") is False

def test_correct_parameters_count(config):
    """Проверка количества параметров"""
    assert len(config["General"]) + len(config["Watchdog"]) == 19
