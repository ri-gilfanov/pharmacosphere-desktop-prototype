from tkinter.ttk import Style


class Theme:
    def __init__(self, tk):
        self.stl = Style()
        self.tk = tk
        self.fontFamily = 'Verdana'
        self.fontSize = 10  # От 10 до 12
        self.font = self.fontFamily, self.fontSize

    def refresh(self):
        self.stl.configure('TButton', font=(self.font))
        self.stl.configure('TCombobox', font=(self.font))
        self.stl.configure('TLabel', font=(self.font))
        self.stl.configure('TEntry', font=(self.font))
        self.stl.configure('TListbox', font=(self.font))
        self.stl.configure('TNotebook.Tab', font=(self.font))
        self.stl.configure('Treeview', font=(self.font))
        self.stl.configure('Treeview.Heading', font=(self.font))
        '''self.tk.option_add("*TCombobox*Listbox*Font", ('', 12))'''
