# test_ldap.py
# -*- coding: utf-8  -*-

# Модуль логирования
import logging
# Настройки логирования
logging.basicConfig(filename='python_error.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s')

# Модуль для работы с LDAP
import ldap3

# Сразу тут же тест конвертации данных в JSON формат и для работы с config.json
# Импортируем модуль
import json


# try:

print ("Start!");
l = ldap3.initialize('LDAP://OU=Workstations,OU=Tayshet,OU=Bratsk,DC=HQ,DC=ROOT,DC=AD')


l.protocol_version = ldap.VERSION3
l.set_option(ldap.OPT_REFERRALS, 0)

# bind = l.simple_bind_s("me@example.com", "password")

base = "dc=HQ, dc=ROOT, dc=AD"
criteria = "(&(objectClass=computer)(sAMAccountName=username))"
attributes = ['displayName', 'company']
result = l.search_s(base, ldap.SCOPE_SUBTREE, criteria, attributes)

results = [entry for dn, entry in result if isinstance(entry, dict)]
print (results)

l.unbind()
    
    
    # storage = cgi.FieldStorage()
    # Получить значение того или иного параметра по его имени можно при помощи метода getvalue
    # worker_id = 0
    # staff_id = 90
    # target_staff_id = 1

    # # Переменная для хранения строки для возврата ответа
    # res = ''

    # # Проверка, действительно ли параметр содержит значение, и после обработки (при необходимости) направляем результат обратно клиенту.
    # if worker_id is not None and staff_id is not None and target_staff_id:
        # # print(data)

        # # Читаем из файла конфигурацию для подключения к БД
        # with open("../config.json", encoding='utf-8') as json_data_file:
            # conf_data = json.load(json_data_file)

        # # Соединение с БД
        # # port=int(data['mariadb']['port']) - тут приведение типа к integer, т.к.
        # # port должен быть integer
        # conn = mariadb.connect(
            # user=conf_data['mariadb']['user'],
            # password=conf_data['mariadb']['passwd'],
            # host=conf_data['mariadb']['host'],
            # port=int(conf_data['mariadb']['port']),
            # database=conf_data['mariadb']['db']
        # )

        # # dictionary=True - чтобы работать с результатом как с объектом (ассоциативным массивом)
        # cur = conn.cursor(dictionary=True)

        # # Если есть id сотрудника
        # if worker_id != 0:
            # query = "UPDATE spr_workers SET staff = ? WHERE id = ?"
            # args = [target_staff_id, worker_id]
            # # Выполним обновление данных о депаратаменте БД
            # cur.execute(query, args)
            # # После внесений изменений в БД всегда надо делать commit (!!! есть вариант делать autocommit, надо изучить)
            # conn.commit()

        # # Если есть id департамента
        # if staff_id != 0:

            # # id родителя
            # parent_id_now = 0
            # # кол-во элементов в этом родителе
            # node_count_now = 0

            # # Текущий департамент, где находится элемент
            # query = "SELECT id, node_count FROM spr_staff WHERE id iN (SELECT parent_id FROM spr_staff WHERE id = ?) LIMIT 1"
            # args = [staff_id]
            # # Запрос данных
            # cur.execute(query, args)

            # staff_rez = cur.fetchall()

            # # Если не пустой результат вернулся
            # if cur.rowcount != 0:
                # parent_id_now = staff_rez[0]['id'];
                # node_count_now = staff_rez[0]['node_count'];

            # # Если родитель указан не тот же самый, который был
            # if parent_id_now != target_staff_id:
                # # Если помещаем не в дочерний элемент
                # if not checkExistTreeParents ('spr_staff', staff_id, target_staff_id, conn):
                    # # Если бывший родитель указан и это не корень (0)
                    # if parent_id_now != 0:
                        # # Обновляем кол-во подкатегорий (node_count)
                        # query = "UPDATE spr_staff SET node_count = node_count - 1 WHERE id = ?"
                        # args = [parent_id_now]
                        # # Выполним обновление данных о депаратаменте БД
                        # cur.execute(query, args)
                        # # После внесений изменений в БД всегда надо делать commit (!!! есть вариант делать autocommit, надо изучить)
                        # conn.commit()
                        # print("Обновили старого родителя, так как он был")

                    # # Обновляем подкатегорию
                    # query = "UPDATE spr_staff SET parent_id = ? WHERE id = ?"
                    # args = [target_staff_id, staff_id]
                    # # Выполним обновление данных о депаратаменте БД
                    # cur.execute(query, args)
                    # # После внесений изменений в БД всегда надо делать commit (!!! есть вариант делать autocommit, надо изучить)
                    # conn.commit()

                    # # Обновляем кол-во подкатегорий (node_count)
                    # query = "UPDATE spr_staff SET node_count = node_count + 1 WHERE id = ?"
                    # args = [target_staff_id]
                    # # Выполним обновление данных о депаратаменте БД
                    # cur.execute(query, args)
                    # # После внесений изменений в БД всегда надо делать commit (!!! есть вариант делать autocommit, надо изучить)
                    # conn.commit()
                # else:
                    # print("Пытались поместить в дочерний элемент")
            # else:
                # print("Пытались поместить туда, где и были до того")

        # print("Конец!")

        # # Закрываем соединение
        # conn.close()
    # else:
        # # Работая с Python под WEB, нельзя забывать про вывод заголовков и указание кодировки
        # print('Status: 200 OK')
        # print('Content-Type: text/html')
        # print('')

        # # Результат в виде JSON (Пустой ответ)
        # print(json.dumps({"result": "success", "data": ""}))

# except Exception as e:
    # # Лог ошибок (!!! не уверен, что это лучшая реализация, но работает)
    # logging.error("Exception occurred", exc_info=True)
