# def plus(a, b):
#   # Something
#   return a+b
#
# def minus(a, b):
#   # Something
#   return a-b


#!!! не доделано. Доделать/убрать Соединение с БД
# def dbConnect():
#   return


# Дерево отделов и департаментов (рекурсия)
def showTreeStaff (level, space, type, sel_id, first, last_level, deleted, dtype, conn):
    # print (level)

    staff_rez = {}

    rez_str = ''

    # определяем уровень для запроса
    # if level == 0:
    #     parent_str = "`parent_id` = '0'"
    # else:
    #     parent_str = "`parent_id` = ?"

    # берем верхний уровень
    query = """SELECT * FROM `spr_staff` WHERE `parent_id` = ? ORDER BY `name`"""
    # print(query);

    # dictionary=True - чтобы работать с результатом как с объектом (ассоциативным массивом)
    cur = conn.cursor(dictionary=True)

    # Запрос данных
    cur.execute(query, [level])

    staff_rez = cur.fetchall()

    # Количество вернувшихся элементов
    # print(cur.rowcount)

    # Если не пустой результат вернулся
    # if cur.rowcount != 0:
    #     print(staff_rez);

      # Собираем то, что получили, в одну строку для возврата обратно ???
      # for data in sclad_rez:
      #   res += '' + data['name'] + ''

    # Если первый проход
    if first:
        # print('first');

        if type == 'list':
            rez_str += '''
                    <ol class="tree">
                    <li>
                        <label id="cat_0" class="droppable hover" onclick="getWorkers (0); return;" cat_name="">Вне списка</label> <input type="checkbox" id="folder0" checked />
                    </li>'''

    else:
        if type == 'list':
            rez_str += '''<ol class="tree2">'''

    # Если не пустой результат вернулся
    if cur.rowcount != 0:
        # foreach ($sclad_rez as $sclad_rez_value){
        for data in staff_rez:
            # staffs[data['name'].lower()] = data

            if type == 'list':
                # print('мы тут 1')
                # print(data)

                # Если в этом элементе должны быть "вложены" еще другие
                if data['node_count'] > 0:
                    rez_str += '''
                        <li>
                            <label id="cat_''' + str(str(data['id'])) + '''" class="draggable droppable hover" onclick="getWorkers (''' + str(data['id']) + '''); return;" cat_name="''' + data['name'] + '''"> ''' + data['name'] + '''</label> <input type="checkbox" id="folder''' + str(data['id']) + '''" checked />
                        '''
                    rez_str += showTreeStaff(data['id'], '', 'list', 0, False, 0, False, 0, conn)

                    rez_str += '</li>'

                else:
                    rez_str += '''
                        <li>
                            <label id="cat_''' + str(data['id']) + '''" class="draggable droppable hover" onclick="getWorkers (''' + str(data['id']) + '''); return;" cat_name="''' + data['name'] + '''"> ''' + data['name'] + '''</label> <input type="checkbox" id="folder''' + str(data['id']) + '''" checked />
                        </li>'''

    #         if ($type == 'select'){
    #             # echo $space.$value['name'].'<br>';
    #
    #             $selected = '';
    #             if ($sclad_rez_value['id'] == $sel_id){
    #                 $selected = ' selected';
    #             }
    #             $rez_str .= '<option value="'.$sclad_rez_value['id'].'" '.$selected.'>'.$space.$sclad_rez_value['name'].'</option>';
    #
    #             $space2 = $space. '...';
    #             # $last_level2 = $last_level+1;
    #
    #             rez_str += showTreeStaff ($sclad_rez_value['id'], space2, 'select', sel_id, False, 0, False, 0, conn)
    #             # $rez_str .= showTreeSclad2($sclad_rez_value['id'], $space2, 'select', $sel_id, FALSE, 0, FALSE, $dbtable, 0, 0, $msql_cnnct);
    #         }
    #     }

        if type == 'list':
            rez_str += '</ol>'

    if first:
        if type == 'list':
            rez_str += '</ol>'

    return rez_str
