from general.rig_tk import Entry
from tkinter import END, messagebox
from tkinter.ttk import Label
from general.topTemplates import Editor, Addition, Editing


class ManufacturerEditor(Editor):
    def __init__(self, tab):
        super().__init__(tab)
        lblName = Label(self.frmFields, text='Название')
        self.entName = Entry(self.frmFields)
        lblName.grid(row=0, **self.grd.cl0_pdSt)
        self.entName.grid(row=0, **self.grd.cl1_pdSt)

    def clear(self):
        self.entName.delete(0, END)


class ManufacturerAddition(ManufacturerEditor, Addition):
    def __init__(self, tab):
        super().__init__(tab)

    def apply(self):
        name = self.trn.getNameSting(self.entName.get())
        if name != '' and self.db.checkName('manufacturer_list', name):
            code = self.db.getNewCode('manufacturer_list')
            self.db.data['manufacturer_list'] += [{'code': code, 'name': name}]
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
                'Изготовитель с таким названием уже добавлен.',
                parent=self.toplevel)


class ManufacturerEditing(ManufacturerEditor, Editing):
    def __init__(self, tab):
        super().__init__(tab)

    def fillAndShow(self):
        if self.tv.selection():
            self.clear()
            slcTag = self.tv.selection()[0]
            values = self.tv.item(slcTag)['values']
            self.entName.insert(0, values[0])
            self.show()

    def apply(self):
        name = self.trn.getNameSting(self.entName.get())
        slcTag = self.tv.selection()[0]
        flagName = self.db.checkName('manufacturer_list', name)
        flagCode = self.db.getCode('manufacturer_list', name)
        if name != '' and flagName or flagCode == int(slcTag):
            self.tv.set(slcTag, 0, name)
            for rec in self.db.data['manufacturer_list']:
                if rec['code'] == int(slcTag):
                    rec['name'] = name
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
                'Изготовитель с таким названием уже добавлен.',
                parent=self.toplevel)
