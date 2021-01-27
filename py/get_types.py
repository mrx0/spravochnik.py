# -*- coding: utf-8  -*-

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
    req_data = storage.getvalue('flag')

    # Переменная для хранения строки для возврата ответа
    res = ''

    # Проверка, действительно ли параметр содержит значение, и после обработки (при необходимости) направляем результат обратно клиенту.
    if req_data is not None:
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
        query = """SELECT * FROM spr_types db 
            WHERE db.status <> ? 
            ORDER BY db.id ASC
            """

        # Запрос данных
        cur.execute(query, [9])

        result = cur.fetchall()

        # Собираем то, что получили, в одну строку для возврата обратно в Ajax
        for data in result:
            res += ''+data['name']+''
            # print(data['name'])

        # Работая с Python под WEB, нельзя забывать про вывод заголовков и указание кодировки
        print('Status: 200 OK')
        print('Content-Type: text/html')
        print('')

        # Результат в виде JSON
        print(json.dumps({"result": "success", "data": result}))

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