from general.tabTemplates import StandartTab
from ..tops.topManufacturer import ManufacturerAddition, ManufacturerEditing


class ManufacturerTab(StandartTab):
    def __init__(self, basis):
        super().__init__(basis)
        self.tv['columns'] = ['name']
        self.tv.heading('#0', text='Код')
        self.tv.heading('name', text='Название')
        self.tv.column('#0', anchor='e', minwidth=40, stretch=True, width=80)
        self.tv.column('name', minwidth=460, stretch=True, width=920)
        self.addition = ManufacturerAddition(self)
        self.eddition = ManufacturerEditing(self)
        self.tv.bind('<Double-Button-1>', lambda _: self.eddition.fillAndShow())
        self.btnAdd['command'] = lambda: self.addition.show()
        self.btnChn['command'] = lambda: self.eddition.fillAndShow()

    def reset(self):
        self.db.openData()
        self.update()
        self.basis.prcTab.update()
        self.basis.itmTab.update()

    def update(self, requestList=None):
        for rec in self.tv.get_children():
            self.tv.delete(rec)
        self.db.data['manufacturer_list'].sort(key=lambda e: e['name'].lower())
        for rec in self.db.data['manufacturer_list']:
            strCode = str(rec['code'])
            self.updateView(requestList, **{
                'iid': strCode,
                'text': strCode,
                'value': (rec['name'], )})

    def delete(self):
        if self.tv.selection():
            slcTag = self.tv.selection()[0]
            self.db.deleteRecord('manufacturer_list', int(slcTag))
            self.tv.delete(slcTag)
            for rec in self.db.data['item_list']:
                if int(slcTag) in rec['manufacturers']:
                    rec['manufacturers'].remove(int(slcTag))
                    strLenMnfs = str(len(rec['manufacturers']))
                    self.basis.itmTab.tv.set(str(rec['code']), 3, strLenMnfs)
            index = 0
            while index < len(self.db.data['price_list']):
                if self.db.data['price_list'][index]['code'][1] == int(slcTag):
                    self.db.data['price_list'].remove(self.db.data['price_list'][index])
                else:
                    index += 1
            for tagParent in self.basis.prcTab.tv.get_children():
                for tagChildren in self.basis.prcTab.tv.get_children(tagParent):
                    if tagChildren.split('.')[1] == slcTag:
                        self.basis.prcTab.tv.delete(tagChildren)
