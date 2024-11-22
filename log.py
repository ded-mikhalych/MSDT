import logging
from collections import defaultdict

# Настройка логгирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("program.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def load_txt(file_path):
    # Загрузка данных из TXT-файла
    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            headers = file.readline().strip().split('\t')
            data = [dict(zip(headers, line.strip().split('\t'))) for line in file]
        logger.info(f"Файл '{file_path}' загружен успешно")
        return data
    except Exception as e:
        logger.error(f"Ошибка загрузки TXT: {e}")
        raise

def load_multiple_txt(file_paths):
    # Загрузка и объединение данных из нескольких txt файлов
    combined_data = []
    for file_path in file_paths:
        try:
            data = load_txt(file_path)
            combined_data.extend(data)
        except Exception as e:
            logger.error(f"Ошибка при обработке файла {file_path}: {e}")
    logger.info(f"Общий объем данных после объединения: {len(combined_data)} строк")
    return combined_data

def group_by_column(data, column):
    # Группировка данных по указанной колонке
    logger.info(f"Группировка данных по колонке '{column}'")
    grouped_data = defaultdict(list)
    try:
        for row in data:
            grouped_data[row[column]].append(row)
        logger.info(f"Создано {len(grouped_data)} групп")
        return grouped_data
    except KeyError:
        logger.error(f"Указанной колонки '{column}' нет в данных")
        raise

def filter_groups(grouped_data, min_size):
    # Фильтрация групп по минимальному размеру
    logger.info(f"Фильтрация групп с размером меньше {min_size}")
    filtered = {key: value for key, value in grouped_data.items() if len(value) >= min_size}
    logger.info(f"Осталось {len(filtered)} групп после фильтрации")
    return filtered

def sort_groups_by_size(grouped_data):
    # Сортировка групп по количеству записей в каждой
    logger.info("Сортировка групп по размеру")
    sorted_data = sorted(grouped_data.items(), key=lambda x: len(x[1]), reverse=True)
    return sorted_data

def save_to_txt(data, output_path):
    # Сохранение данных в txt файл
    try:
        # Разворачиваем данные обратно в список словарей
        flattened_data = [item for _, group in data for item in group]
        if len(flattened_data) == 0:
            logger.info("Нет данных для сохранения")
            return
        keys = flattened_data[0].keys()
        with open(output_path, mode='w', encoding='utf-8') as file:
            file.write('\t'.join(keys) + '\n')
            for row in flattened_data:
                file.write('\t'.join(str(row[key]) for key in keys) + '\n')
        logger.info(f"Успешно сохранено в '{output_path}'")
    except Exception as e:
        logger.error(f"Ошибка сохранения данных: {e}")
        raise

def main():
    # Ввод данных
    input_files = input("Введите пути к входным TXT-файлам (через запятую): ").strip()
    output_file = input("Введите путь к выходному TXT-файлу: ").strip()
    group_by = input("Введите колонку для группировки: ").strip()
    filter_size = input("Введите мин. размер группы для фильтрации: ").strip()

    file_list = input_files.split(",")
    # Преобразуем введенное значение в число
    filter_size = int(filter_size) if filter_size else None

    try:
        if len(file_list) > 1:
            data = load_multiple_txt(file_list)
        else:
            data = load_txt(file_list[0])
        grouped = group_by_column(data, group_by)
        if filter_size:
            grouped = filter_groups(grouped, filter_size)
        sorted_groups = sort_groups_by_size(grouped)
        save_to_txt(sorted_groups, output_file)

        logger.info("Программа успешно завершена")
    except Exception as e:
        logger.error(f"Ошибка выполнения программы: {e}")
        exit(1)

if __name__ == "__main__":
    main()
