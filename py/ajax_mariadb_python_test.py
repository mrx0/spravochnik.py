# -*- coding: utf-8  -*-

# Модуль логирования
import logging
logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')


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
    data = storage.getvalue('data')

    # Переменная для хранения строки для возврата ответа
    res = '';

    # Проверка, действительно ли параметр содержит значение, и после обработки (при необходимости) направляем результат обратно клиенту.
    if data is not None:
        # print(data)

        # Читаем из файла конфигурацию для подключения к БД
        with open("../config.json") as json_data_file:
            req_data = json.load(json_data_file)

        # Соединение с БД
        # port=int(data['mariadb']['port']) - тут приведение типа к integer, т.к.
        # port должен быть integer
        conn = mariadb.connect(
            user=data['mariadb']['user'],
            password=data['mariadb']['passwd'],
            host=data['mariadb']['host'],
            port=int(data['mariadb']['port']),
            database=data['mariadb']['db']
        )

        # dictionary=True - чтобы работать с результатом как с объектом (ассоциативным массивом)
        cur = conn.cursor(dictionary=True)

        # Запрос данных
        cur.execute("""
            SELECT * FROM spr_types db 
            WHERE db.name 
            LIKE ? AND db.status <> ? 
            ORDER BY db.name ASC 
            LIMIT 10
            """, (req_data,9,))

        result = cur.fetchall()

        # Собираем то, что получили, в одну строку для возврата обратно в Ajax
        for data in result:
            res += data['name']+' '
            print(data['name'])+' '

        # Работая с Python под WEB, нельзя забывать про вывод заголовков и указание кодировки
        print('Status: 200 OK')
        print('Content-Type: text/html')
        print('')

        # Результат в виде JSON
        print(json.dumps({"result": "success", "data": res}))
    else:
        # Работая с Python под WEB, нельзя забывать про вывод заголовков и указание кодировки
        print('Status: 200 OK')
        print('Content-Type: text/html')
        print('')

        # Результат в виде JSON
        print(json.dumps({"result": "success", "data": ""}))
except Exception as e:
  logging.error("Exception occurred", exc_info=True)