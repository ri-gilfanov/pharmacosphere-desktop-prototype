from .rig_tk import Combobox, Entry
from tkinter import END
from tkinter.filedialog import askopenfilename
from tkinter.ttk import \
    Button, Frame, Label, \
    Progressbar, Scrollbar, Treeview
from re import findall
from gc import collect
import sys
sys.path.append('general/external/')
from xlrd import open_workbook, cellname


class Tab():
    def __init__(self, basis):
        self.basis = basis
        self.tk = basis.tk
        self.db = basis.db
        self.frmTab = Frame(self.tk)
        self.grd = basis.grd
        self.vld = basis.vld
        self.trn = basis.trn


class SearchBlock(Tab):
    def __init__(self, basis):
        super().__init__(basis)
        self.frmSearch = Frame(self.frmTab)
        self.lblSearch = Label(self.frmSearch, text='Поиск')
        self.entSearch = Entry(self.frmSearch, width=32)
        self.lblSearch.grid(row=0, column=0, padx=5, pady=10)
        self.entSearch.grid(row=0, column=1, padx=5, pady=10, sticky='w, e')
        self.entSearch.bind('<KeyRelease>', self.search)

    def search(self, event):
        strRequest = self.entSearch.get()
        if len(strRequest) >= 3:
            requestList = self.trn.getWrdList(strRequest)
        else:
            requestList = None
        self.update(requestList)

    def update(self, requestList=None):
        pass


class ViewBlock(Tab):
    def __init__(self, basis):
        super().__init__(basis)
        self.frmView = Frame(self.frmTab)
        self.tv = Treeview(self.frmView, selectmode='browse')
        scrVer = Scrollbar(self.frmView)
        scrHor = Scrollbar(self.frmView, orient='hor')
        scrVer['command'] = self.tv.yview
        scrHor['command'] = self.tv.xview
        self.tv['yscrollcommand'] = scrVer.set
        self.tv['xscrollcommand'] = scrHor.set
        self.frmView.grid_rowconfigure(0, weight=1)
        self.frmView.grid_columnconfigure(0, weight=1)
        self.tv.grid(row=0, column=0, sticky='nesw')
        scrVer.grid(row=0, column=1, sticky='ns')
        scrHor.grid(row=1, column=0, sticky='we')


class EditBlock(Tab):
    def __init__(self, basis):
        super().__init__(basis)
        self.frmEdit = Frame(self.frmTab)
        self.btnAdd = Button(self.frmEdit, text='Добавить запись')
        self.btnChn = Button(self.frmEdit, text='Изменить запись')
        btnDel = Button(self.frmEdit, text='Удалить запись')
        btnSav = Button(self.frmEdit, text='Сохранить БД в файл')
        btnRst = Button(self.frmEdit, text='Перезагрузить БД из файла')
        [b.grid(row=0, column=c, padx=5, pady=10) for c, b in enumerate([
            self.btnAdd, self.btnChn, btnDel, btnSav, btnRst])]
        btnDel['command'] = self.delete
        btnSav['command'] = self.db.saveData
        btnRst['command'] = self.reset

    def delete(self):
        pass

    def reset(self):
        pass


class StandartTab(SearchBlock, ViewBlock, EditBlock):
    def __init__(self, basis):
        super().__init__(basis)
        self.frmSearch.pack(fill='x')
        self.frmView.pack(expand=True, fill='both')
        self.frmEdit.pack()
        self.frmTab.pack()

    def updateView(self, requestList, iid, text, value):
        if not requestList:
            self.tv.insert(
                parent='', index='end', iid=iid, text=text, value=value)
        else:
            string = ''
            if value:
                string = value[0]
            else:
                string = text
            lenRequest, coincidence = len(requestList), 0
            for request in requestList:
                if request.lower() in string.lower():
                    coincidence += 1
            if coincidence == lenRequest:
                self.tv.insert(
                    parent='', index='end', iid=iid, text=text, value=value)


class XlsTab(ViewBlock):
    def __init__(self, basis):
        super().__init__(basis)
        self.xlsData = None
        self.frmTab.grid_rowconfigure(2, weight=1)
        self.frmTab.grid_columnconfigure(1, weight=1)

        self.frmFile = Frame(self.frmTab)
        self.btnOpen = Button(
            self.frmFile, command=self.clickBtnOpen, text='Открыть')
        self.lblPath = Label(self.frmFile, text='')

        self.frmOptions = Frame(self.frmTab)
        self.frmOptions.grid_columnconfigure(0, weight=1)
        
        self.argOpt_wd6 = {'master': self.frmOptions, 'width': 6}
        self.argOptionCell = dict(self.argOpt_wd6, **self.vld.vldCell)
        self.argOptionDate = dict(self.argOpt_wd6, **self.vld.vldDate)
        self.argOptionInteger = dict(self.argOpt_wd6, **self.vld.vldInt)
        self.argOptionReadonly = dict(self.argOpt_wd6, **{'state': 'readonly'})
        
        self.lblSheet = Label(self.frmOptions, text='Лист Excel №: ')
        self.lblCellRange = Label(self.frmOptions, text='Диапазон ячеек: ')
        self.cmbSheet = Combobox(**self.argOptionReadonly)
        self.entCellStart = Entry(**self.argOptionCell)
        self.entCellFinish = Entry(**self.argOptionCell)
        
        self.lblSheet.grid(row=0, **self.grd.cl0_pdSt_stW)
        self.cmbSheet.grid(row=0, **self.grd.cl1_sp2_pdSt_stWE)
        self.lblCellRange.grid(row=1, **self.grd.cl0_pdSt_stW)
        self.entCellStart.grid(row=1, sticky='w, e', **self.grd.cl1_pdSt)
        self.entCellFinish.grid(
            row=1, column=2, sticky='w, e', **self.grd.pdSt)

        self.cmbSheet.bind('<<ComboboxSelected>>', self.selectData)
        self.entCellStart.bind('<KeyRelease>', self.selectData)
        self.entCellFinish.bind('<KeyRelease>', self.selectData)

        self.frmProgress = Frame(self.frmTab)
        self.frmProgress.grid_columnconfigure(0, weight=1)
        self.lblProgress = Label(self.frmProgress)
        self.prgProgress = Progressbar(self.frmProgress, mode='determinate')
        self.lblProgress.grid(row=0, column=0, padx=5, pady=0, sticky='w, e')
        self.prgProgress.grid(row=1, column=0, padx=5, pady=0, sticky='w, e')

        self.frmView.grid_propagate(False)
        self.frmFile.grid(row=0, columnspan=2, **self.grd.cl0_pdSt_stW)
        self.frmOptions.grid(row=1, sticky='n, e, s, w', **self.grd.cl0_pdSt)
        self.frmView.grid(
            row=1, sticky='n, e, s, w', rowspan=2, **self.grd.cl1_pdSt)
        self.frmProgress.grid(
            row=3, sticky='w, e', columnspan=2, **self.grd.cl0_pdSt)

    def getScope(self):
        self.resetOptions()
        self.resetView()
        lastRow = len(self.xlsData[self.sheetID]) - 1
        lastCol = len(self.xlsData[self.sheetID][0]) - 1
        cellStart = self.entCellStart.get()
        cellFinish = self.entCellFinish.get()
        self.colStart, self.rowStart = self.getCellID(cellStart)
        self.colFinish, self.rowFinish = self.getCellID(cellFinish)
        if self.rowStart > self.rowFinish:
                self.rowStart, self.rowFinish = self.rowFinish, self.rowStart
        if self.colStart > self.colFinish:
                self.colStart, self.colFinish = self.colFinish, self.colStart
        if self.colFinish > lastCol:
                self.colFinish = lastCol
        if self.rowFinish > lastRow:
                self.rowFinish = lastRow

    def clickBtnOpen(self):
        self.path = askopenfilename(
            filetypes=[('Microsoft Excel 97/2003', '.xls')])
        if self.path:
            self.lblPath['text'] = self.path.split('/').pop()
            self.openFile()

    def getColID(self, string):
        string, strSymbols = string.lower(), 'abcdefghijklmnopqrstuvwxyz'
        lenSymbols, number = len(strSymbols), -1
        while string != '':
            lenString = len(string)
            if lenString - 1:
                order = (lenString - 1) * lenSymbols
            else:
                order = 1
            for index in range(lenSymbols):
                if string[0] == strSymbols[index]:
                    number += (index + 1) * order
            string = string[1:]
        return(number)

    def getCellID(self, string):
        try:
            colID = self.getColID(findall('([A-z]+)', string)[0])
            rowID = int(findall('(\d+)', string)[0]) - 1
        except IndexError:
            colID, rowID = 0, 0
        return(colID, rowID)

    def openFile(self):
        self.entCellStart.delete(0, END)
        self.entCellFinish.delete(0, END)
        book = open_workbook(
            filename=self.path, encoding_override='cp1251')
        self.cmbSheet['values'] = [
            (sheetID + 1) for sheetID in range(book.nsheets)]
        sheets = [
            book.sheet_by_index(sheetID) for sheetID in range(book.nsheets)]
        self.xlsData = []
        for sheetID, sheet in enumerate(sheets):
            self.xlsData.append([])
            for colID in range(sheet.nrows):
                self.xlsData[sheetID].append(sheet.row_values(colID))
        if self.cmbSheet['values']:
            self.cmbSheet.set(self.cmbSheet['values'][0])
            if sheets[0].nrows > 0 and sheets[0].ncols > 0:
                self.entCellStart.insert(0, 'A1')
                self.entCellFinish.insert(
                    0, cellname(sheets[0].nrows - 1, sheets[0].ncols - 1))
        book, sheets = None, None
        collect()
        self.selectData()

    def closeFile(self):
        self.xlsData = None
        self.lblPath['text'] = ''
        self.cmbSheet.set('')
        self.cmbSheet['values'] = []
        self.resetOptions()
        self.resetView()

    def resetOptions(self):
        pass

    def resetView(self):
        pass

    def progress(self, string, index, strLen):
        self.lblProgress['text'] = '%s%s%s%s%s%s' % (
            string, '. Обработано ', str(index), ' из ', strLen, '.')
        self.prgProgress['value'] = index
        self.tk.update()
