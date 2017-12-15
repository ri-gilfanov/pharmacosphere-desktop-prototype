from tkinter import Toplevel
from tkinter.ttk import Button, Frame


class ModalWindow():
    def __init__(self, tab):
        self.toplevel = Toplevel(tab.tk)
        self.toplevel.transient(tab.tk)
        self.toplevel.withdraw()
        self.toplevel.grab_release()
        self.toplevel.protocol('WM_DELETE_WINDOW', self.hide)

    def show(self):
        self.centering()
        self.toplevel.deiconify()
        self.toplevel.tkraise()
        self.toplevel.grab_set()
        self.toplevel.focus_set()

    def hide(self):
        self.toplevel.grab_release()
        self.toplevel.withdraw()

    def centering(self):
        sw = self.toplevel.winfo_screenwidth()
        rw = self.toplevel.winfo_reqwidth()
        x = (sw - rw) // 2
        sw = self.toplevel.winfo_screenheight()
        rw = self.toplevel.winfo_reqheight()
        y = (sw - rw) // 2
        self.toplevel.wm_geometry('+%i+%i' % (x, y))


class Exporter(ModalWindow):
    def __init__(self, basis):
        super().__init__(basis)

        self.grd = basis.grd
        self.vld = basis.vld
        self.trn = basis.trn
        self.db = basis.db

        self.frmFields = Frame(self.toplevel)
        self.frmExcess = Frame(self.toplevel)
        self.frmEditing = Frame(self.toplevel)

        self.okButton = Button(self.frmEditing)
        self.cancelButton = Button(self.frmEditing, text='Отменить')
        self.okButton.grid(row=0, column=0, padx=5, pady=10)
        self.cancelButton.grid(row=0, column=1, padx=5, pady=10)

        self.okButton['command'] = self.apply
        self.cancelButton['command'] = self.hide

        self.frmFields.pack(fill='x')
        self.frmExcess.pack()
        self.frmEditing.pack()

    def apply(self):
        pass


class Editor(ModalWindow):
    def __init__(self, tab):
        super().__init__(tab)

        self.tab = tab
        self.basis = tab.basis
        self.grd = self.basis.grd
        self.vld = self.basis.vld
        self.trn = self.basis.trn
        self.db = tab.db
        self.tv = tab.tv

        self.frmFields = Frame(self.toplevel)
        self.frmExcess = Frame(self.toplevel)
        self.frmEditing = Frame(self.toplevel)

        self.okButton = Button(self.frmEditing)
        self.cancelButton = Button(self.frmEditing, text='Отменить')
        self.okButton.grid(row=0, column=0, padx=5, pady=10)
        self.cancelButton.grid(row=0, column=1, padx=5, pady=10)

        self.okButton['command'] = self.apply
        self.cancelButton['command'] = self.hide

        self.frmFields.pack(fill='x')
        self.frmExcess.pack()
        self.frmEditing.pack()

    def apply(self):
        pass


class Addition(Editor):
    def __init__(self, tab):
        super().__init__(tab)
        self.toplevel.title('Добавить запись')
        self.okButton['text'] = 'Добавить'

    def endAddition(self, tag):
        self.tv.see(tag)
        self.tv.selection_set(tag)
        self.hide()
        self.clear()


class Editing(Editor):
    def __init__(self, tab):
        super().__init__(tab)
        self.toplevel.title('Изменить запись')
        self.okButton['text'] = 'Изменить'
