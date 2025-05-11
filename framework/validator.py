from pathlib import Path
import uuid
import re


def is_valid_directory_path(path_str: str) -> bool:
    try:
        path = Path(path_str)
        return path.is_absolute() and path.exists() and path.is_dir()
    except Exception:
        return False


def is_valid_uuid(uuid_str: str) -> bool:
    try:
        uuid.UUID(uuid_str.strip())
        return True
    except Exception:
        return False


def is_valid_locale(locale_str: str) -> bool:
    unix_pattern = r'^[a-z]{2,3}_[A-Z]{2,3}(\.[a-zA-Z0-9\-]+)?$'
    rfc_pattern = r'^([a-z]{2,3}|i-[a-z0-9]+)(?:-[a-zA-Z0-9]+)*$'
    return bool(re.fullmatch(unix_pattern, locale_str) or re.fullmatch(rfc_pattern, locale_str.lower()))


def is_int_in_range(value, min_val, max_val):
    try:
        number = int(value)
        return min_val <= number <= max_val
    except Exception:
        return False


def is_float_in_range(value, min_val, max_val):
    try:
        number = float(value)
        return min_val < number <= max_val
    except Exception:
        return False


def validate_config(config: dict) -> dict:
    errors = {}

    general = config.get('General', {})
    watchdog = config.get('Watchdog', {})

    # Проверки General
    if not is_int_in_range(general.get('ScanMemoryLimit', 0), 1024, 8192):
        errors['ScanMemoryLimit'] = "Неверное значение (должно быть целое число от 1024 до 8192)"
    
    if general.get('PackageType', '').lower() not in ['rpm', 'deb']:
        errors['PackageType'] = "Должно быть rpm или deb"

    if not is_int_in_range(general.get('ExecArgMax', 0), 10, 100):
        errors['ExecArgMax'] = "Неверное значение (должно быть целое число от 10 до 100)"

    for key in ['AdditionalDNSLookup', 'CoreDumps', 'RevealSensitiveInfoInTraces', 
                'UseFanotify', 'KsvlaMode', 'StartupTraces']:
        if general.get(key, '').lower() not in ['true', 'false', 'yes', 'no']:
            errors[key] = f"Неверное значение в {key} (ожидалось true/false/yes/no)"
    
    if not is_int_in_range(general.get('ExecEnvMax', 0), 10, 100):
        errors['ExecEnvMax'] = "Неверное значение (целое число от 10 до 100)"
    
    if not is_int_in_range(general.get('MaxInotifyWatches', 0), 1000, 1000000):
        errors['MaxInotifyWatches'] = "Неверное значение (целое число от 1000 до 1000000)"

    if not is_valid_directory_path(general.get('CoreDumpsPath', '')):
        errors['CoreDumpsPath'] = "Путь должен быть абсолютным и существовать"

    if not is_valid_uuid(general.get('MachineId', '')):
        errors['MachineId'] = "Неверный UUID"

    if not is_int_in_range(general.get('MaxInotifyInstances', 0), 1024, 8192):
        errors['MaxInotifyInstances'] = "Неверное значение (целое число от 1024 до 8192)"

    if not is_valid_locale(general.get('Locale', '')):
        errors['Locale'] = "Неверный формат локали"

    # Проверки Watchdog
    connect_timeout = watchdog.get('ConnectTimeout', '')
    if not (connect_timeout.endswith('m') and is_int_in_range(connect_timeout[:-1], 1, 120)):
        errors['ConnectTimeout'] = "Неверное значение (целое число от 1 до 120 с окончанием 'm')"

    for field in ['MaxVirtualMemory', 'MaxMemory']:
        value = watchdog.get(field, '').lower()
        if value not in ['off', 'auto']:
            if not is_float_in_range(value, 0, 100):
                errors[field] = f"Неверное значение в {field} (off, auto или число (0;100])"

    if not is_int_in_range(watchdog.get('PingInterval', 0), 100, 10000):
        errors['PingInterval'] = "Неверное значение (целое число от 100 до 10000)"

    return errors
