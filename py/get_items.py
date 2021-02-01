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
    req_data = storage.getvalue('type')

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
        query = """SELECT * FROM spr_items db 
            WHERE db.type_id = ? AND db.status <> ? 
            ORDER BY db.model_name ASC
            """

        args = [req_data, 9]

        # Если получили type == 0, значит надо показать Все элементы
        if req_data == '0':
            query = """SELECT * FROM spr_items db 
                WHERE db.status <> ? 
                ORDER BY db.model_name ASC
                """

            args = [9]

        # Запрос данных
        cur.execute(query, args)

        result = cur.fetchall()

        # Собираем то, что получили, в одну строку для возврата обратно в Ajax
        for data in result:
            # Если пусто БД, значит пустая строка (!!! пока, потом какой-то маркер добавить)
            if data['invent'] is None:
                data['invent'] = '<span style="color: red">не указан</span>'
            if data['serial'] is None or data['serial'] == '0':
                data['serial'] = '<span style="color: red">не указан</span>'
            if data['host_name'] is None:
                data['host_name'] = ''

            res += '''
                            <tr data-uid="''' + str(data['id']) + '''" role="row">
                                <td class="" role="gridcell">
                                    <div style="display: flex; position: relative; margin-left: auto; margin-right: auto; cursor:pointer;">
                                        <div style="margin:auto;" title="">
                                            ''' + data['type_name'] + '''
                                        </div>
                                    </div>
                                </td>
                                <td class="" role="gridcell">
                                    <div style="display: flex; position: relative; margin-left: auto; margin-right: auto; cursor:pointer;">
                                        <div style="margin:auto; overflow: hidden; white-space: nowrap; text-overflow: ellipsis;" title="''' + data['model_name'] + '''">
                                            ''' + data['model_name'] + '''
                                        </div>
                                    </div>
                                </td>
                                <td data-copymenu="true" class="" role="gridcell">
                                    <div style="display: flex; position: relative; margin-left: auto; margin-right: auto; cursor:pointer;">
                                        <div id="NOM_DEMAND" style="margin:auto; cursor: pointer; color: rgb(25, 132, 200);" title="">
                                            ''' + str(data['invent']) + '''
                                        </div>
                                    </div>
                                </td>
                                <td class="" role="gridcell">
                                    <div style="margin:auto; overflow: hidden; white-space: nowrap; text-overflow: ellipsis;" title="">
                                        ''' + data['serial'] + '''
                                    </div>
                                </td>
                                <td class="" role="gridcell">
                                    <div style="display: flex; position: relative; margin-left: auto; margin-right: auto; cursor:pointer;">
                                        <div style="margin:auto;" title="">
                                            ''' + data['host_name'] + '''
                                        </div>
                                    </div>
                                </td>
                                <td class="" role="gridcell">
                                    <div id="NOM_DEMAND" style="cursor: pointer; color: rgb(25, 132, 200);" title="-=ФИО=-">
                                        -=ФИО=-
                                    </div>
                                </td>
                                <td class="" role="gridcell">
                                    <div class="note">
                                        -=коммент=-
                                    </div>
                                </td>
                            </tr>
                            '''

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