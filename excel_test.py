# Импорт модуля для работы с Excel
import openpyxl
# Создание объекта, читаем файл и присваиваем объекту книгу из файла.
# data_only=True - берём только значения (не формулы)
wb = openpyxl.reader.excel.load_workbook(filename="СПРАВОЧНИК_.xlsx", data_only=True)
# Выводим массив с названиями листов вниги
print(wb.sheetnames)
# Активируем лист по его индексу
# 11 - ПК
wb.active = 11
# Обращаемся к листу через объект wb.active
sheet = wb.active

#print​(sheet['A1'].value)
# for i in range(8,351):
#     print(sheet['A'+str(i)].value,sheet['B'+str(i)].value,sheet['C'+str(i)].value)

# Цикл, в котором выводим данные из листа sheet из всех ячеек A,B,C... c i по N строку
for i in range(8,352):
    # Тип
    type = sheet['B' + str(i)].value
    # Хост_имя / КУПСО
    host_name = sheet['C' + str(i)].value
    # Модель
    model = sheet['D' + str(i)].value
    # Серийный №
    serial_num = sheet['E' + str(i)].value
    # состояние
    state = sheet['F' + str(i)].value
    # ФИО
    fio = sheet['G' + str(i)].value
    # ИНВ №
    invent_num_old = sheet['H' + str(i)].value
    # ИНВ № ПТР
    invent_num = sheet['I' + str(i)].value
    # Столбец2
    col2 = sheet['J' + str(i)].value
    # Примечания
    comment = sheet['K' + str(i)].value
    # группа
    group = sheet['L' + str(i)].value
    # МОЛ
    mol = sheet['M' + str(i)].value
    # Столбец12
    col12 = sheet['N' + str(i)].value
    # удаленка
    remote = sheet['O' + str(i)].value
    # расположение
    place = sheet['P' + str(i)].value
    # в_ПТР
    ptr = sheet['Q' + str(i)].value
    # Столбец3
    col3 = sheet['R' + str(i)].value

    # !!!
    # Тут можно уже работать с БД

    # Но пока просто выведем всё это в консоль
    # print (type ' -> ' + model + ' -> ' + host_name + ' -> ' + serial_num + ' -> ' + invent_num_old + ' -> ' + invent_num + ' -> ' + fio)
    print (type, model, host_name, serial_num, invent_num_old, invent_num, fio)