from tkinter import Menu, Tk
from tkinter.filedialog import askopenfilename
from tkinter.ttk import Notebook

from os.path import isfile
from pickle import load as loadPickle

from editormod.tabs.tabPrice import PriceTab
from editormod.tabs.tabItem import ItemTab
from editormod.tabs.tabProvider import ProviderTab
from editormod.tabs.tabManufacturer import ManufacturerTab
from editormod.tabs.tabXlsDebug import DebugXlsTab
from editormod.tabs.tabXlsImport import ImportXlsTab
from editormod.tops.topMain import PriceMasterExporter

from editormod.data import DataBase
from general.styles import Theme
from general.validator import Validator
from general.grider import Grider
from general.translater import Translater


class Basis:
    def __init__(self):
        self.tk = Tk()
        self.tk.minsize(1000, 600)
        self.tk.title('Редактор (версия 0.15)')

        self.db = DataBase()
        self.db.openData()
        self.theme = Theme(self.tk)
        self.theme.refresh()
        self.vld = Validator(self.tk)
        self.grd = Grider()
        self.trn = Translater()
        
        self.pmExporter = PriceMasterExporter(self)
        
        self.main_menu = Menu(self.tk)
        self.tk.config(menu=self.main_menu)
        self.pm_menu = Menu(self.main_menu, tearoff=0)
        self.main_menu.add_cascade(
            label="Импорт/экспорт .pickle-файлов",
            menu=self.pm_menu)
        self.pm_menu.add_command(
            command=self.import_pm_data,
            label="Импорт прайс-листа .pickle")
        self.pm_menu.add_command(
            command=self.pmExporter.fillAndShow,
            label="Создать шаблон базы данных прайс-мастера")

        nb = Notebook(self.tk)

        self.prcTab = PriceTab(self)
        self.itmTab = ItemTab(self)
        self.prvTab = ProviderTab(self)
        self.mnfTab = ManufacturerTab(self)
        self.debugXlsTab = DebugXlsTab(self)
        self.importXlsTab = ImportXlsTab(self)
        self.prcTab.reset()

        nb.add(self.prcTab.frmTab, text='Общий прайс-лист')
        nb.add(self.itmTab.frmTab, text='Наименования')
        nb.add(self.prvTab.frmTab, text='Поставщики')
        nb.add(self.mnfTab.frmTab, text='Изготовители')
        nb.add(self.debugXlsTab.frmTab, text='Отладка .xls-файлов')
        nb.add(self.importXlsTab.frmTab, text='Импорт .xls-файлов')
        nb.pack(expand=True, fill='both')

        self.tk.mainloop()

    def import_pm_data(self):
        self.path = askopenfilename(
            filetypes=[('Шаблон базы данных прайс-мастера', '.pmd')])
        if self.path and isfile(self.path):
            with open(self.path, 'rb') as filePickle:
                pm_data = loadPickle(filePickle)
                if 'provider' in pm_data:
                    [self.db.data['price_list'].append(r) for r in pm_data['price_list']]
                    for r in self.db.data['provider_list']:
                        if r['code'] == pm_data['provider']['code']:
                            r = pm_data['provider']
                    # Добавить импорт обновлённых сведений о поставщике
                    self.prcTab.reset()


if __name__ == "__main__":
    Basis()
