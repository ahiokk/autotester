import pytest
import os
from framework.config_reader import file_parser

@pytest.fixture
def sections():
    """Фикстура для чтения конфига"""
    config_path = os.getenv('CONFIG_PATH')
    if not config_path:
        raise RuntimeError("Переменная окружения CONFIG_PATH не установлена")
    
    return file_parser()
