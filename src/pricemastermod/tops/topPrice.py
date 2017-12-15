from general.rig_tk import Entry, Searchbox
from tkinter import END, messagebox
from tkinter.ttk import Label
from general.topTemplates import Addition, Editing


class PriceAddition(Addition):
    def __init__(self, tab):
        super().__init__(tab)
        [Label(self.frmFields, text=s).grid(row=i, **self.grd.cl0_pdSt)
            for i, s in enumerate([
                'Изготовитель', 'Цена', 'Срок годности'])]
        self.cmbManufacturer = Searchbox(
            master=self.frmFields,
            postcommand=self.update_manufacturer_list,
            width=32)
        self.entPrice = Entry(self.frmFields, width=12, **self.vld.vldFlt2)
        self.entDate = Entry(self.frmFields, width=12, **self.vld.vldDate)

        self.cmbManufacturer.grid(row=0, **self.grd.cl1_pdSt)
        self.entPrice.grid(row=1, sticky='w', **self.grd.cl1_pdSt)
        self.entDate.grid(row=2, sticky='w', **self.grd.cl1_pdSt)
        self.lblHint = Label(self.frmFields)
        self.lblHint.grid(row=3, columnspan=2, **self.grd.pdSt)
        self.lblHint['wraplength'] = self.toplevel.winfo_reqwidth() - 8
        hintA = 'Поле изготовитель — раскрывающийся список с вариантами выбора и встроенным поиском.'
        hintB = 'Клавиши ↑, ↓ — раскрыть список и перемещаться по вариантам, Esc — скрыть, Enter — выбрать.'
        hintC = 'Чтобы вернуть все варианты — очистите соответствующее поле ввода.'
        self.lblHint['text'] = '\n%s\n\n%s\n\n%s' % (hintA, hintB, hintC)
        self.toplevel.bind('<Configure>', self.hint_resize)

    def hint_resize(self, event):
        self.lblHint['wraplength'] = self.toplevel.winfo_reqwidth() - 8

    def fillAndShow(self):
        self.clear()
        self.show()

    def update_manufacturer_list(self, event=None):
        selected_tag = None
        if self.tv.selection():
            if len(self.tv.parent(self.tv.selection()[0])) == 0:
                selected_tag = self.tv.selection()[0]
            elif len(self.tv.parent(self.tv.selection()[0])) > 0:
                selected_tag = self.tv.parent(self.tv.selection()[0])
        if selected_tag is not None:
            itemName = self.tv.item(int(selected_tag))['text']
            itemCode = self.db.getCode('item_list', itemName)
            for record in self.db.data['item_list']:
                if record['code'] == itemCode:
                    mcl = record['manufacturers']
                    break
            values = [self.db.getName('manufacturer_list', i) for i in mcl]
            self.cmbManufacturer.source = values
            self.cmbManufacturer.filter_values()

    def apply(self):
        if len(self.tv.parent(self.tv.selection()[0])) == 0:
            slcParentTag = self.tv.selection()[0]
        elif len(self.tv.parent(self.tv.selection()[0])) > 0:
            slcParentTag = self.tv.parent(self.tv.selection()[0])

        itemCode = int(slcParentTag)
        providerCode = self.db.data['provider']['code']
        manufacturerName = self.cmbManufacturer.get()
        manufacturerCode = self.db.getCode('manufacturer_list', manufacturerName)
        code = [itemCode, manufacturerCode, providerCode]

        repeatFlag = True
        for offer in self.db.data['price_list']:
            if offer['code'] == code:
                repeatFlag = False
                break

        price = self.trn.getFltOrZero(self.entPrice.get())
        date = self.entDate.get()
        tag = '%i.%i.%i' % (itemCode, manufacturerCode, providerCode)

        mcl = self.db.data['item_list'][itemCode]['manufacturers']
        if (repeatFlag is True and
                manufacturerCode != -1 and
                manufacturerCode in mcl and
                providerCode != -1):
            self.db.data['price_list'] += [{
                'code': code, 'price': price, 'date': date}]
            providerName = self.db.data['provider']['name']
            manufacturerName = self.db.getName(
                'manufacturer_list', manufacturerCode)
            strPrice = '{:.2f}'.format(price)
            value = [manufacturerName, providerName, strPrice, date]
            self.tv.insert(slcParentTag, 'end', iid=tag, text=tag, value=value)
            self.endAddition(tag)

        elif repeatFlag is False:
            messagebox.showerror(
                'Ошибка',
                'Предложение поставщика c кодом %s уже добавлено.' % (tag),
                parent=self.toplevel)

        elif manufacturerCode == -1:
            messagebox.showerror(
                'Ошибка',
                'Указанный изготовитель не найден.',
                parent=self.toplevel)

        elif manufacturerCode not in mcl:
            messagebox.showerror(
                'Ошибка',
                'Изготовитель не ассоциирован с выбранным наименованием.',
                parent=self.toplevel)

        elif providerCode == -1:
            messagebox.showerror(
                'Ошибка',
                'Название и код поставщика следует указать в настройках "Информация о поставщике".',
                parent=self.toplevel)

    def clear(self):
        self.cmbManufacturer.set('')
        [w.delete(0, END) for w in (
            self.cmbManufacturer,
            self.entPrice,
            self.entDate)]


class PriceEditing(Editing):
    def __init__(self, tab):
        super().__init__(tab)
        [Label(self.frmFields, text=s).grid(row=i, **self.grd.cl0_pdSt)
            for i, s in enumerate([
                'Цена', 'Срок годности'])]
        self.entPrice = Entry(self.frmFields, width=10, **self.vld.vldFlt2)
        self.entDate = Entry(self.frmFields, width=10, **self.vld.vldDate)
        self.entPrice.grid(row=0, sticky='w', **self.grd.cl1_pdSt)
        self.entDate.grid(row=1, sticky='w', **self.grd.cl1_pdSt)

    def fillAndShow(self):
        if self.tv.selection()[0]:
            if len(self.tv.parent(self.tv.selection()[0])):
                self.clear()
                slcTag = self.tv.selection()[0]
                values = self.tv.item(slcTag)['values']
                self.entPrice.insert(0, values[1])
                self.entDate.insert(0, values[2])
                self.show()

    def apply(self):
        slcTag = self.tv.selection()[0]
        price = self.trn.getFltOrZero(self.entPrice.get())
        self.tv.set(slcTag, 1, '{:.2f}'.format(price))
        self.tv.set(slcTag, 2, self.entDate.get())
        for rec in self.db.data['price_list']:
            if rec['code'] == [int(x) for x in slcTag.split('.')]:
                rec['price'] = self.trn.getFltOrZero(self.entPrice.get())
                rec['date'] = self.entDate.get()
                break
        self.hide()

    def clear(self):
        [w.delete(0, END) for w in (self.entPrice, self.entDate)]
