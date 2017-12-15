from general.rig_tk import Combobox, Entry
from tkinter import END, Text, WORD
from tkinter.ttk import Button, Label, Scrollbar
from general.topTemplates import Editor


class ColumnCombiner(Editor):
    def __init__(self, tab):
        super().__init__(tab)
        self.toplevel.title('Объединить колонки')
        [Label(self.frmFields, text=s).grid(row=0, column=i, **self.grd.pdSt)
            for i, s in enumerate([
                'Начало строки',
                'Колонка №1',
                'Середина',
                'Колонка №2',
                'Окончание'])]
        self.entBfr, self.entMdl, self.entAft = [
            Entry(self.frmFields, width=12, justify='center')
            for i in range(3)]
        self.cmbColA, self.cmbColB = [
            Combobox(self.frmFields, width=8, state='readonly')
            for i in range(2)]
        self.lblPreview = Label(self.frmFields)
        [w.grid(row=1, column=i, **self.grd.pdSt) for i, w in enumerate((
            self.entBfr,
            self.cmbColA,
            self.entMdl,
            self.cmbColB,
            self.entAft))]
        self.lblPreview.grid(row=2, columnspan=5, **self.grd.cl0_pdSt)
        self.okButton['text'] = 'Объединить'
        [w.bind('<KeyRelease>', self.preview) for w in (
            self.entBfr, self.entMdl, self.entAft)]
        [w.bind('<<ComboboxSelected>>', self.preview) for w in (
            self.cmbColA, self.cmbColB)]
        self.okButton['command'] = self.tab.combineColumns

    def clear(self):
        [w.delete(0, END) for w in (
            self.entBfr, self.entMdl, self.entAft, self.cmbColA, self.cmbColB)]
        self.cmbColA.set('')
        self.cmbColB.set('')
        self.lblPreview['text'] = ''

    def fillAndShow(self):
        if self.tv.selection():
            self.slcTag = self.tv.selection()[0]
        elif self.tv.get_children():
            self.slcTag = self.tv.get_children()[0]
        if self.slcTag:
            self.clear()
            self.cmbColA['values'] = self.tv['columns']
            self.cmbColB['values'] = self.tv['columns']
            self.lblPreview['wraplength'] = self.toplevel.winfo_reqwidth() - 12
            self.show()

    def preview(self, event=None):
        self.lblPreview['text'] = ''
        if self.slcTag:
            strColA = self.cmbColA.get()
            strColB = self.cmbColB.get()
            self.idColA = self.tab.getColID(strColA)
            self.idColB = self.tab.getColID(strColB)
            self.strBefore = self.entBfr.get()
            self.strMiddle = self.entMdl.get()
            self.strAfter = self.entAft.get()
            values = self.tv.item(self.slcTag)['values']
            self.lblPreview['text'] += self.strBefore
            for index in range(len(self.cmbColA['values'])):
                if strColA == self.cmbColA['values'][index]:
                    self.lblPreview['text'] += values[index]
            self.lblPreview['text'] += self.strMiddle
            for index in range(len(self.cmbColB['values'])):
                if strColB == self.cmbColB['values'][index]:
                    self.lblPreview['text'] += values[index]
            self.lblPreview['text'] += self.strAfter


class ColumnDeleter(Editor):
    def __init__(self, tab):
        super().__init__(tab)
        self.slcTag = None
        self.idColumn = None
        self.toplevel.title('Удалить колонку')
        lblColumn = Label(self.frmFields, text='Выберите колонку для удаления')
        self.cmbColumn = Combobox(self.frmFields, width=8, state='readonly')
        lblColumn.grid(row=0, **self.grd.cl1_pdSt)
        self.cmbColumn.grid(row=1, **self.grd.cl1_pdSt)
        self.okButton['text'] = 'Удалить'
        self.okButton['command'] = self.tab.deleteColumn

    def clear(self):
        self.cmbColumn.set('')
        self.cmbColumn.delete(0, END)

    def fillAndShow(self):
        self.clear()
        self.cmbColumn['values'] = self.tv['columns']
        self.show()


class ReplacerInSpSh(Editor):
    def __init__(self, tab):
        super().__init__(tab)
        self.toplevel.title('Заменить выбранные варианты')
        self.frmFields.grid_columnconfigure(0, weight=1)
        self.frmFields.grid_columnconfigure(1, weight=1)
        self.lblVarA = Label(self.frmFields, text='')
        self.lblVarB = Label(self.frmFields, text='')
        self.btnVarA = Button(
            self.frmFields,
            command=self.selectVarA,
            text='Копировать вариант А')
        self.btnVarB = Button(
            self.frmFields,
            command=self.selectVarB,
            text='Копировать вариант Б')

        [w.grid(row=0, column=i, **self.grd.pdSt) for i, w in enumerate((
            self.lblVarA, self.lblVarB))]
        [w.grid(row=1, column=i, **self.grd.pdSt) for i, w in enumerate((
            self.btnVarA, self.btnVarB))]

        self.txtVarC = Text(self.frmExcess, width=100, height=5, wrap=WORD)
        scrVarC = Scrollbar(self.frmExcess)
        scrVarC['command'] = self.txtVarC.yview
        self.txtVarC['yscrollcommand'] = scrVarC.set
        self.txtVarC.grid(row=0, column=0, sticky='w, e')
        scrVarC.grid(row=0, column=1, sticky='n, s')

        self.okButton['text'] = 'Заменить'
        self.okButton['command'] = self.tab.replaceInSpSh

    def clear(self):
        self.lblVarA['text'] = ''
        self.lblVarB['text'] = ''
        self.txtVarC.delete(1.0, END)

    def fillAndShow(self):
        if self.tv.selection():
            self.clear()
            slcTag = self.tv.selection()[0]
            values = self.tv.item(slcTag)['values']
            self.lblVarA['wraplength'] = (
                self.toplevel.winfo_reqwidth() - 2) // 2
            self.lblVarB['wraplength'] = (
                self.toplevel.winfo_reqwidth() - 2) // 2
            self.lblVarA['text'] = values[0]
            self.lblVarB['text'] = values[1]
            self.show()

    def selectVarA(self):
        self.txtVarC.delete(1.0, END)
        self.txtVarC.insert(1.0, self.lblVarA['text'])

    def selectVarB(self):
        self.txtVarC.delete(1.0, END)
        self.txtVarC.insert(1.0, self.lblVarB['text'])
