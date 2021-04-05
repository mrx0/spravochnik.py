# worker_edit
# Редактируем существующего сотрудника

# Модуль логирования
import logging
# Настройки логирования
logging.basicConfig(filename='python_error.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s')

# Для доступа к данным поступившим в результате запроса в Python служит класс FieldStorage из модуля cgi.
# Импортируем его
import cgi

# Импортируем модуль работы с json
import json

# Импорт модуля для работы с MariaDB
import mariadb

try:
    storage = cgi.FieldStorage()
    # Получить значение того или иного параметра по его имени можно при помощи метода getvalue
    worker_id = storage.getvalue('worker_id')
    fio = storage.getvalue('worker_name')
    tab_nomer = storage.getvalue('tabel_nom')
    phone_personal = storage.getvalue('tel_own')
    employment_date = storage.getvalue('employment_date')
    birth = storage.getvalue('birth')
    email = storage.getvalue('email')
    login = storage.getvalue('login')
    password = storage.getvalue('password')
    staff = storage.getvalue('staff_id')
    staff_position = storage.getvalue('staff_position_id')
    # !!! wasInRusal пока нигде не используем
    wasInRusal = storage.getvalue('wasInRusal')

    # Работаем с базой
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

    cur = conn.cursor()

    # Добавляем сотрудника
    # Строка запроса
    query = """
        UPDATE spr_workers
        SET fio=%s, tab_nomer=%s, phone_personal=%s, employment_date=%s, birth=%s, email=%s, login=%s, password=%s, staff=%s, staff_position=%s
        WHERE
        id=%s
        """
    # print(query)

    # Запрос в БД
    cur.execute(query, (fio, tab_nomer, phone_personal, employment_date, birth, email, login, password, staff, staff_position,worker_id,))

    # После внесений изменений в БД всегда надо делать commit (!!! есть вариант делать autocommit, надо изучить)
    conn.commit()

    # Работая с Python под WEB, нельзя забывать про вывод заголовков и указание кодировки
    print('Status: 200 OK')
    print('Content-Type: text/html')
    print('')

    # Результат в виде JSON
    print(json.dumps({"result": "success", "data": ""}))

    # Закрываем соединение
    conn.close()

except Exception as e:
    # Лог ошибок (!!! не уверен, что это лучшая реализация, но работает)
    logging.error("Exception occurred", exc_info=True)