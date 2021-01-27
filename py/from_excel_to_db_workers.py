# from_excel_to_db_workers.py
# В ручном режиме запускается и добавляет из Excel в БД данные по сотрудникам

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

    # Получаем все отделы
    # Строка запроса
    query = """SELECT * FROM spr_staff db
        WHERE db.status <> ?
        ORDER BY db.id ASC
        """

    # Запрос данных
    cur.execute(query, [9])

    result = cur.fetchall()
    # print(result)

    # Будущий массив отделов
    staffs = {}

    # Собираем то, что получили, в ассоциативный массив, где индексом будет имя
    # .lower() тут приводит регистр к нижнему для будущего удобного поиска
    for data in result:
        staffs[data['name'].lower()] = data
    # print(staffs)
    # print(staffs.get('птр'))
    # print(staffs['птр']['name'])

    # get(key) - по сути проверяет есть ли такой ключ в массиве, если есть
    # возвращает значение по этому ключу
    # Если нет, вернёт None
    # if staffs.get(key) is not None: ....

    # key in array проверяет есть ли такой ключ в массиве
    # Возвращает либо True либо False
    # print('птр' in staffs)


    # Получаем все должности
    # Строка запроса
    query = """SELECT * FROM spr_staff_positions db
        WHERE db.status <> ?
        ORDER BY db.id ASC
        """

    # Запрос данных
    cur.execute(query, [9])

    result = cur.fetchall()
    # print(result)

    # Будущий массив должностей
    staff_positions = {}

    # Собираем то, что получили, в ассоциативный массив, где индексом будет имя
    # .lower() тут приводит регистр к нижнему для будущего удобного поиска
    for data in result:
        staff_positions[data['name'].lower()] = data
    # print(staff_positions)
    # print(staff_positions.get('птр'))
    # print(staff_positions['птр']['name'])


    # Создание объекта, читаем excel файл и присваиваем объекту книгу из файла.
    # data_only=True - берём только значения (не формулы)
    wb = openpyxl.reader.excel.load_workbook(filename="../excel/СПРАВОЧНИК_.xlsx", data_only=True)
    # Выводим массив с названиями листов вниги
    # print(wb.sheetnames)

    # Активируем лист по его индексу
    # 11 - ПК
    # 14 - Склад
    # 2 - ШР
    wb.active = 2

    # Обращаемся к листу через объект wb.active
    sheet = wb.active

    # Переменная, в которую будем фиксировать отдел
    temp_staff = ''

    # Цикл, в котором выводим данные из листа sheet из всех ячеек A,B,C... c i по N строку
    # !!! Если меняешь лист, проверь range, они везде разные
    for i in range(5,609):
        # Для листа ШР

        # Переменная, в которую будем фиксировать должность
        temp_staff_position = ''

        # Отдел 0 уровня
        staff0 = sheet['B' + str(i)].value
        # Если дошли до отдела "_", выскакиваем из цикла
        if staff0 == '_':
            break

        # Если в отделе "лишние" слова, то надо удалить
        # !!! задача решена в лоб, лень морочиться со сложными функциями
        if staff0 != None:
            if '(ПТР)' in staff0:
                staff0 = staff0.replace('(ПТР)', '')

        # Отдел 1 уровня
        staff1 = sheet['D' + str(i)].value
        # Должность 1
        staff_position1 = sheet['H' + str(i)].value
        # Должность 2
        staff_position2 = sheet['I' + str(i)].value
        # Если пустая строка
        if staff_position2 == None:
            staff_position2 = '';
            temp_staff_position = staff_position1
        else:
            # У генерального директора порядок слов в должности стоят в excel в обратном порядке, учтём
            # !!! такая же история у 'мастер старший', 'Директор	технический',
            # 'Начальник И.о.', 'руководитель И.о.' и 'энергетик главный'
            # потом просто в БД поменять на нормальное просто
            # !!! Если файл будет перезаливаться другой, надо не забыть в нём привести всё к одному виду
            # например в должностях, где есть дефис, поставить пробелы справа и слева
            if staff_position2 == 'генеральный':
                temp_staff_position = staff_position2.strip() + ' ' + staff_position1.strip()
                # print (temp_staff_position)
                # print (staff_positions[temp_staff_position.lower()])
                # print (temp_staff_position.lower() in staff_positions)
            else:
                temp_staff_position = staff_position1.strip() + ' ' + staff_position2.strip()

        # ФИО
        fio = sheet['J' + str(i)].value
        # Тел
        phone_personal = sheet['K' + str(i)].value
        # Пустой телефон будет пустым
        if phone_personal == '-':
            phone_personal = ''
        # Статус (уволен или нет)
        status = sheet['M' + str(i)].value
        # Сразу присвоим уволенным программный статус 8 для БД
        if status == 'уволен':
            status = 8
        else:
            status = 0

        # Если отдел 0 уровня присутствует, ведём его для сотрудников, пока не встретится следующий 0 или 1
        if staff0 != None:
            temp_staff = staff0

        # Если отдел 1 уровня попадается, ведём его для сотрудников, пока не встретится следующий 0 или 1
        if staff1 != None:
            temp_staff = staff1

        # Удаляем пробелы в начале и в конце строки
        temp_staff = temp_staff.strip()

        # Тут можно уже работать с БД
        # Но пока просто выведем всё это в консоль
        # Если нет ФИО, то и выводить ничего не будем
        if fio != None:
            # print(temp_staff + '/', staff_position1 + ' ', staff_position2, '!' + fio + '!', '[' + str(phone_personal) + ']')
            # Проверка, есть ли в БД такой отдел
            # if temp_staff.lower() in staffs:
            #     print('+')
            # else:
            #     print('-')
            #     print(temp_staff, temp_staff_position, fio, phone_personal)


            # Если у нас в БД есть такой отдел, далее работаем с этим отделом
            # !!! Все отделы я уже добавил в базу вручную, нет смысла писать код автоматического добавления их в БД из Excel
            if temp_staff.lower() in staffs:
                # Если у нас в БД есть такая должность, далее работаем с этой должностью
                # !!! Все должности я уже добавил в базу вручную, нет смысла писать код автоматического добавления их в БД из Excel
                if temp_staff_position.lower() in staff_positions:

                    staff_id = staffs[temp_staff.lower()]['id']
                    staff_position_id = staff_positions[temp_staff_position.lower()]['id']

                    # Теперь можно добавлять сотрудника
                    # !!! пока без табельника и другой фигни
                    # Строка запроса
                    query = """
                        INSERT INTO spr_workers
                        (fio, staff_position, staff, phone_personal, status)
                        VALUES
                        (?, ?, ?, ?, ?)
                        """
                    # print(query)

                    # Запрос в БД
                    cur.execute(query, [fio, staff_position_id, staff_id, phone_personal, status])

                    # После внесений изменений в БД всегда надо делать commit (!!! есть вариант делать autocommit, надо изучить)
                    conn.commit()

            # Ниже выведем то, что не нашлось, чтоб потом добавить значения и перепрогнать еще раз файл
            # Это (проверку) можно делать без добавления всех данных в БД, закомментировав выше запрос
                else:
                    print('Не нашёл должность');
                    print(temp_staff, temp_staff_position, fio, phone_personal)
            else:
                print('Не нашёл отдел');
                print(temp_staff, temp_staff_position, fio, phone_personal)


    # Закрываем соединение
    conn.close()

except Exception as e:
    # Лог ошибок (!!! не уверен, что это лучшая реализация, но работает)
    logging.error("Exception occurred", exc_info=True)