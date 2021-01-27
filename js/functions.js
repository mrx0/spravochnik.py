
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

            //Запросим данные по типам оборудования
            getDataFromDB('items_types');

            //Запросим данные
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
});

//Функция получения данных ... !!! дописать каких
function getDataFromDB (flag) {
    // Куда передаём данные по умолчанию и откуда будем ждать ответ (скрипт *.py)
    let link = "py/get_types.py";

    //Если мы хотим получить значения по-другому флагу
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
            //console.log(res);
            // console.log(res.data);

            //Если результат success
            if(res.result == "success") {
                //Если длина ответа больше 0
                if (res.data.length > 0) {
                    // console.log(res.data);
                    // console.log(typeof(res.data));

                    //Выводим данные
                    $('#main_window_header').html('<div id="main_window_header_buttons" data-role="buttongroup" class="k-widget k-button-group" role="group" tabindex="0" aria-disabled="false"></div>');
                    $('#main_window_header_buttons').append('<span title="Все" data-value="0" role="button" class="k-button k-state-active k-state-focused">Все</span>');

                    res.data.forEach(function(element) {
                        //console.log(element['name']);

                        //Каждый отдельный элемент в отдельную кнопку
                        $('#main_window_header_buttons').append('<span id="item_type_'+element['id']+'" data-status="item_type_button" data-value="'+element['id']+'" role="button" class="k-button" title="'+element['name']+'">'+element['name']+'</span>');
                    });
                }
            }
        }
    });
}

// Функция отображения всех сотрудников (создаёт форму и запрашивает данные для неё у function getScladCategories)
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
        '</div>');

    getAllWorkers ();

}

//Загрузка категорий склада
function getAllWorkers (){

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


