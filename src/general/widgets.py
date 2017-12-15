from tkinter import END, EXTENDED, Listbox
from tkinter.ttk import Button, Frame, Label, Scrollbar
from .rig_tk import Combobox


class DoubleSelector:
    def __init__(self, parent):
        self.unslc = []
        self.slc = []
        
        self.frame = Frame(parent)
        
        self.unslcLabel = Label(self.frame)
        self.slcLabel = Label(self.frame)
        
        self.unselListbox = Listbox(self.frame, selectmode=EXTENDED, width=39)
        unselListboxScroll = Scrollbar(self.frame)
        unselListboxScroll['command'] = self.unselListbox.yview
        self.unselListbox['yscrollcommand'] = unselListboxScroll.set
        
        self.selButton = Button(self.frame, text='>>')
        self.unselButton = Button(self.frame, text='<<')
        
        self.selListbox = Listbox(self.frame, selectmode=EXTENDED, width=39)
        selListboxScroll = Scrollbar(self.frame)
        selListboxScroll['command'] = self.selListbox.yview
        self.selListbox['yscrollcommand'] = selListboxScroll.set
        
        self.unslcLabel.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
        self.slcLabel.grid(row=0, column=3, columnspan=2, padx=5, pady=5)
        
        self.unselListbox.grid(row=1, rowspan=2, column=0)
        unselListboxScroll.grid(row=1, rowspan=2, column=1, sticky='ns')
        
        self.selButton.grid(row=1, column=2, padx=5, pady=5, sticky='s')
        self.unselButton.grid(row=2, column=2, padx=5, pady=5, sticky='n')
        
        self.selListbox.grid(row=1, rowspan=2, column=3)
        selListboxScroll.grid(row=1, rowspan=2, column=4, sticky='ns')
        
        self.frame.pack()


class MnfSelector(DoubleSelector):
    def __init__(self, top):
        super().__init__(top.frmExcess)
        
        self.tv = top.tv
        self.db = top.db
        
        self.unslcLabel['text'] = 'Неассоциированные'+'\n'+'изготовители'
        self.slcLabel['text'] = 'Ассоциированные'+'\n'+'изготовители'
        
        self.selButton['command'] = lambda: self.move(self.unselListbox, self.unslc, self.slc)
        self.unselListbox.bind('<Double-Button-1>', lambda _: self.move(self.unselListbox, self.unslc, self.slc))
        
        self.unselButton['command'] = lambda: self.move(self.selListbox, self.slc, self.unslc)
        self.selListbox.bind('<Double-Button-1>', lambda _: self.move(self.selListbox, self.slc, self.unslc))
    
    def add(self):
        self.slc = []
        self.unslc = []
        for mnf in self.db.data['manufacturer_list']:
            self.unslc.append(mnf)
        self.refresh()
    
    def edit(self):
        mnfCodes = []
        self.slc = []
        self.unslc = []
        
        if self.tv.selection():
            code = int(self.tv.selection()[0])
            for itm in self.db.data['item_list']:
                if itm['code'] == code:
                    mnfCodes = itm['manufacturers']
                    break
        
        for mnf in self.db.data['manufacturer_list']:
            if mnf['code'] in mnfCodes:
                self.slc.append({'code': mnf['code'], 'name': mnf['name']})
            else:
                self.unslc.append(mnf)
        
        self.refresh()
    
    def refresh(self):
        if self.slc:
            self.slc.sort(key=lambda e: e['name'].lower())
        if self.unslc:
            self.unslc.sort(key=lambda e: e['name'].lower())
        
        self.unselListbox.delete(0, END)
        self.selListbox.delete(0, END)
        
        for mnf in self.unslc:
            self.unselListbox.insert(END, mnf['name'])
        for mnf in self.slc:
            self.selListbox.insert(END, mnf['name'])
    
    def move(self, listbox, source, target):
        posits = list(listbox.curselection())
        if posits:
            for i in range(len(posits)):
                target.insert(0, source.pop(posits[i]))
                for j in range(len(posits)):
                    if posits[i] < posits[j]:
                        posits[j] -= 1
            self.refresh()
    
    def get(self):
        return([element['code'] for element in self.slc])
