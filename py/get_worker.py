# get_worker.py
# -*- coding: utf-8  -*-
# Получаем данные по сотруднику

# Модуль логирования
import logging
# Настройки логирования
logging.basicConfig(filename='python_error.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s')

# Для доступа к данным поступившим в результате запроса в Python служит класс FieldStorage из модуля cgi.
# Импортируем его
import cgi

import datetime

# Сразу тут же тест конвертации данных в JSON формат и для работы с config.json
# Импортируем модуль
import json

# Импорт модуля для работы с MariaDB
import mariadb

try:
    storage = cgi.FieldStorage()
    # Получить значение того или иного параметра по его имени можно при помощи метода getvalue
    req_data = storage.getvalue('worker_id')

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
        query = """SELECT 
            s_w.fio, s_w.tab_nomer, s_w.phone_personal, s_w.employment_date, s_w.birth, s_w.email, s_w.login, s_w.password, 
            st.id AS st_id, st.name AS st_name, st_pos.id AS pos_id, st_pos.name AS pos_name, 
            s_w.status 
            FROM spr_workers s_w
            LEFT JOIN spr_staff st ON st.id = s_w.staff
            LEFT JOIN spr_staff_positions st_pos ON st_pos.id = s_w.staff_position
            WHERE s_w.id = """+req_data+""" LIMIT 1"""

        # args = (req_data,)

        # Запрос данных
        # 2021-04-04  !!! ёбаная хуйня не работает как надо блэт! Или я тупой...
        # Если убирать из запроса s_w.employment_date и s_w.birth, то будет работать нормально, а с ними полный пиздец
        # хз, что-то там с JSON наверное, да и хуй с ним, я заебался разбираться, потом
        # cur.execute(query, (req_data,))
        cur.execute(query)

        result = cur.fetchone()

        # Собираем то, что получили, в одну строку для возврата обратно в Ajax
        # for data in result:
        #     # Если пусто БД, значит пустая строка (!!! пока, потом какой-то маркер добавить)
        #     if data['tab_nomer'] is None:
        #         data['tab_nomer'] = '<span style="color: red">не указан</span>'
        #     if data['phone_personal'] is None or data['phone_personal'] == '':
        #         data['phone_personal'] = '<span style="color: grey">не указан</span>'
        #     if data['pos_name'] is None or data['pos_name'] == '':
        #         data['pos_name'] = '<span style="color: grey">не указана</span>'
        #     if data['phone_personal'] is None or data['phone_personal'] == '':
        #         data['phone_personal'] = '<span style="color: grey">не указан</span>'
        #
        #     res += '''
        #                     <tr class="draggable worker_item_tr" data-uid="workerId_''' + str(data['id']) + '''" role="row">
        #                         <td class="" role="gridcell" style="border-left: 1px solid #CCC;">
        #                             <div style="position: relative; margin-left: auto; margin-right: auto; cursor:pointer;">
        #                                 <div style="margin:auto;" title="">
        #                                     ''' + data['fio'] + '''
        #                                 </div>
        #                             </div>
        #                         </td>
        #                         <td class="" role="gridcell" style="border-left: none;">
        #                             <div style="position: relative; margin-left: auto; margin-right: auto; cursor:pointer;">
        #                                 <div style="margin:auto; overflow: hidden; white-space: nowrap; text-overflow: ellipsis;" title="">
        #                                     ''' + str(data['tab_nomer']) + '''
        #                                 </div>
        #                             </div>
        #                         </td>
        #                         <td class="" role="gridcell" style="border-left: none;">
        #                             <div style="position: relative; margin-left: auto; margin-right: auto; cursor:pointer;">
        #                                 <div style="margin:auto; overflow: hidden; white-space: nowrap; text-overflow: ellipsis;" title="">
        #                                     ''' + data['pos_name'] + '''
        #                                 </div>
        #                             </div>
        #                         </td>
        #                         <td data-copymenu="true" class="" role="gridcell" style="border-left: none;">
        #                             <div style="position: relative; margin-left: auto; margin-right: auto; cursor:pointer;">
        #                                 <div id="NOM_DEMAND" style="margin:auto; cursor: pointer; color: rgb(25, 132, 200);" title="">
        #                                     ''' + str(data['phone_personal']) + '''
        #                                 </div>
        #                             </div>
        #                         </td>
        #                     </tr>
        #                     '''

        # Работая с Python под WEB, нельзя забывать про вывод заголовков и указание кодировки
        print('Status: 200 OK')
        print('Content-Type: text/html')
        print('')

        # Результат в виде JSON
        print(json.dumps({"result": "success", "data": result}, default=str))

        # Закрываем соединение
        conn.close()
    else:
        # Работая с Python под WEB, нельзя забывать про вывод заголовков и указание кодировки
        print('Status: 200 OK')
        print('Content-Type: text/html')
        print('')

        # Результат в виде JSON (Пустой ответ)
        print(json.dumps({"result": "error", "data": ""}))

except Exception as e:
    # Лог ошибок (!!! не уверен, что это лучшая реализация, но работает)
    logging.error("Exception occurred", exc_info=True)