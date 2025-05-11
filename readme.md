
Автоматизированное тестирование конфигурационных файлов Kaspersky

------Описание------

Этот проект предназначен для проверки валидности конфигурационных файлов `.ini` согласно заданным требованиям.  
Тесты написаны на `pytest` и проверяют:
- Корректность параметров в секциях `General` и `Watchdog`
- Диапазоны значений числовых параметров
- Формат булевых, строковых и файловых данных
- Наличие обязательных параметров
- Отсутствие дубликатов секций


------Настройка тестового окружения------

Рекомендуется использовать виртуальное окружение `venv`:

1. Создайте виртуальное окружение:
   python -m venv venv

2. Активируйте виртуальное окружение:

   - Windows (PowerShell):
     \venv\Scripts\Activate

   - Linux/macOS:
     source venv/bin/activate

3. Установите зависимости:
   pip install -r requirements.txt


------Запуск автотестов------

1. Установите переменную окружения `CONFIG_PATH` перед запуском тестов, указывая путь к тестируемому конфигурационному файлу.

   - Windows (PowerShell):
     $env:CONFIG_PATH =путь\до\вашего\config.ini

   - Windows(cmd)
     set CONFIG_PATH=C:путь\до\вашего\config.ini 

   - Linux/macOS:
     export CONFIG_PATH=/путь/до/вашего/config.ini
   

2. Запустите тесты:
   pytest -v

------Структура проекта------

├── framework/
│   ├── config_reader.py
│   └── validator.py
├── kaspersky/
│   └── tests/
│       ├── fixtures.py
│       ├── test_sections.py
│       ├── test_validator.py
│       └── test_values.py
├── requirements.txt
└── README.md


------Дополнительно------

Если хотите получить отчёт о покрытии тестами:

pip install pytest-cov
pytest --cov=framework tests/


------Требования------

- Python 3.10+
- Pytest 8.0+