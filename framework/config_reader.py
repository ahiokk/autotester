import os
import pathlib

def get_config_path() -> str:
    """Функция возвращает путь к конфигурационному файлу.
    Если переменная окружения CONFIG_PATH установлена — использовать её,
    иначе использовать путь по умолчанию /var/opt/kaspersky/config.ini.
    """
    DEFAULT_CONFIG_PATH = '/var/opt/kaspersky/config.ini'
    return os.environ.get('CONFIG_PATH', DEFAULT_CONFIG_PATH)

def file_parser() -> dict:
    """Функция читает и парсит INI-файл конфигурации в словарь."""

    # Получаем путь к файлу
    config_path = get_config_path()
    path = pathlib.Path(config_path)

    # Проверка: если файл не существует, выбрасываем исключение
    if not path.is_file():
        raise FileNotFoundError(f"Файл конфигурации не найден: {path}")

    sections = {}             # Словарь, где будут храниться все секции и параметры
    used_sections = set()      # Множество для отслеживания уже использованных секций
    current_section = None     # Текущая обрабатываемая секция
    has_duplicates = False     # Флаг наличия дублирующихся секций

    # Открываем файл для чтения
    with path.open('r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()  # Убираем пробелы по краям строки

            # Пропускаем пустые строки и комментарии (начинающиеся с ';' или '#')
            if not line or line.startswith(';') or line.startswith('#'):
                continue

            # Если строка - это начало новой секции
            if line.startswith('[') and line.endswith(']'):
                section = line[1:-1].strip()  # Вырезаем скобки и пробелы

                if section in used_sections:
                    has_duplicates = True  # Если секция уже была — отмечаем дубликат
                else:
                    sections[section] = {}  # Создаём новую секцию в словаре
                    used_sections.add(section)

                current_section = section  # Устанавливаем текущую секцию

            # Если строка — это параметр (ключ=значение) внутри секции
            elif '=' in line and current_section is not None:
                key, value = map(str.strip, line.split('=', 1))  # Разбиваем по первому знаку '='
                sections[current_section][key] = value  # Сохраняем ключ и значение в текущую секцию

    # Сохраняем информацию, были ли дубликаты секций
    sections['Duplicate'] = has_duplicates

    return sections
