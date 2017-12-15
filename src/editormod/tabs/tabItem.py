from general.tabTemplates import StandartTab
from ..tops.topItem import ItemAddition, ItemEditing


class ItemTab(StandartTab):
    def __init__(self, basis):
        super().__init__(basis)
        self.tv['columns'] = [
            'name',
            'substance',
            'markup',
            'manufacturers',
            'nomenclature',
            'prescription']
        self.tv.heading('#0', text='Код')
        self.tv.heading('name', text='Наименование')
        self.tv.heading('substance', text='Действующее вещество')
        self.tv.heading('markup', text='% макс. наценки')
        self.tv.heading('manufacturers', text='Изготовители')
        self.tv.heading('nomenclature', text='Номенклатура')
        self.tv.heading('prescription', text='Рецептурный')
        self.tv.column('#0', minwidth=25, stretch=True, width=50)
        self.tv.column('name', minwidth=125, stretch=True, width=250)
        self.tv.column('substance', minwidth=105, stretch=True, width=210)
        self.tv.column('markup', anchor='e', minwidth=60, stretch=True, width=120)
        self.tv.column('manufacturers', anchor='e', minwidth=50, stretch=True, width=100)
        self.tv.column('nomenclature', minwidth=60, stretch=True, width=120)
        self.tv.column('prescription', anchor='c', minwidth=50, stretch=True, width=100)
        self.addition = ItemAddition(self)
        self.editing = ItemEditing(self)
        self.tv.bind('<Double-Button-1>', lambda _: self.editing.fillAndShow())
        self.btnAdd['command'] = lambda: self.addition.fillAndShow()
        self.btnChn['command'] = lambda: self.editing.fillAndShow()

    def reset(self):
        self.db.openData()
        self.update()
        self.basis.prcTab.update()
        self.basis.mnfTab.update()

    def update(self, requestList=None):
        for rec in self.tv.get_children():
            self.tv.delete(rec)
        self.db.data['item_list'].sort(key=lambda e: e['name'].lower())
        for rec in self.db.data['item_list']:
            strCode = str(rec['code'])
            strMarkup = str(rec['markup'])
            strLenMnfs = str(len(rec['manufacturers']))
            intNomenclature = rec['nomenclature']
            if intNomenclature == 1:
                strNomenclature = 'Мед. средство'
            elif intNomenclature == 2:
                strNomenclature = 'Сопутствующее'
            else:
                strNomenclature = 'Неизвестно'
            strPrescription = 'Да' if rec['prescription'] else 'Нет'
            value = rec['name'], rec['substance'], strMarkup, strLenMnfs, strNomenclature, strPrescription
            self.updateView(requestList, **{
                'iid': strCode,
                'text': strCode,
                'value': (value)})

    def delete(self):
        if self.tv.selection():
            slcTag = self.tv.selection()[0]
            self.db.deleteRecord('item_list', int(slcTag))
            self.tv.delete(slcTag)
            index = 0
            while index < len(self.db.data['price_list']):
                if self.db.data['price_list'][index]['code'][0] == int(slcTag):
                    self.db.data['price_list'].remove(self.db.data['price_list'][index])
                else:
                    index += 1
            self.basis.prcTab.tv.delete(slcTag)
