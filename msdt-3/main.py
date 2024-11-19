import csv
import re

from mypy.server.objgraph import Iterable

from checksum import (
    calculate_checksum,
    serialize_result
)


def is_row_valid(row: dict[str, str]):
    processors = {
        # Типичный имейл. Состоит из латинских букв, цифр, символов "." и "@". Обратите внимание, что адрес может иметь поддомен.
        "email": r"\w+@\w+\.\w+",
        # Статус должен начинаться с трехзначного кода, отделенного пробелом от текстового описания.
        "http_status_message": r"\d{3} .+",
        # ИНН состоит из 12 цифровых символов. В данном задании символы ИНН они указаны подряд без пробелов/тире и т.д.
        "inn": r"\d{12}",
        # В данном задании пробелами разделены первые 2 и последние 2 цифры серии, а также серия и номер паспорта.
        "passport": r"\d{2} \d{2} \d{6}",
        # IP-адрес указывается без маски подсети. Не забывайте, что он 32-битный.
        "ip_v4": r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",
        # Это широта в системе координат WGS84 (srid 4326). Обратите внимание на ограничения на значение, которые она имеет. Должна быть числовым значением без единиц измерения и прочей текстовой информации.
        "latitude": r"-?((?:[1-8]\d|\d)\.\d{1,6}|90.0)",
        # Это представление веб-цвета в виде трех пар 16-ричных цифр. Наличие хештега перед ними обязательно.
        "hex_color": r"#[\dabcdef]{6}",
        # 13-значный международный стандартный книжный номер
        "isbn": r"(\d{3}-)?\d-\d{5}-\d{3}-\d",
        # Всемирно уникальный идентификатор в каноническом представлении
        "uuid": r"[\dabcdef]{8}-[\dabcdef]{4}-[\dabcdef]{4}-[\dabcdef]{4}-[\dabcdef]{12}",
        # Время определенного формата с указанием часов, минут и секунд с точностью до 6 знаков. Не забывайте, что в сутках 24 часа, а в минуте - 60 секунд.
        "time": r"(?:2[0-4]|[01]\d):[0-6]\d:[0-6]\d.\d{6}",
    }
    for field_name, processor in processors.items():
        if re.fullmatch(processor, row[field_name]) is None:
            return False
    return True


def get_wrong_lines() -> Iterable[int]:
    with open("93.csv", mode="r", encoding="utf16", newline="") as file_to_validate:
        strings_reader = csv.DictReader(file_to_validate, delimiter=';')
        for i, row in enumerate(strings_reader):
            if not is_row_valid(row):
                yield i


def main():
    lines = list(get_wrong_lines())
    variant = 93
    checksum = calculate_checksum(lines)
    serialize_result(variant, checksum)


if __name__ == '__main__':
    main()
