# from_excel_to_db_sclad.py
# В ручном режиме запускается и добавляет из Excel в БД данные по оборудованию

# Модуль логирования
import logging
# Настройки логирования
logging.basicConfig(filename='../python_error.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s')

# Импортируем модуль работы с json
import json

# Импорт модуля для работы с MariaDB
import mariadb

# Импорт модуля для работы с Excel
import openpyxl

try:

    # Работаем с базой
    # Читаем из файла конфигурацию для подключения к БД
    with open("../config.json", encoding='utf-8') as json_data_file:
        conf_data = json.load(json_data_file)

    # Соединение с БД
    # port=int(data['mariadb']['port']) - тут приведение типа к integer, т.к.
    # port должен быть integer
    conn = mariadb.connect(
        user=conf_data['mariadb']['user'],
        password=conf_data['mariadb']['passwd'],
        host=conf_data['mariadb']['host'],
        port=int(conf_data['mariadb']['port']),
        database=conf_data['mariadb']['db']
    )

    # dictionary=True - чтобы работать с результатом как с объектом (ассоциативным массивом)
    cur = conn.cursor(dictionary=True)

    # Получаем типы оборудования
    # Строка запроса
    query = """SELECT * FROM spr_types db 
        WHERE db.status <> ? 
        ORDER BY db.id ASC
        """

    # Запрос данных
    cur.execute(query, [9])

    result = cur.fetchall()
    # print(result)

    # Будущий массив типов
    items_types = {}

    # Собираем то, что получили, в ассоциативный массив, где индексом будет имя
    # .lower() тут приводит регистр к нижнему для будущего удобного поиска
    for data in result:
        items_types[data['name'].lower()] = data
    # print(items_types)
    # print(items_types.get('пк'))
    # print(items_types['пк']['name'])

    # get(key) - по сути проверяет есть ли такой ключ в массиве, если есть
    # возвращает значение по этому ключу
    # Если нет, вернёт None
    # if items_types.get(key) is not None: ....

    # key in array проверяет есть ли такой ключ в массиве
    # Возвращает либо True либо False
    # print('пк' in items_types)

    # Создание объекта, читаем excel файл и присваиваем объекту книгу из файла.
    # data_only=True - берём только значения (не формулы)
    wb = openpyxl.reader.excel.load_workbook(filename="../excel/СПРАВОЧНИК_.xlsx", data_only=True)
    # Выводим массив с названиями листов вниги
    # print(wb.sheetnames)

    # Активируем лист по его индексу
    # 11 - ПК
    # 14 - Склад
    wb.active = 14

    # Обращаемся к листу через объект wb.active
    sheet = wb.active

    # Цикл, в котором выводим данные из листа sheet из всех ячеек A,B,C... c i по N строку
    # !!! Если меняешь лист, проверь range, они везде разные
    for i in range(4,524):
        # Для листа Склад
        # Тип
        type = sheet['J' + str(i)].value
        # Хост_имя / КУПСО
        host_name = sheet['G' + str(i)].value
        # Модель
        model = sheet['C' + str(i)].value
        # Если в модели "лишние" слова, например тип, то надо удалить
        # !!! задача решена в лоб, лень морочиться со сложными функциями
        if 'Блок сист.' in model:
            model = model.replace('Блок сист.', '')
        if 'Коммутатор' in model:
            model = model.replace('Коммутатор', '')
        if 'Монитор 22' in model:
            model = model.replace('Монитор 22', '')
        if 'Монитор ж/к' in model:
            model = model.replace('Монитор ж/к', '')
        if 'Монитор' in model:
            model = model.replace('Монитор', '')
        if 'МФУ' in model:
            model = model.replace('МФУ', '')
        if 'ноутбук' in model:
            model = model.replace('ноутбук', '')
        if 'Ноутбук' in model:
            model = model.replace('Ноутбук', '')
        if 'персональный компьютер' in model:
            model = model.replace('персональный компьютер', '')
        if 'Компьютер' in model:
            model = model.replace('Компьютер', '')
        if 'ПК' in model:
            model = model.replace('ПК', '')
        if 'Принтер' in model:
            model = model.replace('Принтер', '')
        if 'широкоформатный' in model:
            model = model.replace(' широкоформатный', '')
            model = model+' широкоформатный'
        # Удаляем пробелы в начале и в конце строки
        model = model.strip()


        # Серийный №
        serial_num = sheet['D' + str(i)].value
        # Если серийник не указан или равен 0, будет просто пустой
        if serial_num == 'не указан' or serial_num == '0':
            serial_num = ''
        # ИНВ №
        invent_num_old = sheet['E' + str(i)].value
        # ИНВ № ПТР
        invent_num = sheet['F' + str(i)].value


        # # !!! Для листа ПК
        # # Тип
        # type = sheet['B' + str(i)].value
        # # Хост_имя / КУПСО
        # host_name = sheet['C' + str(i)].value
        # # Модель
        # model = sheet['D' + str(i)].value
        # # Серийный №
        # serial_num = sheet['E' + str(i)].value
        # # состояние
        # state = sheet['F' + str(i)].value
        # # ФИО
        # fio = sheet['G' + str(i)].value
        # # ИНВ №
        # invent_num_old = sheet['H' + str(i)].value
        # # ИНВ № ПТР
        # invent_num = sheet['I' + str(i)].value
        # # Столбец2
        # col2 = sheet['J' + str(i)].value
        # # Примечания
        # comment = sheet['K' + str(i)].value
        # # группа
        # group = sheet['L' + str(i)].value
        # # МОЛ
        # mol = sheet['M' + str(i)].value
        # # Столбец12
        # col12 = sheet['N' + str(i)].value
        # # удаленка
        # remote = sheet['O' + str(i)].value
        # # расположение
        # place = sheet['P' + str(i)].value
        # # в_ПТР
        # ptr = sheet['Q' + str(i)].value
        # # Столбец3
        # col3 = sheet['R' + str(i)].value

        # Тут можно уже работать с БД
        # Но пока просто выведем всё это в консоль
        # print (type ' -> ' + model + ' -> ' + host_name + ' -> ' + serial_num + ' -> ' + invent_num_old + ' -> ' + invent_num + ' -> ' + fio)
        # print (type, model, host_name, serial_num, invent_num_old, invent_num, fio)
        # print(type + ' => ', model, host_name, serial_num, invent_num_old, invent_num)

        # Если у нас в БД есть такой тип, далее работает с этим типом
        # !!! Все типы я уже добавил в базу вручную, нет смысла писать код автоматического добавления их в БД из Excel
        if type.lower() in items_types:
            # Сначала проверим, нет ли уже такого. Если есть, то возьмём его id
            # Получаем модель оборудования
            # Строка запроса
            query = """SELECT * FROM spr_models db
                WHERE db.name = ?
                ORDER BY db.id ASC
                """

            # Запрос данных
            cur.execute(query, [model])

            result = cur.fetchone()
            # print(result)

            # Модели нет в базе
            if result == None:
                # Добавляем её
                # Будем добавлять модели в БД
                # Строка запроса
                query = """
                    INSERT INTO spr_models
                    (type_id, name)
                    VALUES
                    (?, ?)
                    """

                # Запрос в БД
                cur.execute(query, [items_types[type.lower()]['id'], model])

                model_id = cur.lastrowid
                model_name = model

                # После внесений изменений в БД всегда надо делать commit (!!! есть вариант делать autocommit, надо изучить)
                conn.commit()

            # Модель уже есть в базе, получаем её id и name для дальнейшего использования
            else:
                model_id = result['id']
                model_name = result['name']
                # print(model_id)
                # print(model_name)


        # Теперь можно добавлять оборудование
        # !!! пока без того, на ком числится
        # Строка запроса
        query = """
            INSERT INTO spr_items
            (model_id, model_name, type_id, type_name, serial, host_name, invent, invent_old)
            VALUES
            (?, ?, ?, ?, ?, ?, ?, ?)
            """

        # Запрос в БД
        cur.execute(query, [model_id, model_name, items_types[type.lower()]['id'], items_types[type.lower()]['name'], serial_num, host_name, invent_num, invent_num_old])

        # После внесений изменений в БД всегда надо делать commit (!!! есть вариант делать autocommit, надо изучить)
        conn.commit()


    # Закрываем соединение
    conn.close()

except Exception as e:
    # Лог ошибок (!!! не уверен, что это лучшая реализация, но работает)
    logging.error("Exception occurred", exc_info=True)