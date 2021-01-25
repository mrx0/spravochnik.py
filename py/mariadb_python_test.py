# # Module Imports
# import mariadb
# import sys
#
# # Connect to MariaDB Platform
# try: conn = mariadb.connect(
#     user="",
#     password="",
#     host="",
#     port=,
#     database=""
# )
# except mariadb.Error as e:
#     print(f"Error connecting to MariaDB Platform: {e}")
#     sys.exit(1)
#
# # Get Cursor
# cur = conn.cursor()
#
# cur.execute(
#     "SELECT name FROM spr_types WHERE status <> ?",
#     ('9',))
#
# # Print Result-set
# for (name) in cur:
#     print(f"Name: {name}")



# !/usr/bin/python
# Импорт модуля для работы с MariaDB
import mariadb
# импортируем библиотеку JSON для работы с config.json
import json

# Читаем из файла
with open("../config.json") as json_data_file:
    data = json.load(json_data_file)
# Выводим на экран
# print(data)
# print(data['mariadb'])
# print(data['mariadb']['host'])


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

cur = conn.cursor(dictionary=True)

# Запрос данных по условию
status = "9"
cur.execute("""
    SELECT * FROM spr_types 
    WHERE status <> ?
    """, (status,))

# Метод fetchone возвращает одну строку данных
#result = cur.fetchone()
#print(result)

# Метод fetchall возвращает все строки в виде списка
result = cur.fetchall()

# Выводим то, что получили
for data in result:
    print(data['id'])



# # Вставка записи
# try:
#     cur.execute("INSERT INTO spr_types (name) VALUES (?)", ("ЧТо-тО",))
#
# except mariadb.Error as e:
#     print(f"Error: {e}")
#
# # После внесений изменений в БД всегда надо делать commit (!!! есть вариант делать autocommit, надо изучить)
# conn.commit()
#
# # Последний вставленный ID в базу
# print(f"Last Inserted ID: {cur.lastrowid}")

# Закрываем соединение с БД
conn.close()