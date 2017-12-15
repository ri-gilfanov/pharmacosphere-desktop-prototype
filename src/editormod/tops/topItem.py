from general.rig_tk import Combobox, Entry
from tkinter import END, messagebox
from tkinter.ttk import Label
from general.widgets import MnfSelector
from general.topTemplates import Editor, Addition, Editing


class ItemEditor(Editor):
    def __init__(self, tab):
        super().__init__(tab)
        self.frmFields.grid_columnconfigure(1, weight=1)
        [Label(self.frmFields, text=s).grid(row=i, **self.grd.cl0_pdSt)
            for i, s in enumerate([
                'Название',
                'Действующее вещество',
                '% макс. наценки',
                'Номенклатура',
                'Рецептурный'])]
        self.entName = Entry(self.frmFields)
        self.entSubstance = Entry(self.frmFields)
        self.entMarkup = Entry(self.frmFields, width=7, **self.vld.vldInt)
        self.cbNomenclature = Combobox(
            master=self.frmFields,
            width=12,
            state='readonly',
            values=['Неизвестно', 'Мед. средство', 'Сопутствующее'])
        self.cbPrescription = Combobox(
            master=self.frmFields,
            width=12,
            state='readonly',
            values=['Да', 'Нет'])
        self.entName.grid(row=0, sticky='w, e', **self.grd.cl1_pdSt)
        self.entSubstance.grid(row=1, sticky='w, e', **self.grd.cl1_pdSt)
        self.entMarkup.grid(row=2, sticky='w', **self.grd.cl1_pdSt)
        self.cbNomenclature.grid(row=3, sticky='w', **self.grd.cl1_pdSt)
        self.cbPrescription.grid(row=4, sticky='w', **self.grd.cl1_pdSt)
        self.selector = MnfSelector(self)

    def clear(self):
        [ent.delete(0, END) for ent in (
            self.entName,
            self.entSubstance,
            self.entMarkup)]


class ItemAddition(ItemEditor, Addition):
    def __init__(self, tab):
        super().__init__(tab)

    def fillAndShow(self):
        self.selector.add()
        self.show()

    def apply(self):
        name = self.trn.getNameSting(self.entName.get())
        if name != '' and self.db.checkName('item_list', name):
            code = self.db.getNewCode('item_list')
            substance = self.entSubstance.get()
            murkup = self.entMarkup.get()
            if murkup.isdigit() is False:
                murkup = '0'
            manufacturers = self.selector.get()
            nomenclature = self.cbNomenclature.get()
            if nomenclature == 'Мед. средство':
                nomenclature = 1
            elif nomenclature == 'Сопутствующее':
                nomenclature = 2
            else:
                nomenclature = 0
            prescription = self.trn.getBoolean(self.cbPrescription.get())
            self.db.data['item_list'] += [{
                'code': code,
                'name': name,
                'substance': substance,
                'markup': int(murkup),
                'manufacturers': manufacturers,
                'nomenclature': nomenclature,
                'prescription': prescription}]
            self.tab.update()
            self.basis.prcTab.update()
            tag = str(code)
            self.endAddition(tag)
        elif name == '':
            messagebox.showerror(
                'Ошибка',
                'Название не может быть пустой строкой.',
                parent=self.toplevel)
        else:
            messagebox.showerror(
                'Ошибка',
                'Наименование с таким названием уже добавлено.',
                parent=self.toplevel)


class ItemEditing(ItemEditor, Editing):
    def __init__(self, tab):
        super().__init__(tab)

    def fillAndShow(self):
        if self.tv.selection():
            self.clear()
            slcTag = self.tv.selection()[0]
            values = self.tv.item(slcTag)['values']
            print(values)
            self.entName.insert(0, values[0])
            self.entSubstance.insert(0, values[1])
            self.entMarkup.insert(0, values[2])
            self.cbNomenclature.set(values[4])
            self.cbPrescription.set(values[5])
            self.selector.edit()
            self.show()

    def apply(self):
        name = self.trn.getNameSting(self.entName.get())
        slcTag = self.tv.selection()[0]
        flagName = self.db.checkName('item_list', name)
        flagCode = self.db.getCode('item_list', name)
        if name != '' and flagName or flagCode == int(slcTag):
            self.tv.set(slcTag, 0, name)
            self.tv.set(slcTag, 1, self.entSubstance.get())
            self.tv.set(slcTag, 2, self.entMarkup.get())
            self.tv.set(slcTag, 3, str(len(self.selector.get())))
            self.tv.set(slcTag, 4, self.cbNomenclature.get())
            self.tv.set(slcTag, 5, self.cbPrescription.get())
            for rec in self.db.data['item_list']:
                if rec['code'] == int(slcTag):
                    rec['name'] = name
                    rec['substance'] = self.entSubstance.get()
                    rec['markup'] = int(self.entMarkup.get())
                    rec['manufacturers'] = self.selector.get()
                    nomenclature = self.cbNomenclature.get()
                    if nomenclature == 'Мед. средство':
                        rec['nomenclature'] = 1
                    elif nomenclature == 'Сопутствующее':
                        rec['nomenclature'] = 2
                    else:
                        rec['nomenclature'] = 0
                    prescription = self.trn.getBoolean(self.cbPrescription.get())
                    rec['prescription'] = prescription
                    break
            self.hide()
        elif name == '':
            messagebox.showerror(
                'Ошибка',
                'Название не может быть пустой строкой.',
                parent=self.toplevel)
        else:
            messagebox.showerror(
                'Ошибка',
                'Наименование с таким названием уже добавлено.',
                parent=self.toplevel)
