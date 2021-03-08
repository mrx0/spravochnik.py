
// Клики в body по кнопкам
$("body").on("click", ".k-button", function(){
    //console.log($(this).attr("id"));

    //Если нажали на кнопку
    //Если кнопка главного меню
    if ($(this).attr("data-status") == 'main_menu_button') {

        //Удаляем у всех кнопок из main_menu_button класс k-state-active, чтобы они не выглядели выделенными
        $('[data-status="main_menu_button"]').removeClass('k-state-active');
        // Добавляем нажатой кнопке из main_menu_button класс k-state-active, чтобы она выглядела выделенной
        $(this).addClass('k-state-active');

        // - items_button
        if ($(this).attr("id") == 'items_button') {
            // Чистим главное окно
            $('#main_window').html('');
            // Чистим менюшку с кнопками по типам
            $("#main_window_header").html('');
            // Показываем менюшку с кнопками по типам
            $("#main_window_header").show();

            // Запросим данные по типам оборудования
            getDataFromDB('items_types');

            // Запросим данные по всему оборудованию
            getItemsFromDB(0)

            // Запросим данные
            //getDataFromDB ($(this).attr("id"));
        }
        // - workers_button
        if ($(this).attr("id") == 'workers_button') {
            // Чистим главное окно
            $('#main_window').html('');
            // Чистим менюшку с кнопками по типам
            $("#main_window_header").html('');
            // Прячем менюшку с кнопками по типам
            $("#main_window_header").hide();

            // Отображение всех сотрудников
            showAllWorkers();

            //Запросим данные
            //getDataFromDB ($(this).attr("id"));

        }
    }

    // Если кнопка типа оборудования
    if ($(this).attr("data-status") == 'item_type_button') {

        // Удаляем у всех кнопок из main_menu_button класс k-state-active, чтобы они не выглядели выделенными
        $('[data-status="item_type_button"]').removeClass('k-state-active k-state-focused');
        // $('[data-status="item_type_button"]').removeClass('k-state-focused');
        // Добавляем нажатой кнопке из main_menu_button класс k-state-active, чтобы она выглядела выделенной
        $(this).addClass('k-state-active k-state-focused');
        // $(this).addClass('k-state-focused');

        // Запросим данные по всему оборудованию
        getItemsFromDB($(this).attr("data-value"));
    }
});

// Функция получения данных по типам оборудования / сотрудникам
function getDataFromDB (flag) {
    // Куда передаём данные по умолчанию и откуда будем ждать ответ (скрипт *.py)
    let link = "py/get_types.py";

    // Если мы хотим получить значения по-другому флагу
    // - данные по сотруднику
    if (flag == 'workers_button'){
        link = "py/get_workers.py";
    }
    if (flag == 'items_types'){
        link = "py/get_types.py";
    }

    // Данные, которые передаём
    let reqData = {
        flag: flag
    };
    // console.log(reqData);

    // Поехали
    $.ajax({
        url: link,
        global: false,
        type: "POST",
        dataType: "JSON",
        data: reqData,
        cache: false,
        beforeSend: function () {
            // Что-то делаем пока ждём ответа
            // $('#errrror').html("<div style='width: 120px; height: 32px; padding: 10px; text-align: center; vertical-align: middle; border: 1px dotted rgb(255, 179, 0); background-color: rgba(255, 236, 24, 0.5);'><img src='img/wait.gif' style='float:left;'><span style='float: right;  font-size: 90%;'> обработка...</span></div>");
        },
        // Действие, при ответе с сервера
        success: function (res) {
            // Выводим в консоль
            // console.log(res);
            // console.log(res.data);

            //Если результат success
            if(res.result == "success") {
                //Если длина ответа больше 0
                if (res.data.length > 0) {
                    // console.log(res.data);
                    // console.log(typeof(res.data));

                    //Выводим данные
                    $('#main_window_header').html('<div id="main_window_header_buttons" data-role="buttongroup" class="k-widget k-button-group" role="group" tabindex="0" aria-disabled="false"></div>');
                    $('#main_window_header_buttons').append('<span title="Все" data-status="item_type_button" data-value="0" role="button" class="k-button k-state-active k-state-focused">Все</span>');

                    res.data.forEach(function(element) {
                        // console.log(element['name']);

                        // Каждый отдельный элемент в отдельную кнопку
                        $('#main_window_header_buttons').append('<span id="item_type_'+element['id']+'" data-status="item_type_button" data-value="'+element['id']+'" role="button" class="k-button" title="'+element['name']+'">'+element['name']+'</span>');
                    });
                }
            }
        }
    });
}

// Функция отображения всех сотрудников (создаёт форму и запрашивает данные для неё у function getStaffTree и getWorkers)
function showAllWorkers(){
    $('#main_window').html('' +
        '<div style="white-space: nowrap;">' +
            '<div style="display: inline-block; border: 1px solid #c5c5c5; position: relative; vertical-align: top;">' +
                '<div style="margin: 5px 0 5px; font-size: 11px; cursor: pointer;">' +
                    '<!--<span class="dotyel a-action lasttreedrophide">скрыть всё</span>, <span class="dotyel a-action lasttreedropshow">раскрыть всё</span>-->' +
                '</div>' +
                '<div id="workers_staff_rezult" style="width: 350px; max-width: 350px; min-width: 350px; height: 750px; overflow-y: scroll; overflow-x: hidden;">' +
                '</div>' +
            '</div>' +
			'<div style="display: inline-block; border: 1px solid #c5c5c5; position: relative; vertical-align: top;">' +
                '<div style="margin: 5px 0 5px; font-size: 11px; cursor: pointer;">' +
                    '<!--<span class="dotyel a-action lasttreedrophide">скрыть всё</span>, <span class="dotyel a-action lasttreedropshow">раскрыть всё</span>-->' +
                '</div>' +
                '<div id="workers_rezult" style="/*width: 700px; max-width: 700px; min-width: 700px;*/ height: 750px; overflow-y: scroll; overflow-x: hidden;">' +
				'</div>' +
            '</div>' +
        '</div>');

    getStaffTree ();
	
	getWorkers (0);

}

//Загрузка дерева
function getStaffTree (){
    //console.log('getStaffTree');

    let link = "py/get_staff_tree.py";

    //!!! Просто что-то передали, потом исправить/убрать
    let reqData = {
        flag: true
    };
    //console.log(reqData);

    $.ajax({
        url: link,
        global: false,
        type: "POST",
        dataType: "JSON",
        data: reqData,
        cache: false,
        beforeSend: function () {
            // Что-то делаем пока ждём ответа
            // $('#errrror').html("<div style='width: 120px; height: 32px; padding: 10px; text-align: center; vertical-align: middle; border: 1px dotted rgb(255, 179, 0); background-color: rgba(255, 236, 24, 0.5);'><img src='img/wait.gif' style='float:left;'><span style='float: right;  font-size: 90%;'> обработка...</span></div>");
        },
        // Действие, при ответе с сервера
        success: function (res) {
            // console.log (res);

            // Вывели дерево/список
            if (res.result == 'success') {
                $("#workers_staff_rezult").html(res.data);
            }
        }
    })
}

//Загрузка оборудования
function getItemsFromDB (type){

    let link = "py/get_items.py";

    let reqData = {
        type: type
    };
    // console.log(reqData);

    $.ajax({
        url: link,
        global: false,
        type: "POST",
        dataType: "JSON",
        data: reqData,
        cache: false,
        beforeSend: function () {
            // Что-то делаем пока ждём ответа
            // $('#errrror').html("<div style='width: 120px; height: 32px; padding: 10px; text-align: center; vertical-align: middle; border: 1px dotted rgb(255, 179, 0); background-color: rgba(255, 236, 24, 0.5);'><img src='img/wait.gif' style='float:left;'><span style='float: right;  font-size: 90%;'> обработка...</span></div>");
        },
        // Действие, при ответе с сервера
        success: function (res) {
            // console.log (res);

            // Вывели список в таблице
            if (res.result == 'success') {
                $('#main_window').html('' +
                    '<table role="grid" id="myTable" class="tablesorter">' +
                    '<colgroup>' +
                        '<col style="width: 50px;  min-width: 50px;">' +
                        '<col style="width: 100px">' +
                        '<col style="width: 100px; min-width: 100px;">' +
                        '<col style="width: 80px">' +
                        '<col style="width: 100px; min-width: 100px;">' +
                        '<col style="width: 200px">' +
                        '<col style="width:186px">' +
                    '</colgroup>' +
                    '<thead role="rowgroup">' +
                        '<tr role="row">' +
                            '<th scope="col" role="columnheader" data-field="COUNT_VR" aria-haspopup="true" rowspan="1" data-title="" data-groupable="false" data-index="1" id="b29dedd7-57f8-465a-8ed7-263c454c422d" title="" class="k-header" data-role="columnsorter">' +
                                '<span class="k-link" href="">Тип</span>' +
                            '</th>' +
                            '<th scope="col" role="columnheader" data-field="DOCS" aria-haspopup="true" rowspan="1" data-title="" data-groupable="false" data-index="2" id="d18deb96-8f96-4ae2-8b0b-47db353fbc7e" title="" class="k-header" data-role="columnsorter">' +
                                '<span class="k-link" href="">Модель</span>' +
                            '</th>' +
                            '<th scope="col" role="columnheader" data-field="NOMER_DEMAND" aria-haspopup="true" rowspan="1" data-title="" data-groupable="false" data-index="0" id="657d0dca-7461-490a-ad56-2fa0ff5aec83" title="" class="k-header" data-role="columnsorter">' +
                                '<span class="k-link" href="">Инвент. №</span>' +
                            '</th>' +
                            '<th scope="col" role="columnheader" data-field="DATE_BEGIN" aria-haspopup="true" rowspan="1" data-title="" aria-label="" data-aggregates="count" data-index="3" id="b5e42713-5842-46c7-8611-68e18393ed37" title="Дата выдачи" class="k-header" data-role="columnsorter">' +
                                '<span class="k-link" href="">Серийн. №</span>' +
                            '</th>' +
                            '<th scope="col" role="columnheader" data-field="CL_PHONE" aria-haspopup="true" rowspan="1" data-title="Host / Т.номер" aria-label="" data-aggregates="count" data-index="6" id="786d2679-6aad-4b0d-a59c-5030f828ef8e" title="Телефон" class="k-header" data-role="columnsorter">' +
                                '<span class="k-link" href="">Host / Т.номер</span>' +
                            '</th>' +
                            '<th scope="col" role="columnheader" data-field="NAME_CLIENT" aria-haspopup="true" rowspan="1" data-title="Числится" aria-label="" data-aggregates="count" data-index="7" id="451c820c-081d-430a-9997-c4f55f9fdcd2" title="Клиент" class="k-header" data-role="columnsorter">' +
                                '<span class="k-link" href="">Числится</span>' +
                            '</th>' +
                            '<th scope="col" role="columnheader" data-field="NOTE" aria-haspopup="true" rowspan="1" data-title="Описание" data-groupable="false" data-index="11" id="2fc10ed1-4709-41a5-b46d-31221285d389" title="Описание" class="k-header <!--k-with-icon k-filterable-->" data-role="columnsorter">' +
                                '<span class="k-link" href="">Примечания</span>' +
                            '</th>' +
                        '</tr>' +
                    '</thead>' +
                    '<tbody id="itemTableData" role="rowgroup">' +

                    '</tbody>' +
                '</table>' +
                '');

                $("#itemTableData").html(res.data);

                //Запускаем функцию для сортировки
                $(function() {
                    $("#myTable").tablesorter();
                });
            }
        }
    })
}

//Загрузка сотрудников
function getWorkers(staff){
	let link = "py/get_workers.py";

    let reqData = {
        staff: staff
    };
    // console.log(reqData);

    $.ajax({
        url: link,
        global: false,
        type: "POST",
        dataType: "JSON",
        data: reqData,
        cache: false,
        beforeSend: function () {
            // Что-то делаем пока ждём ответа
            // $('#errrror').html("<div style='width: 120px; height: 32px; padding: 10px; text-align: center; vertical-align: middle; border: 1px dotted rgb(255, 179, 0); background-color: rgba(255, 236, 24, 0.5);'><img src='img/wait.gif' style='float:left;'><span style='float: right;  font-size: 90%;'> обработка...</span></div>");
        },
        // Действие, при ответе с сервера
        success: function (res) {
            // console.log (res);

            // Вывели список
            if (res.result == 'success') {
                $("#workers_rezult").html(res.data);
            }
        }
    })
}

// Показываем блок для подтверждения переноса
// !!!2021-02-08 Сейчас никакого блока нет, функцуия сквозная, просто передаёт данные дальше
// но м.б. в будущем мы сделаем тут диалог подтверждения
function showMoveApprove(item, target){
    // console.log(item);
    // console.log(target);
    // console.log(item.elem.getAttribute("data-uid")+" in "+target.id);
    // console.log(item.elem.id.split('_')[0]);

    let itemDataUID = item.elem.getAttribute("data-uid");
    let targetDataUID = target.getAttribute("data-uid");
    // console.log(itemDataUID.split('_')[1]);
    // console.log(targetDataUID.split('_')[1]);

    //Спрячем элемент, который переносили, чтобы не перезагружать страницу
    item.elem.style.display = 'none';

    //Перемещение департамента в другой
    if (itemDataUID.split('_')[0] == 'staffId') {
        moveWorkerOrStaffInStaff(0, itemDataUID.split('_')[1], targetDataUID.split('_')[1]);
    }
    //Перемещение сотрудника в другой департамент
    if (itemDataUID.split('_')[0] == 'workerId') {
        moveWorkerOrStaffInStaff(itemDataUID.split('_')[1], 0, targetDataUID.split('_')[1]);
    }
}

//Перемещаем позицию в другое место
function moveWorkerOrStaffInStaff (worker_id, staff_id, target_staff_id){

    let link = "py/move_item_in_staff.py";

    let reqData = {
        worker_id: worker_id,
        staff_id: staff_id,
        target_staff_id: target_staff_id
    };
    //console.log(reqData);

    $.ajax({
        url: link,
        global: false,
        type: "POST",
        dataType: "JSON",
        data: reqData,
        cache: false,
        beforeSend: function () {
            // Что-то делаем пока ждём ответа
            // $('#errrror').html("<div style='width: 120px; height: 32px; padding: 10px; text-align: center; vertical-align: middle; border: 1px dotted rgb(255, 179, 0); background-color: rgba(255, 236, 24, 0.5);'><img src='img/wait.gif' style='float:left;'><span style='float: right;  font-size: 90%;'> обработка...</span></div>");
        },
        success: function (res) {
            console.log (res);

            if (res.result == 'success') {
                getStaffTree ();
            }
        }
    })

}

//Для теста контекстного меню
let menu = document.querySelector('.context-menu-container');

function showMenu(x, y){
    menu.style.left = x + 'px';
    menu.style.top = y + 'px';
    //menu.classList.add('show-menu');

    menu.style.display = 'block';
}

function hideMenu(){
    //menu.classList.remove('show-menu');

    menu.style.display = 'none';
}

function onContextMenu(e){
    e.preventDefault();
    showMenu(e.pageX, e.pageY);
    document.addEventListener('mousedown', onMouseDown, false);
}

function onMouseDown(e){
    hideMenu();
    document.removeEventListener('mousedown', onMouseDown);
}

// document.addEventListener('contextmenu', onContextMenu, false);
//
//
// let items = document.querySelector(".k-menu-link");
// console.log(items);

document.addEventListener("contextmenu", event => {
    // console.log(event.target.closest('td'));
    // console.log(event.target.closest('tr'));
    // console.log(event.target.closest('tr').className);

    if (event.target.closest('tr') !== null) {
        if (event.target.closest('tr').className !== undefined) {
            if (event.target.closest('tr').className == 'item_data') {
                onContextMenu(event);
            }
        }
    }

    //event.preventDefault();

//                        //Сначала очищаем у всех окраску
//                        $(".droppable, .draggable").removeClass("context_pick");
//                        //Теперь покрасим
//                        if (event.target.classList.contains("droppable")){
//                            $(event.target).addClass("context_pick");
//                        }

    //contextMenuShow(0, 0, event, "sclad_cat");
    //onContextMenu

}, false);
