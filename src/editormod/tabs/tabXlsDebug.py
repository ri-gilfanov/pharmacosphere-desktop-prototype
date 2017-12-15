from general.rig_tk import Combobox, Entry
from general.tabTemplates import XlsTab
from tkinter import Text, END, WORD
from tkinter.filedialog import asksaveasfilename
from tkinter.ttk import Button, Frame, Label, Scrollbar
from ..tops.topXlsDebug import ColumnCombiner, ColumnDeleter, ReplacerInSpSh
import sys
sys.path.append('general/external/')
from xlrd import colname
from xlwt import Workbook
from gc import collect


class DebugXlsTab(XlsTab):
    def __init__(self, basis):
        super().__init__(basis)
        self.colCombiner = ColumnCombiner(self)
        self.colDeleter = ColumnDeleter(self)
        self.replacerInSpSh = ReplacerInSpSh(self)
        self.path = ''
        self.flag = False

        self.btnSave = Button(
            self.frmFile, command=self.saveFile, text='Сохранить')
        self.btnClose = Button(
            self.frmFile, command=self.closeFile, text='Закрыть')
        [w.grid(row=0, column=i, sticky='w', **self.grd.pdSt)
            for i, w in enumerate((
                self.btnOpen, self.btnSave, self.btnClose, self.lblPath))]

        lblCheckArea = Label(
            self.frmOptions, text='Область проверки:')
        lblCheckType = Label(
            self.frmOptions, text='Тип проверки:')
        lblColumn = Label(
            self.frmOptions, text='Колонка: ')
        lblSymbRange = Label(
            self.frmOptions, text='Фрагмент строк: ')
        self.lblLimit = Label(
            self.frmOptions, text='Мин. совпадений: ')
        lblIgnNum = Label(
            self.frmOptions, text='Игнорировать числа: ')
        lblIgnWrd = Label(
            self.frmOptions, text='Игнорировать сочетания: ')
        self.cmbCheckArea = Combobox(
            values=(
                'Колонка электронной таблицы',
                'Колонка ЭТ и наименования в БД',
                'Колонка ЭТ и изготовители в БД'),
            **self.argOptionReadonly)
        self.cmbCheckType = Combobox(
            values=(
                'Сравнение по словам',
                'Поиск слов в строке',
                'По-символьное сравнение'),
            **self.argOptionReadonly)
        self.cmbColumn = Combobox(**self.argOptionReadonly)
        self.entSymbStart = Entry(**self.argOptionInteger)
        self.entSymbFinish = Entry(**self.argOptionInteger)
        self.entLimit = Entry(**self.argOptionInteger)
        self.cmbIgnNum = Combobox(
            values=('Да', 'Нет'), **self.argOptionReadonly)

        frmIgnWrd = Frame(self.frmOptions)
        frmIgnWrd.grid_columnconfigure(0, weight=1)
        self.txtIgnWrd = Text(frmIgnWrd, width=35, height=5, wrap=WORD)
        scrIgnWrd = Scrollbar(frmIgnWrd)
        scrIgnWrd['command'] = self.txtIgnWrd.yview
        self.txtIgnWrd['yscrollcommand'] = scrIgnWrd.set
        self.txtIgnWrd.grid(row=0, column=0, sticky='w, e')
        scrIgnWrd.grid(row=0, column=1, sticky='n, s')

        self.btnCheck = Button(
            self.frmOptions,
            text='Начать проверку',
            command=self.check)
        self.btnShow = Button(
            self.frmOptions,
            text='Вернуться к просмотру таблицы',
            command=self.selectData)

        [w.grid(row=i, **self.grd.cl0_sp3_pdSt_stWE) for i, w in enumerate(
            (lblCheckArea, self.cmbCheckArea, lblCheckType, self.cmbCheckType),
            start=2)]
        [w.grid(row=i, **self.grd.cl0_pdSt_stW) for i, w in enumerate((
            lblColumn, lblSymbRange, self.lblLimit, lblIgnNum), start=6)]
        self.cmbColumn.grid(row=6, **self.grd.cl1_sp2_pdSt_stWE)
        self.entSymbStart.grid(row=7, sticky='w, e', **self.grd.cl1_pdSt)
        self.entSymbFinish.grid(
            row=7, column=2, sticky='w, e', **self.grd.pdSt)
        self.entLimit.grid(row=8, **self.grd.cl1_sp2_pdSt_stWE)
        self.cmbIgnNum.grid(row=9, **self.grd.cl1_sp2_pdSt_stWE)
        [w.grid(row=i, **self.grd.cl0_sp3_pdSt_stWE) for i, w in enumerate((
            lblIgnWrd, frmIgnWrd, self.btnCheck), start=10)]

        self.cmbCheckType.bind('<<ComboboxSelected>>', self.selectCheckType)

        self.frmEdit = Frame(self.frmView)
        self.frmEdit.grid_columnconfigure(0, weight=1)
        self.frmEdit.grid_columnconfigure(2, weight=1)
        self.btnUniteCols = Button(
            self.frmEdit,
            text='Объединить колонки по шаблону',
            command=self.colCombiner.fillAndShow)
        self.btnDelCol = Button(
            self.frmEdit,
            text='Удалить колонку',
            command=self.colDeleter.fillAndShow)
        self.btnDelRow = Button(
            self.frmEdit, text='Удалить строку', command=self.deleteRow)
        self.btnReplaceInSpSh = Button(
            self.frmEdit,
            text='Заменить выбранные варианты в электронной таблице',
            command=self.replacerInSpSh.fillAndShow)
        self.btnReplaceFromDB = Button(
            self.frmEdit,
            text='Заменить выбранный вариант в ЭТ на вариант из БД',
            command=self.replaceFromDB)

        self.frmEdit.grid(row=2, sticky='n, e, s, w', **self.grd.cl0_pdSt)
        self.frmTab.pack()

    def saveFile(self):
        self.path = asksaveasfilename(
            defaultextension='.xls',
            filetypes=[('Microsoft Excel 97/2003', '.xls')])
        if self.path:
            book = Workbook(encoding='cp1251')
            sheets = []
            for sheetID in range(len(self.xlsData)):
                sheets.append(book.add_sheet('Sheet' + str(sheetID)))
                lenRows = len(self.xlsData[sheetID])
                for rowID in range(lenRows):
                    lenCols = len(self.xlsData[sheetID][rowID])
                    for colID in range(lenCols):
                        sheets[sheetID].write(
                            r=rowID,
                            c=colID,
                            label=self.xlsData[sheetID][rowID][colID])
            book.save(self.path)
            book, sheets = None, None
            collect()

    def selectCheckType(self, event):
        if self.cmbCheckType.get() == 'По-символьное сравнение':
            self.lblLimit['text'] = 'Макс. отличий: '
        else:
            self.lblLimit['text'] = 'Мин. совпадений: '

    def selectData(self, event=None):
        self.resetOptions()
        self.resetView()
        self.sheetID = self.trn.getNatMnsOrZero(self.cmbSheet.get())
        if self.xlsData and len(self.xlsData[self.sheetID]):
            self.getScope()
            self.tv.heading('#0', text='Строка')
            self.tv.column('#0', minwidth=50, stretch=True, width=75)
            self.tv['columns'] = [
                colname(colID) for colID in range(
                    self.colStart, self.colFinish + 1)]
            for rowID in range(self.rowStart, self.rowFinish + 1):
                tag = str(rowID)
                self.tv.insert(parent='', index='end', iid=tag, text=rowID + 1)
                for valueID, colID in enumerate(range(self.colStart, self.colFinish + 1)):
                    colName = colname(colID)
                    self.tv.heading(colName, text=colName)
                    self.tv.column(colName, minwidth=50, stretch=True, width=150)
                    cell = self.xlsData[self.sheetID][rowID][colID]
                    self.tv.set(tag, valueID, cell)
            self.cmbColumn['values'] = [
                colname(colID) for colID in range(
                    self.colStart, self.colFinish + 1)]
            [b.grid(row=0, column=i, **self.grd.pdSt) for i, b in enumerate((
                self.btnUniteCols, self.btnDelCol, self.btnDelRow))]

    def combineColumns(self):
        idColA = self.colCombiner.idColA
        idColB = self.colCombiner.idColB
        strBfr = self.colCombiner.strBefore
        strMdl = self.colCombiner.strMiddle
        strAft = self.colCombiner.strAfter
        if idColA != idColB:
            for row in self.xlsData[self.sheetID]:
                strColA, strColB = str(row[idColA]), str(row.pop(idColB))
                row[idColA] = '%s%s%s%s%s' % (
                    strBfr, strColA, strMdl, strColB, strAft)
            self.colFinish -= 1
            self.selectData()
            self.colCombiner.hide()
            self.colCombiner.clear()

    def deleteColumn(self):
        idColumn = self.getColID(self.colDeleter.cmbColumn.get())
        if idColumn >= 0:
            for row in self.xlsData[self.sheetID]:
                row.pop(idColumn)
            self.selectData()
            self.colDeleter.hide()
            self.colDeleter.clear()

    def deleteRow(self):
        if self.tv.selection():
            slcTag = self.tv.selection()[0]
            for rowID in range(self.rowStart, self.rowFinish + 1):
                if rowID == int(slcTag):
                    self.xlsData[self.sheetID].pop(rowID)
                    break
            self.tv.delete(slcTag)

    def check(self):
        def coincidenceFlag(count, limit):
            if count >= limit and count >= 1:
                return(True)
            else:
                return(False)

        def distanceFlag(count, limit):
            if count <= limit:
                return(True)
            else:
                return(False)

        if self.flag is False and self.path:
            self.flag = True
            self.btnCheck['text'] = 'Прервать проверку'
            checkArea = self.cmbCheckArea.get()
            checkType = self.cmbCheckType.get()
            self.checkColumn = self.getColID(self.cmbColumn.get())
            self.symbStart = self.trn.getNatMnsOrZero(self.entSymbStart.get())
            self.symbFinish = self.trn.getNatOrNone(self.entSymbFinish.get())
            self.ignNum = self.trn.getBoolean(self.cmbIgnNum.get())
            self.ignWrd = self.trn.getWrdList(self.txtIgnWrd.get('1.0', END))
            self.limit = self.trn.getNatOrZero(self.entLimit.get())
            '''Отсев повторных'''
            self.columnSpSh = []
            length = len(self.xlsData[self.sheetID][self.rowStart:self.rowFinish])
            strLen = str(length)
            self.prgProgress['maximum'] = length
            for index, row in enumerate(self.xlsData[self.sheetID][self.rowStart:self.rowFinish]):
                if row[self.checkColumn] not in self.columnSpSh:
                    self.columnSpSh.append(row[self.checkColumn])
                self.progress('Отсев повторяющихся строк', index, strLen)
            self.prgProgress['value'] = 0
            self.resetView()
            '''Настройка таблицы'''
            self.tv['columns'] = ['value_A', 'value_B']
            self.tv.column('#0', anchor='e', minwidth=75, stretch=True, width=100)
            self.tv.column('value_A', minwidth=150, stretch=True, width=300)
            self.tv.column('value_B', minwidth=150, stretch=True, width=300)            
            if checkArea == 'Колонка электронной таблицы' or '':
                self.tv.heading('value_A', text='Значение 1')
                self.tv.heading('value_B', text='Значение 2')
            else:
                self.tv.heading('value_A', text='Значение ЭТ')
                self.tv.heading('value_B', text='Значение БД')
            if checkType == 'По-символьное сравнение':
                self.tv.heading('#0', text='Отличий')
            else:
                self.tv.heading('#0', text='Совпадений')
            '''Проверка'''
            result, length = [], len(self.columnSpSh)
            strLen, index = str(length), 0
            self.prgProgress['maximum'] = length
            checkArg = {
                'limit': self.limit,
                'result': result,
                'length': length,
                'strLen': strLen,
                'index': index}
            if checkArea == 'Колонка электронной таблицы' or '':
                self.btnReplaceFromDB.grid_forget()
                if checkType == 'По-символьное сравнение':
                    result = self.checkInSpSh(
                        function=self.getDistance,
                        checkCount=distanceFlag,
                        **checkArg)
                elif checkType == 'Поиск слов в строке':
                    result = self.checkInSpSh(
                        function=self.getCoincidenceWS,
                        checkCount=coincidenceFlag,
                        **checkArg)
                else:
                    result = self.checkInSpSh(
                        function=self.getCoincidenceWW,
                        checkCount=coincidenceFlag,
                        **checkArg)
            else:
                self.btnReplaceInSpSh.grid_forget()
                self.columnDB = []
                if checkArea == 'Колонка ЭТ и наименования в БД':
                    for rec in self.db.data['item_list']:
                        self.columnDB.append(rec['name'])
                elif checkArea == 'Колонка ЭТ и изготовители в БД':
                    for rec in self.db.data['manufacturer_list']:
                        self.columnDB.append(rec['name'])
                if checkType == 'По-символьное сравнение':
                    result = self.checkInDtBs(
                        function=self.getDistance,
                        checkCount=self.distanceFlag,
                        **checkArg)
                elif checkType == 'Поиск слов в строке':
                    result = self.checkInDtBs(
                        function=self.getCoincidenceWS,
                        checkCount=self.coincidenceFlag,
                        **checkArg)
                else:
                    result = self.checkInDtBs(
                        function=self.getCoincidenceWW,
                        checkCount=self.coincidenceFlag,
                        **checkArg)
            '''Сортировка результата'''
            if result:
                if checkType == 'По-символьное сравнение':
                    result.sort(key=lambda e: e[0])
                else:
                    result.sort(key=lambda e: e[0], reverse=True)
            '''Вывод'''
            length = len(result)
            strLen, index = str(length), 0
            self.prgProgress['maximum'] = length
            while self.flag is True and index < length:
                self.tv.insert(
                    '', index,
                    iid=str(index),
                    text=result[index][0],
                    value=[result[index][1], result[index][2]])
                index += 1
                self.progress('Вывод строк', index, strLen)
            self.btnShow.grid(row=13, **self.grd.cl0_sp3_pdSt_stWE)
            '''Кнопка замены'''
            if checkArea == 'Колонка электронной таблицы' or '':
                self.btnReplaceInSpSh.grid(row=0, **self.grd.cl1_pdSt)
            else:
                self.btnReplaceFromDB.grid(row=0, **self.grd.cl1_pdSt)
            '''Проверка прерывания'''
            if self.flag is True:
                self.progress('Проверка завершена', index, strLen)
                self.btnCheck['text'] = 'Начать проверку'
                self.flag = False
            else:
                self.lblProgress['text'] = 'Проверка прервана.'
            collect()
        else:
            self.flag = False
            self.btnCheck['text'] = 'Начать проверку'

    def checkInSpSh(self, function, checkCount, limit, result, length, strLen, index):
        while self.flag is True and index < length:
            cellA = self.columnSpSh[index]
            for cellB in self.columnSpSh[index:length]:
                self.checkTemplate(cellA, cellB, function, checkCount, limit, result)
            index += 1
            self.progress('Сравнение строк', index, strLen)
        self.prgProgress['value'] = 0
        return(result)

    def checkInDtBs(self, function, checkCount, limit, result, length, strLen, index):
        while self.flag is True and index < length:
            cellA = self.columnSpSh[index]
            for cellB in self.columnDB:
                self.checkTemplate(cellA, cellB, function, checkCount, limit, result)
            index += 1
            self.progress('Сравнение строк', index, strLen)
        self.prgProgress['value'] = 0
        return(result)

    def checkTemplate(self, cellA, cellB, function, checkCount, limit, result):
        str1, str2 = str(cellA), str(cellB)
        if self.ignNum is True:
            str1, str2 = self.deleteNumbers(str1), self.deleteNumbers(str2)
        if str1 != str2:
            if self.ignWrd:
                str1, str2 = self.replaceWord(str1), self.replaceWord(str2)
            if self.symbStart != 0 or self.symbFinish is not None:
                str1 = str1[self.symbStart:self.symbFinish]
                str2 = str2[self.symbStart:self.symbFinish]
            count = function(str1, str2)
            var1, var2 = [count, cellA, cellB], [count, cellB, cellA]
            if (checkCount(count, limit) and
                var1 not in result and
                    var2 not in result):
                result.append(var1)

    def deleteNumbers(self, string):
        symbolList, index = list(string), 0
        while index < len(symbolList):
            if symbolList[index].isdigit():
                symbolList.pop(index)
            else:
                index += 1
        return(''.join(symbolList))

    def replaceWord(self, string):
        string = string.lower()
        for word in self.ignWrd:
            word = word.lower()
            while string.find(word) != -1:
                string = string.replace(word, '')
        return(string)

    def getCoincidenceWW(self, s1, s2):
        wordListA = self.trn.getWrdList(s1)
        wordListB = self.trn.getWrdList(s2)
        count = 0
        for word in wordListA:
            if len(word) >= 3 and word in wordListB:
                count += 1
        return(count)

    def getCoincidenceWS(self, s1, s2):
        wordList, count = self.trn.getWrdList(s1), 0
        for word in wordList:
            if len(word) >= 3 and word in s2:
                count += 1
        return(count)

    def getDistance(self, s1, s2):
        d, lenstr1, lenstr2 = {}, len(s1), len(s2)
        for i in range(-1, lenstr1 + 1):
            d[(i, -1)] = i + 1
        for j in range(-1, lenstr2 + 1):
            d[(-1, j)] = j + 1
        for i in range(lenstr1):
            for j in range(lenstr2):
                if s1[i] == s2[j]:
                    cost = 0
                else:
                    cost = 1
                d[(i, j)] = min(
                    d[(i - 1, j)] + 1,
                    d[(i, j - 1)] + 1,
                    d[(i - 1, j - 1)] + cost)
                if i and j and s1[i] == s2[j - 1] and s1[i - 1] == s2[j]:
                    d[(i, j)] = min(d[(i, j)], d[i - 2, j - 2] + cost)
        return(d[lenstr1 - 1, lenstr2 - 1])

    def replaceInSpSh(self):
        varA = self.replacerInSpSh.lblVarA['text']
        varB = self.replacerInSpSh.lblVarB['text']
        varC = self.replacerInSpSh.txtVarC.get(1.0, END)
        varC = varC.replace('\n', ' ')
        varC = varC.strip()
        for row in self.xlsData[self.sheetID][self.rowStart:self.rowFinish]:
            if row[self.checkColumn] == varA or row[self.checkColumn] == varB:
                row[self.checkColumn] = varC
        tags = self.tv.get_children()
        for tag in tags:
            values = self.tv.item(tag)['values']
            if values[0] == varA or values[0] == varB:
                self.tv.set(tag, 0, varC)
                self.tv.item(tag, text='?')
            if values[1] == varA or values[1] == varB:
                self.tv.set(tag, 1, varC)
                self.tv.item(tag, text='?')
        self.replacerInSpSh.hide()
        self.replacerInSpSh.clear()

    def replaceFromDB(self):
        slcTag = self.tv.selection()[0]
        values = self.tv.item(slcTag)['values']
        varSS = values[0]
        varDB = values[1]
        for row in self.xlsData[self.sheetID][self.rowStart:self.rowFinish]:
            if row[self.checkColumn] == varSS:
                row[self.checkColumn] = varDB
        tags = self.tv.get_children()
        for tag in tags:
            values = self.tv.item(tag)['values']
            if values[0] == varSS:
                self.tv.set(tag, 0, varDB)
                self.tv.item(tag)['text'] = '?'

    def resetOptions(self):
        self.cmbColumn.delete(0, END)
        [btn.grid_forget() for btn in [
            self.btnShow, self.btnReplaceInSpSh, self.btnReplaceFromDB]]
        self.lblProgress['text'] = ''
        self.prgProgress['value'] = 0

    def resetView(self):
        for rec in self.tv.get_children():
            self.tv.delete(rec)
        self.tv['columns'] = []
        self.tv.heading('#0', text='')
        self.tv.column('#0', stretch=True, width=self.tv.winfo_reqwidth() - 2)
        [btn.grid_forget() for btn in [
            self.btnUniteCols, self.btnDelCol, self.btnDelRow]]
