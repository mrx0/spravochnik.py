# # Module Imports
# import mariadb
# import sys
#
# # Connect to MariaDB Platform
# try: conn = mariadb.connect(
#     user="root",
#     password="gfhjkm84286252",
#     host="localhost",
#     port=3307,
#     database="spr_itgroup"
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

# Соединение с БД
conn = mariadb.connect(
    user="root",
    password="gfhjkm84286252",
    host="localhost",
    port=3307,
    database="spr_itgroup"
)

cur = conn.cursor()

# Запрос данных по условию
status = "9"
cur.execute("SELECT name FROM spr_types WHERE status <> ?", (status,))

# Выводим то, что получили
for (name) in cur:
    print(f"Name: {name}")

# Вставка записи
try:
    cur.execute("INSERT INTO spr_types (name) VALUES (?)", ("ЧТо-тО",))

except mariadb.Error as e:
    print(f"Error: {e}")

conn.commit()

# Последний вставленный ID в базу
print(f"Last Inserted ID: {cur.lastrowid}")

# Закрываем соединение с БД
conn.close()