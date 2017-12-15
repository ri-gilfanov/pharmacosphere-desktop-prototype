from tkinter import Menu, Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.ttk import Notebook

from os.path import isfile
from pickle import load as loadPickle, dump as dumpPickle

from pricemastermod.tabs.tabPrice import PriceTab
from pricemastermod.tabs.tabXlsDebug import DebugXlsTab
from pricemastermod.tabs.tabXlsImport import ImportXlsTab

from pricemastermod.data import DataBase
from general.styles import Theme
from general.validator import Validator
from general.grider import Grider
from general.translater import Translater


class Basis:
    def __init__(self):
        self.tk = Tk()
        self.tk.minsize(1000, 600)
        self.tk.title('Прайс-мастер (версия 0.15)')

        self.db = DataBase()
        self.db.openData()
        self.theme = Theme(self.tk)
        self.theme.refresh()
        self.vld = Validator(self.tk)
        self.grd = Grider()
        self.trn = Translater()
        
        self.main_menu = Menu(self.tk)
        self.tk.config(menu=self.main_menu)
        self.pl_menu = Menu(self.main_menu, tearoff=0)
        self.main_menu.add_cascade(
            label="Импорт/экспорт .pickle-файлов",
            menu=self.pl_menu)
        self.pl_menu.add_command(
            command=self.import_pm_template,
            label="Обновить шаблон базы данных")
        self.pl_menu.add_command(
            command=self.export_pm_data,
            label="Экспорт прайс-листа")

        nb = Notebook(self.tk)

        self.prcTab = PriceTab(self)
        self.debugXlsTab = DebugXlsTab(self)
        self.importXlsTab = ImportXlsTab(self)
        self.prcTab.reset()

        nb.add(self.prcTab.frmTab, text='Прайс-лист')
        nb.add(self.debugXlsTab.frmTab, text='Отладка .xls-файлов')
        nb.add(self.importXlsTab.frmTab, text='Импорт .xls-файлов')
        nb.pack(expand=True, fill='both')

        self.tk.mainloop()

    def import_pm_template(self):
        self.path = askopenfilename(
            filetypes=[('Шаблон базы данных прайс-мастера', '.pmt')])
        if isfile(self.path):
            with open(self.path, 'rb') as filePickle:
                bufer = loadPickle(filePickle)
                if 'provider' in bufer:
                    self.db.data.update(bufer)
                    # Переделать с учётом удаления именований и изготовителей
                    self.prcTab.reset()

    def export_pm_data(self):
        self.path = asksaveasfilename(
            filetypes=[('Шаблон базы данных прайс-мастера', '.pmd')])
        if self.path:
            with open(self.path, 'wb') as filePickle:
                dumpPickle(self.db.data, filePickle, protocol=4)


if __name__ == "__main__":
    Basis()
