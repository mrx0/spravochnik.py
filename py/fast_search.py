# fast_search.py
# -*- coding: utf-8  -*-
# Быстрый поиск в бд

# Модуль логирования
import logging
# Настройки логирования
logging.basicConfig(filename='python_error.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s')

# Для доступа к данным поступившим в результате запроса в Python служит класс FieldStorage из модуля cgi.
# Импортируем его
import cgi

# Сразу тут же тест конвертации данных в JSON формат и для работы с config.json
# Импортируем модуль
import json

# Импорт модуля для работы с MariaDB
import mariadb

try:
    storage = cgi.FieldStorage()
    # Получить значение того или иного параметра по его имени можно при помощи метода getvalue
    searchdata = storage.getvalue('searchdata')
    target = storage.getvalue('target')

    # Переменная для хранения строки для возврата ответа
    res = ''
    # Маркер, что можно делать запрос
    ican = False

    # Проверка, действительно ли параметр содержит значение, и после обработки (при необходимости) направляем результат обратно клиенту.
    if searchdata is not None and target is not None:
        # print(data)

        # Читаем из файла конфигурацию для подключения к БД
        with open("./config.json", encoding='utf-8') as json_data_file:
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

        # Строка запроса
        if target == "staff":
            query = "SELECT db.* FROM `spr_staff` db WHERE db.name LIKE %s AND db.status <> %s ORDER BY db.name ASC LIMIT 5;"
            ican = True

        if target == "staff_position":
            query = "SELECT db.* FROM `spr_staff_positions` db WHERE db.name LIKE %s AND db.status <> %s ORDER BY db.name ASC LIMIT 5;"
            ican = True

        if ican:
            # Запрос данных
            cur.execute(query, ("%" + searchdata + "%",9,))

            result = cur.fetchall()

            # Собираем то, что получили, в одну строку для возврата обратно в Ajax
            for data in result:
                # Если пусто БД, значит пустая строка (!!! пока, потом какой-то маркер добавить)
                res += "<li id = '"+str(data['id'])+"' data-type='"+ target +"'>" + data['name'] + " </li>"
                # res += "<option value='" + data['name'] + "' style='font-size: 10%'>"

        # Работая с Python под WEB, нельзя забывать про вывод заголовков и указание кодировки
        print('Status: 200 OK')
        print('Content-Type: text/html')
        print('')

        # Результат в виде JSON
        print(json.dumps({"result": "success", "data": res}))

        # Закрываем соединение
        conn.close()
    else:
        # Работая с Python под WEB, нельзя забывать про вывод заголовков и указание кодировки
        print('Status: 200 OK')
        print('Content-Type: text/html')
        print('')

        # Результат в виде JSON (Пустой ответ)
        print(json.dumps({"result": "success", "data": ""}))

except Exception as e:
    # Лог ошибок (!!! не уверен, что это лучшая реализация, но работает)
    logging.error("Exception occurred", exc_info=True)