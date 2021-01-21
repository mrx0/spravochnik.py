//***Для дерева
//Для обслуживания дерева
var objButton;																	//объект Кнопка
var objTree;																	//объект Дерево
var objModel;																	//объект для хранения значения
var nIdModelDef;																//ключ значения По-умолчанию
var nLink;																		//ключ настройки
//$(window).load(function () {
//Параметры в зависимости от нажатой кнопки
function TreeParams() {
    switch (objModel[0].id) {
        case "ID_PLACE":
            return { link: nLink, resKod: "'RES_800'", cursor: 116, empty: 0, node: 1 }
        case "ID_TECH_PLACE":
            return { link: nLink, resKod: "'RES_810'", cursor: 116, empty: 0, node: 1 }
        case "ID_PROBLEM":
            return { link: nLink, resKod: "'RES_490'", cursor: 116, empty: 0, node: 1 }
    }
};
//Событие "открытие" диалога
function dialogOpen(e) {
    var treeview = objTree.data("kendoTreeView");
    treeview.dataSource.read();
    var listNodes = JSON.parse("[" + jqService("/api/ResListNodes", { id: objModel.val(), id_node: nIdModelDef }) + "]");
    treeview.expandPath(listNodes);
    var barDataItem = treeview.dataSource.get(objModel.val());
    if (barDataItem) treeview.select(treeview.findByUid(barDataItem.uid));
}
///Событие "открытие" диалога
function openDialog(e) {
    objButton = e.event.target.id;
    var dialogTree = $("#dialog").data("kendoDialog");
    var titleText = e.event.target.getAttribute('value-title');
    dialogTree.title(titleText == null ? 'Справочник' : titleText);
    dialogTree.open();
}
//Событие "нажатие кн.ОК"
function actionOK(e, callBack) {
    var ItemId;
    var ItemName;
    var treeview = objTree.data("kendoTreeView");
    var item = treeview.dataItem(treeview.select());
    if (item) {
        var ItemId = item.id;
        var ItemName = item.NAME;
    }
    var bUpdate = (ItemId != objModel.val());
    objModel.val(ItemId);
    $("#" + objButton).text(ItemName);
    if (bUpdate && callBack) callBack(objButton, ItemId);
};
//});