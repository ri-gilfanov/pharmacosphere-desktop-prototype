from general.tabTemplates import StandartTab
from ..tops.topPrice import PriceAddition, PriceEditing


class PriceTab(StandartTab):
    def __init__(self, basis):
        super().__init__(basis)
        self.tv['columns'] = ['manufacturer', 'provider', 'price', 'date']
        self.tv.heading('#0', text='Наименование/Код')
        self.tv.heading('manufacturer', text='Изготовитель')
        self.tv.heading('provider', text='Поставщик')
        self.tv.heading('price', text='Цена')
        self.tv.heading('date', text='Срок годности')
        self.tv.column('#0', minwidth=125, stretch=True, width=250)
        self.tv.column('manufacturer', minwidth=100, stretch=True, width=250)
        self.tv.column('provider', minwidth=100, stretch=True, width=250)
        self.tv.column('price', anchor='e', minwidth=50, stretch=True, width=100)
        self.tv.column('date', anchor='c', minwidth=50, stretch=True, width=150)
        self.addition = PriceAddition(self)
        self.editing = PriceEditing(self)
        self.tv.bind('<Double-Button-1>', lambda _: self.editing.fillAndShow())
        self.btnAdd['command'] = lambda: self.addition.fillAndShow()
        self.btnChn['command'] = lambda: self.editing.fillAndShow()

    def reset(self):
        self.db.openData()
        self.update()
        self.basis.itmTab.update()
        self.basis.prvTab.update()
        self.basis.mnfTab.update()

    def update(self, requestList=None):
        for rec in self.tv.get_children():
            self.tv.delete(rec)
        self.db.data['item_list'].sort(key=lambda e: e['name'].lower())
        for rec in self.db.data['item_list']:
            strCode = str(rec['code'])
            self.updateView(requestList, **{
                'iid': strCode,
                'text': rec['name'],
                'value': ()})
        
        tagParents = self.tv.get_children()
        for rec in self.db.data['price_list']:
            strItmCode = str(rec['code'][0])
            if strItmCode in tagParents:
                mnfCode = rec['code'][1]
                prvCode = rec['code'][2]
                code = '%s%s%s%s%s' % (
                    strItmCode, '.', str(mnfCode), '.', str(prvCode))
                prvName = self.db.getName('provider_list', prvCode)
                mnfName = self.db.getName('manufacturer_list', mnfCode)
                strPrice = '{:.2f}'.format(rec['price'])
                value = (mnfName, prvName, strPrice, rec['date'])
                self.tv.insert(
                    parent=strItmCode,
                    index='end',
                    iid=code,
                    text=code,
                    value=value)

    def delete(self):
        slcTags = self.tv.selection()
        if (slcTags and slcTags[0] and len(self.tv.parent(slcTags[0]))):
            slcTag = self.tv.selection()[0]
            self.db.deleteRecord('price_list', [int(x) for x in slcTag.split('.')])
            self.tv.delete(slcTag)
