from general.rig_tk import Searchbox
from tkinter import END
from tkinter.ttk import Label
from general.topTemplates import Exporter
from tkinter.filedialog import asksaveasfilename
from pickle import dump as dumpPickle


class PriceMasterExporter(Exporter):
    def __init__(self, main):
        super().__init__(main)
        self.toplevel.title('Создать шаблон базы данных прайс-мастера')
        self.db = main.db
        lblProvider = Label(self.frmFields, text='Выберите поставщика')
        self.cmbProvider = Searchbox(
            master=self.frmFields,
            postcommand=self.update_provider_list,
            source = [d['name'] for d in self.db.data['provider_list']],
            width=32)
        self.lblHint = Label(self.frmFields)
        lblProvider.grid(row=0, **self.grd.cl1_pdSt)
        self.cmbProvider.grid(row=1, **self.grd.cl1_pdSt)
        self.lblHint.grid(row=2, **self.grd.cl1_pdSt)
        self.okButton['text'] = 'Сохранить как'
        self.okButton['command'] = self.saveFile
        hintA = 'Поле поставщик — раскрывающийся список с вариантами выбора и встроенным поиском.'
        hintB = 'Клавиши ↑, ↓ — раскрыть список и перемещаться по вариантам, Esc — скрыть, Enter — выбрать.'
        hintC = 'Чтобы вернуть все варианты — очистите соответствующее поле ввода.'
        self.lblHint['text'] = '\n%s\n\n%s\n\n%s' % (hintA, hintB, hintC)
        self.toplevel.bind('<Configure>', self.hint_resize)
    
    def hint_resize(self, event):
        self.lblHint['wraplength'] = self.toplevel.winfo_reqwidth() - 8

    def update_provider_list(self, event=None):
        values = [d['name'] for d in self.db.data['provider_list']]
        self.cmbProvider.source = values
        self.cmbProvider.filter_values()

    def clear(self):
        self.cmbProvider.set('')
        self.cmbProvider.delete(0, END)

    def fillAndShow(self):
        self.clear()
        self.show()

    def saveFile(self):

        data = self.db.data.copy()
        data['provider'] = None
        data['price_list'] = []
        del(data['provider_list'])
        prvName = self.trn.getNameSting(self.cmbProvider.get())

        path = asksaveasfilename(
            defaultextension='.pmt',
            initialfile=prvName+'.pmt',
            filetypes=[('Шаблон базы данных прайс-мастера', '.pmt')],
            parent=self.toplevel)
        
        if prvName and path:
            for record in self.db.data['provider_list']:
                if prvName == record['name']:
                    data['provider'] = record
                    break
            with open(path, 'wb') as filePickle:
                dumpPickle(data, filePickle, protocol=4)
        self.hide()
            
