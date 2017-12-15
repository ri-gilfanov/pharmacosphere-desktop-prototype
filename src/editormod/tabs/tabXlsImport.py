from general.rig_tk import Combobox, Entry, Searchbox
from general.tabTemplates import XlsTab
from tkinter import END
from tkinter.ttk import Button, Label
import sys
sys.path.append('general/external/')
from xlrd import colname


class ImportXlsTab(XlsTab):
    def __init__(self, basis):
        super().__init__(basis)
        self.path = ''
        self.btnClose = Button(
            self.frmFile,
            text='Закрыть',
            command=self.closeFile)
        [w.grid(row=0, column=i, sticky='w', **self.grd.pdSt)
            for i, w in enumerate([
                self.btnOpen, self.btnClose, self.lblPath])]
        [Label(self.frmOptions, text=s).grid(row=i, **self.grd.cl0_pdSt_stW)
            for i, s in enumerate([
                'Наименование:',
                'Изготовитель:',
                'Цена:',
                'Срок годности:'], start=2)]
        lblProvider = Label(
            self.frmOptions, text='Название поставщика:')
        lblPriceDate = Label(
            self.frmOptions, text='Дата прайса: ')
        self.cmbItmCol, self.cmbMnfCol, self.cmbPrcCol, self.cmbExpDtCol = [
            Combobox(**self.argOptionReadonly) for i in range(4)]
        self.cmbProvider = Searchbox(
            postcommand=self.update_provider_list,
            source=[d['name'] for d in self.db.data['provider_list']],
            **self.argOpt_wd6)
        self.entPriceDate = Entry(**self.argOptionDate)
        self.btnImportData = Button(
            self.frmOptions,
            text='Импортировать данные',
            command=self.importData)
        [w.grid(row=i, **self.grd.cl1_sp2_pdSt_stWE) for i, w in enumerate(
            (self.cmbItmCol, self.cmbMnfCol, self.cmbPrcCol, self.cmbExpDtCol),
            start=2)]
        lblProvider.grid(row=6, **self.grd.cl0_sp3_pdSt_stWE)
        self.cmbProvider.grid(row=7, **self.grd.cl0_sp3_pdSt_stWE)
        lblPriceDate.grid(row=8, **self.grd.cl0_pdSt_stW)
        self.entPriceDate.grid(row=8, **self.grd.cl1_sp2_pdSt_stWE)
        self.btnImportData.grid(row=9, **self.grd.cl0_sp3_pdSt_stWE)
        [w.bind('<<ComboboxSelected>>', self.previewData) for w in (
            self.cmbItmCol,
            self.cmbMnfCol,
            self.cmbPrcCol,
            self.cmbExpDtCol)]
        self.frmTab.pack()

    def update_provider_list(self, event=None):
        values = [d['name'] for d in self.db.data['provider_list']]
        self.cmbProvider.source = values
        self.cmbProvider.filter_values()

    def selectData(self, event=None):
        self.resetOptions()
        self.resetView()
        self.sheetID = self.trn.getNatMnsOrZero(self.cmbSheet.get())
        if self.xlsData and len(self.xlsData[self.sheetID]):
            self.getScope()
            values = [(colname(colID)) for colID in range(
                self.colStart, self.colFinish + 1)]
            values.insert(0, '')
            self.cmbItmCol['values'] = values
            self.cmbMnfCol['values'] = values
            self.cmbPrcCol['values'] = values
            self.cmbExpDtCol['values'] = values

    def previewData(self, event=None):
        self.resetView()
        self.getParameters()
        self.tv.heading('#0', text='Строка')
        self.tv.column('#0', minwidth=50, stretch=True, width=75)
        columns = []
        if self.itmColID > -1:
            columns.append('item')
        if self.mnfColID > -1:
            columns.append('manufacturer')
        if self.prcColID > -1:
            columns.append('price')
        if self.expDtColID > -1:
            columns.append('date')
        self.tv['columns'] = columns
        columnsLength = len(columns)
        colWidth = (self.tv.winfo_width() - 75) // columnsLength
        colMinWidth = colWidth // 2
        tvArgs = {'minwidth': colMinWidth, 'stretch': True, 'width': colWidth}
        if self.itmColID > -1:
            self.tv.heading('item', text='Наименование')
            self.tv.column('item', **tvArgs)
        if self.mnfColID > -1:
            self.tv.heading('manufacturer', text='Изготовитель')
            self.tv.column('manufacturer', **tvArgs)
        if self.prcColID > -1:
            self.tv.heading('price', text='Цена')
            self.tv.column('price', anchor='e', **tvArgs)
        if self.expDtColID > -1:
            self.tv.heading('date', text='Срок годности')
            self.tv.column('date', anchor='c', **tvArgs)
        for rowID in range(self.rowStart, self.rowFinish + 1):
            tag = str(rowID)
            self.tv.insert(parent='', index='end', iid=tag, text=rowID + 1)
            valueID, row = 0, self.xlsData[self.sheetID][rowID]
            for colID in (
                self.itmColID, self.mnfColID, self.prcColID, self.expDtColID
            ):
                if colID > -1:
                    self.tv.set(tag, valueID, row[colID])
                    valueID += 1

    def importData(self):
        self.getParameters()
        prvName = self.trn.getNameSting(self.cmbProvider.get())
        priceDate = self.entPriceDate.get()
        providerCode = self.db.getCode('provider_list', prvName)
        if prvName != '' and providerCode == -1:
            providerCode = self.db.getNewCode('provider_list')
            self.db.data['provider_list'].append({
                'code': self.db.getNewCode('provider_list'),
                'name': prvName,
                'date': priceDate,
                'phone': '',
                'fax': '',
                'email': ''})
            self.lblProgress['text'] = 'Добавлен поставщик %s.' % (prvName)
        elif priceDate != '' and providerCode > -1:
            for provider in self.db.data['provider_list']:
                if provider['code'] == providerCode:
                    provider['date'] = priceDate
                    self.lblProgress['text'] = (
                        'Обновлена дата прайса для поставщика %s.' % (prvName))
                    break
        if self.itmColID > -1 or self.mnfColID > -1:
            length = len(
                self.xlsData[self.sheetID][self.rowStart:self.rowFinish]) + 1
            strLen = str(length)
            self.prgProgress['maximum'] = length
            self.db.clear_records_from_provider(providerCode)
            for index, rowID in enumerate(
                    range(self.rowStart, self.rowFinish + 1)):
                itmName = self.xlsData[self.sheetID][rowID][self.itmColID]
                print(itmName)
                itmName = self.trn.getNameSting(itmName)
                itmCode = self.db.getCode('item_list', itmName)
                mnfName = self.xlsData[self.sheetID][rowID][self.mnfColID]
                mnfName = self.trn.getNameSting(mnfName)
                mnfСode = self.db.getCode('manufacturer_list', mnfName)
                price = self.xlsData[self.sheetID][rowID][self.prcColID]
                price = self.trn.getFltOrZero(price)
                expiryDate = self.xlsData[self.sheetID][rowID][self.expDtColID]
                expiryDate = self.trn.getNameSting(expiryDate)
                '''Импорт наименований'''
                if self.itmColID > -1:
                    if itmCode == -1:
                        itmCode = self.db.getNewCode('item_list')
                        self.db.data['item_list'].append({
                            'code': itmCode,
                            'name': itmName,
                            'substance': '',
                            'markup': 0,
                            'manufacturers': []})
                '''Импорт изготовителей'''
                if self.mnfColID > -1:
                    if mnfСode == -1:
                        mnfСode = self.db.getNewCode('manufacturer_list')
                        self.db.data['manufacturer_list'].append({
                            'code': mnfСode,
                            'name': mnfName})
                '''Импорт наименований'''
                if self.itmColID > -1 and self.mnfColID > -1:
                    itemLast = self.db.data['item_list'][len(self.db.data['item_list']) - 1]
                    itemMnfs = itemLast['manufacturers']
                    if mnfСode > -1 and mnfСode not in itemMnfs:
                        itemMnfs.append(mnfСode)
                '''Импорт в общий прайс'''
                if prvName != '' and self.itmColID > -1 and self.mnfColID > -1:
                    offerCode = [itmCode, mnfСode, providerCode]
                    repeatFlag = True
                    for offer in self.db.data['price_list']:
                        if offer['code'] == offerCode:
                            offer['price'] = price
                            offer['date'] = expiryDate
                            repeatFlag = False
                            break
                    if repeatFlag is True:
                        self.db.data['price_list'].append({
                            'code': offerCode,
                            'price': price,
                            'date': expiryDate})
                self.progress('Импорт записей', index + 1, strLen)
            self.progress('Импорт завершён', index + 1, strLen)
            self.db.saveData()
            self.basis.prcTab.reset()

    def getParameters(self):
        self.itmColID, self.mnfColID, self.prcColID, self.expDtColID = [
            self.getColID(w.get()) for w in [
                self.cmbItmCol,
                self.cmbMnfCol,
                self.cmbPrcCol,
                self.cmbExpDtCol]]

    def resetOptions(self):
        [w.delete(0, END) for w in (
            self.cmbItmCol,
            self.cmbMnfCol,
            self.cmbPrcCol,
            self.cmbExpDtCol)]

    def resetView(self):
        for rec in self.tv.get_children():
            self.tv.delete(rec)
        self.tv['columns'] = []
        self.tv.heading('#0', text='')
        self.tv.column('#0', stretch=True, width=self.tv.winfo_reqwidth() - 2)
