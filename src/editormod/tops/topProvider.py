from general.rig_tk import Entry
from tkinter import END, messagebox
from tkinter.ttk import Label
from general.topTemplates import Editor, Addition, Editing


class ProviderEditor(Editor):
    def __init__(self, tab):
        super().__init__(tab)
        [Label(self.frmFields, text=s).grid(row=i, **self.grd.cl0_pdSt)
            for i, s in enumerate([
                'Название',
                'Дата прайса',
                'Телефон',
                'Факс',
                'Электронная почта'])]
        self.entName = Entry(self.frmFields)
        self.entDate = Entry(self.frmFields, **self.vld.vldDate)
        self.entPhone = Entry(self.frmFields)
        self.entFax = Entry(self.frmFields)
        self.entEmail = Entry(self.frmFields)
        [w.grid(row=i, **self.grd.cl1_pdSt) for i, w in enumerate((
            self.entName,
            self.entDate,
            self.entPhone,
            self.entFax,
            self.entEmail))]

    def clear(self):
        [w.delete(0, END) for w in (
            self.entName,
            self.entDate,
            self.entPhone,
            self.entFax,
            self.entEmail)]


class ProviderAddition(ProviderEditor, Addition):
    def __init__(self, tab):
        super().__init__(tab)

    def apply(self):
        name = self.trn.getNameSting(self.entName.get())
        if name != '' and self.db.checkName('provider_list', name):
            code = self.db.getNewCode('provider_list')
            date = self.entDate.get()
            phone = self.entPhone.get()
            fax = self.entFax.get()
            email = self.entEmail.get()
            self.db.data['provider_list'].append({
                'code': code,
                'name': name,
                'date': date,
                'phone': phone,
                'fax': fax,
                'email': email})
            self.tab.update()
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
                'Поставщик с таким названием уже добавлен.',
                parent=self.toplevel)


class ProviderEditing(ProviderEditor, Editing):
    def __init__(self, tab):
        super().__init__(tab)

    def fillAndShow(self):
        if self.tv.selection():
            self.clear()
            slcTag = self.tv.selection()[0]
            values = self.tv.item(slcTag)['values']
            [w.insert(0, values[i]) for i, w in enumerate((
                self.entName,
                self.entDate,
                self.entPhone,
                self.entFax,
                self.entEmail))]
            self.show()

    def apply(self):
        name = self.trn.getNameSting(self.entName.get())
        slcTag = self.tv.selection()[0]
        flagName = self.db.checkName('provider_list', name)
        flagCode = self.db.getCode('provider_list', name)
        if name != '' and flagName or flagCode == int(slcTag):
            self.tv.set(slcTag, 0, name)
            [self.tv.set(slcTag, i, w.get()) for i, w in enumerate(
                [self.entDate, self.entPhone, self.entFax, self.entEmail],
                start=1)]
            for rec in self.db.data['provider_list']:
                if rec['code'] == int(slcTag):
                    rec['name'] = name
                    rec['date'] = self.entDate.get()
                    rec['phone'] = self.entPhone.get()
                    rec['fax'] = self.entFax.get()
                    rec['email'] = self.entEmail.get()
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
                'Поставщик с таким названием уже добавлен.',
                parent=self.toplevel)
