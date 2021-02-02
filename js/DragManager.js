var dragManager = new function() {

    /**
     * составной объект для хранения информации о переносе:
     * {
   *   elem - элемент, на котором была зажата мышь
   *   avatar - аватар
   *   downX/downY - координаты, на которых был mousedown
   *   shiftX/shiftY - относительный сдвиг курсора от угла элемента
   * }
     */
   var dragObject = {};

   var self = this;

   function createAvatar(e) {

        // запомнить старые свойства, чтобы вернуться к ним при отмене переноса
        var avatar = dragObject.elem;
        var old = {
            parent: avatar.parentNode,
            nextSibling: avatar.nextSibling,
            position: avatar.position || '',
            left: avatar.left || '',
            top: avatar.top || '',
            zIndex: avatar.zIndex || ''
        };

        // функция для отмены переноса
        avatar.rollback = function() {
            old.parent.insertBefore(avatar, old.nextSibling);
            avatar.style.position = old.position;
            avatar.style.left = old.left;
            avatar.style.top = old.top;
            avatar.style.zIndex = old.zIndex

            //Удалим стиль подсветки у переносимого элемента
            avatar.classList.remove("dnd_class");
        };

        return avatar;
   }

    function startDrag(e) {
        var avatar = dragObject.avatar;

        // инициировать начало переноса
        document.body.appendChild(avatar);
        avatar.style.zIndex = 9999;
        avatar.style.position = 'absolute';

        //Добавим стиль подсветки к переносимому элементу
        avatar.classList.add("dnd_class");
    }

    function findDroppable(event) {
        // спрячем переносимый элемент
        dragObject.avatar.hidden = true;

        // получить самый вложенный элемент под курсором мыши
        var elem = document.elementFromPoint(event.clientX, event.clientY);

        // показать переносимый элемент обратно
        dragObject.avatar.hidden = false;

        if (elem == null) {
            // такое возможно, если курсор мыши "вылетел" за границу окна
            return null;
        }
        //console.log(elem.closest('.droppable'));

        return elem.closest('.droppable');
    }

    function onMouseDown(e) {

        if (e.which != 1) return;

        var elem = e.target.closest('.draggable');
        if (!elem) return;

        dragObject.elem = elem;

        // запомним, что элемент нажат на текущих координатах pageX/pageY
        dragObject.downX = e.pageX;
        dragObject.downY = e.pageY;

        return false;
    }

    function onMouseMove(e) {
        if (!dragObject.elem) return; // элемент не зажат

        if (!dragObject.avatar) { // если перенос не начат...
            var moveX = e.pageX - dragObject.downX;
            var moveY = e.pageY - dragObject.downY;

            // если мышь передвинулась в нажатом состоянии недостаточно далеко
            if (Math.abs(moveX) < 3 && Math.abs(moveY) < 3) {
                return;
            }

            // начинаем перенос
            dragObject.avatar = createAvatar(e); // создать аватар
            if (!dragObject.avatar) { // отмена переноса, нельзя "захватить" за эту часть элемента
                dragObject = {};
                return;
            }

            // аватар создан успешно
            // создать вспомогательные свойства shiftX/shiftY
            var coords = getCoords(dragObject.avatar);
            dragObject.shiftX = dragObject.downX - coords.left;
            dragObject.shiftY = dragObject.downY - coords.top;

            startDrag(e); // отобразить начало переноса
        }

        // отобразить перенос объекта при каждом движении мыши
        dragObject.avatar.style.left = e.pageX - dragObject.shiftX + 'px';
        dragObject.avatar.style.top = e.pageY - dragObject.shiftY + 'px';



        //Находим элемент под перетаскиваемым
        var dropElem = findDroppable(e);
        //console.log(dropElem);

        if (dropElem) {
            //console.log("dropElem");

            self.onDragEnter(dropElem);
        } else {
            //console.log("!dropElem");

            self.onDragLeave();
        }

        return false;
    }

    function finishDrag(e) {
        var dropElem = findDroppable(e);

        if (!dropElem) {
            self.onDragCancel(dragObject);
        } else {
            self.onDragEnd(dragObject, dropElem);
        }
    }

    function onMouseUp(e) {
        if (dragObject.avatar) { // если перенос идет
            finishDrag(e);
        }

        // перенос либо не начинался, либо завершился
        // в любом случае очистим "состояние переноса" dragObject
        dragObject = {};
    }

    document.onmousemove = onMouseMove;
    document.onmouseup = onMouseUp;
    document.onmousedown = onMouseDown;

    self.onDragEnter = function(dropElem) {};
    self.onDragLeave = function(dropElem) {};
    self.onDragEnd = function(dragObject, dropElem) {};
    self.onDragCancel = function(dragObject) {};
};

//Переносимый элемент над целью
dragManager.onDragEnter = function(dropElem) {
    //console.log("onEnter");

    dropElem.classList.add('uponMe');
};

//Переносимый элемент не над целью
dragManager.onDragLeave = function(dropElem) {
    //console.log("onLeave");

    //dropElem.classList.remove('uponMe');

    //!!!Тупое решение, удаляем класс наведения (выделения) у всех, а не у конкретного элемента, с которого ушли
    document.querySelectorAll('.droppable').forEach(function(el, i){
        el.classList.remove('uponMe');
    });
};

//Перемещение удачно закончилось
dragManager.onDragEnd = function(dragObject, dropElem) {
    showMoveApprove (dragObject, dropElem);
};

//Перемещение отменилось
dragManager.onDragCancel = function(dragObject) {
    dragObject.avatar.rollback();
};

function getCoords(elem) { // кроме IE8-
    var box = elem.getBoundingClientRect();

    return {
        top: box.top + pageYOffset,
        left: box.left + pageXOffset
    };

}