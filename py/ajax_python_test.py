# -*- coding: utf-8  -*-

# Для доступа к данным поступившим в результате запроса в Python служит класс FieldStorage из модуля cgi.
# Импортируем его
import cgi

# Сразу тут же тест конвертации данных в JSON формат
# Импортируем модуль
import json

storage = cgi.FieldStorage()
# Получить значение того или иного параметра по его имени можно при помощи метода getvalue
data = storage.getvalue('data')

# Работая с Python под WEB, нельзя забывать про вывод заголовков и указание кодировки.
print('Status: 200 OK')
print('Content-Type: text/plain')
print('')

# Проверка, действительно ли параметр содержит значение, и после обработки (при необходимости) направляем результат обратно клиенту.
if data is not None:
    # print(data)
    # Результат в виде JSON
    print(json.dumps({"result": "success", "data": data}))