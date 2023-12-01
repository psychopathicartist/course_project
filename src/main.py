from utils.utils import *

if __name__ == "__main__":
    # Чтение файла
    operations = json_file_load('../operations.json')

    # Запись и сортировка списка с датами
    sorted_operations_date = date_list_make_and_sort(operations)

    # Выбор пяти последних операций
    newest_operations = newest_operation_selection(sorted_operations_date, operations)

    # Преобразование данных к необходимому виду
    for newest_operation in newest_operations:
        newest_operation["date"] = date_conversion(newest_operation)
        newest_operation["from"] = from_and_to_conversion(newest_operation, "from")
        newest_operation["to"] = from_and_to_conversion(newest_operation, "to")
        newest_operation["operationAmount"] = amount_conversion(newest_operation)
        # Вывод
        newest_operation_print(newest_operation)
