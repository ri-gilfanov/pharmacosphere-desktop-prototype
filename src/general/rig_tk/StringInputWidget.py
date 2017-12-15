from tkinter import Listbox as LB, Text as Txt, Spinbox as Sb
from tkinter.ttk import Entry as Ent, Combobox as Cb
from platform import system as this_os


class StringWidget:
    def __init__(self, *args, **kwargs):
        pass

    def press_hotkey(self, event=None):
        print(event.keycode)
        if this_os() == 'Linux':
            if event.keycode == 38:
                '''Выделить всё (ctrl+a)'''
                self.select_all()
                return('break')

        elif this_os() == 'Windows':
            if event.keycode == 65:
                '''Выделить всё (ctrl+a)'''
                self.select_all()
                return('break')

            elif event.keycode == 88:
                '''Вырезать в буфер обмена (ctrl+x)'''
                self.event_generate('<<Cut>>')
                return('break')

            elif event.keycode == 67:
                '''Копировать в буфер обмена (ctrl+c)'''
                self.event_generate('<<Copy>>')
                return('break')

            elif event.keycode == 86:
                '''Вставить из буфера обмена (ctrl+v)'''
                self.event_generate('<<Paste>>')
                return('break')

    def select_all(self):
        self.selection_range(0, 'end')


class Entry(Ent, StringWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bind('<Control-KeyPress>', self.press_hotkey)


class Spinbox(Sb, StringWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bind('<Control-KeyPress>', self.press_hotkey)

    def select_all(self):
        pass  # self.selection_range(0, 'end')


class Combobox(Cb, StringWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bind('<Control-KeyPress>', self.press_hotkey)
        self.bind('<Up>', self.open_list)

    def open_list(self, event=None):
        self.event_generate('<Down>', when='tail')


class Searchbox(Combobox):
    def __init__(self, *args, source=list(), **kwargs):
        super().__init__(*args, **kwargs)
        self.bind('<KeyRelease>', self.filter_values)
        self.source = source
        self.filter_values()

    def filter_values(self, event=None):
        s = self.get().lower()
        self['values'] = [v for v in self.source if s in v.lower() or not s]


class Text(Txt, StringWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bind('<Control-KeyPress>', self.press_hotkey)

    def select_all(self):
        self.tag_add('sel', '1.0', 'end-1c')


class Listbox(LB):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bind('<Control-KeyPress>', self.press_hotkey)

    def press_hotkey(self, event):
        if self['selectmode'] == 'extended':
            if event.keycode == 38 and this_os() == 'Linux':
                    '''Выделить всё (ctrl+a)'''
                    self.select_set(0, 'end')
                    return('break')

            elif this_os() == 'Windows':
                if event.keycode == 65:
                    '''Выделить всё (ctrl+a)'''
                    self.select_set(0, 'end')
                    return('break')

                elif event.keycode == 67:
                    '''Копировать в буфер обмена (ctrl+c)'''
                    self.event_generate('<<Copy>>')
                    return('break')
