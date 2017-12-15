from general.tabTemplates import StandartTab
from ..tops.topProvider import ProviderAddition, ProviderEditing


class ProviderTab(StandartTab):
    def __init__(self, basis):
        super().__init__(basis)
        self.tv['columns'] = ['name', 'date', 'phone', 'fax', 'email']
        self.tv.heading('#0', text='Код')
        self.tv.heading('name', text='Название')
        self.tv.heading('date', text='Дата прайса')
        self.tv.heading('phone', text='Телефон')
        self.tv.heading('fax', text='Факс')
        self.tv.heading('email', text='Электронная почта')
        self.tv.column('#0', anchor='e', minwidth=40, stretch=True, width=80)
        self.tv.column('name', minwidth=127, stretch=True, width=254)
        self.tv.column('date', anchor='c', minwidth=77, stretch=True, width=154)
        self.tv.column('phone', minwidth=102, stretch=True, width=204)
        self.tv.column('fax', minwidth=77, stretch=True, width=154)
        self.tv.column('email', anchor='e', minwidth=77, stretch=True, width=154)
        self.addition = ProviderAddition(self)
        self.eddition = ProviderEditing(self)
        self.tv.bind('<Double-Button-1>', lambda _: self.eddition.fillAndShow())
        self.btnAdd['command'] = lambda: self.addition.show()
        self.btnChn['command'] = lambda: self.eddition.fillAndShow()

    def reset(self):
        self.db.openData()
        self.update()
        self.basis.prcTab.update()

    def update(self, requestList=None):
        for rec in self.tv.get_children():
            self.tv.delete(rec)
        self.db.data['provider_list'].sort(key=lambda e: e['name'].lower())
        for rec in self.db.data['provider_list']:
            strCode = str(rec['code'])
            self.updateView(requestList, **{
                'iid': strCode,
                'text': strCode,
                'value': (
                    rec['name'],
                    rec['date'],
                    rec['phone'],
                    rec['fax'],
                    rec['email'])})

    def delete(self):
        if self.tv.selection():
            slcTag = self.tv.selection()[0]
            self.db.deleteRecord('provider_list', int(slcTag))
            self.tv.delete(slcTag)
            index = 0
            while index < len(self.db.data['price_list']):
                if self.db.data['price_list'][index]['code'][2] == int(slcTag):
                    self.db.data['price_list'].remove(self.db.data['price_list'][index])
                else:
                    index += 1
            for tagParent in self.basis.prcTab.tv.get_children():
                for tagChildren in self.basis.prcTab.tv.get_children(tagParent):
                    if tagChildren.split('.')[2] == slcTag:
                        self.basis.prcTab.tv.delete(tagChildren)
