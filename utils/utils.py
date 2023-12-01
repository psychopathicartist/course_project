import json
import datetime


def json_file_load(file_name):
    '''
    Возвращает список словарей из файла формата json
    '''
    with open(file_name, 'r', encoding='utf-8') as file:
        return json.load(file)


def date_list_make_and_sort(operations_):
    '''
    Создает и возвращает список из дат по всем операциям, отсортированный по новизне
    '''
    date_operation = []
    for operation in operations_:
        if operation != {}:
            date_operation.append(operation["date"][:10])
    dates = [datetime.datetime.strptime(ts, "%Y-%m-%d") for ts in date_operation]
    dates.sort()
    sorted_dates = [datetime.datetime.strftime(ts, "%Y-%m-%d") for ts in dates]
    sorted_dates.reverse()
    return sorted_dates


def newest_operation_selection(sorted_dates, operations_):
    '''
    Возвращает список словарей по пяти последним выполненнм операциям
    '''
    new_operations = []
    for i in sorted_dates:
        for operation in operations_:
            if operation != {} and i in operation["date"] and operation["state"] == 'EXECUTED':
                new_operations.append(operation)
        if len(new_operations) == 5:
            break
    return new_operations


def date_conversion(newest_operation_):
    '''
    Преобразует значения даты операции к виду:
    ДД.ММ.ГГГГ
    '''
    operations_date = newest_operation_["date"][:10]
    operations_date = operations_date.split("-")
    operations_date.reverse()
    operations_date = '.'.join(operations_date)
    return operations_date


def from_and_to_conversion(newest_operation_, key_name):
    '''
    Определяет и преобразует значения номера карты или счета операции к виду:
    XXXX XX** **** XXXX для карты
    **XXXX для счета
    '''
    if "from" in newest_operation_.keys():
        operations_from = newest_operation_[key_name].split(" ")
        operations_from_number = operations_from[-1]
        if len(operations_from_number) == 16:
            operations_from_number = operations_from_number[:6] + '*' * 6 + operations_from_number[-4:]
            operations_from_number = ' '.join(operations_from_number[i*4:(i+1)*4] for i in range(4))
        if len(operations_from_number) == 20:
            operations_from_number = '*' * 2 + operations_from_number[-4:]
        operations_from[-1] = operations_from_number
        operations_from = ' '.join(operations_from)
    else:
        operations_from = None
    return operations_from


def amount_conversion(newest_operation_):
    '''
    Преобразует значения суммы операции и валюты к виду:
    <сумма перевода> <валюта>
    '''
    operations_amount = newest_operation_["operationAmount"]["amount"] + ' '
    operations_amount += newest_operation_["operationAmount"]["currency"]["name"]
    return operations_amount


def newest_operation_print(new_operation_):
    '''
    Выводит результат по каждой операции по форме:
    <дата перевода> <описание перевода>
    <откуда> -> <куда>
    <сумма перевода> <валюта>
    '''
    print(f'''{new_operation_["date"]} {new_operation_["description"]}
{new_operation_["from"]} -> {new_operation_["to"]}
{new_operation_["operationAmount"]}
''')
