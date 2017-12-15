from re import findall


class Validator:
    def __init__(self, tk):
        vlKey = {'validate': 'key'}
        self.vldInt = vlKey.copy()
        self.vldInt['validatecommand'] = (tk.register(self.checkInt), '%P')
        self.vldDate = vlKey.copy()
        self.vldDate['validatecommand'] = (tk.register(self.checkDate), '%P')
        self.vldCell = vlKey.copy()
        self.vldCell['validatecommand'] = (tk.register(self.checkCell), '%P')
        self.vldFlt2 = vlKey.copy()
        self.vldFlt2['validatecommand'] = (tk.register(self.checkFlt2), '%P')

    def checkFlt2(self, inp):
        flag = True
        try:
            float(inp)
        except ValueError:
            if inp == '':
                pass
            else:
                flag = False
        if len(inp.split('.')) > 1 and len(inp.split('.')[1]) > 2:
            flag = False
        elif len(inp.split('.')[0]) > 9:
            flag = False
        return(flag)

    def checkInt(self, inp):
        if inp.isdigit() or inp == '':
            return(True)
        else:
            return(False)

    def checkIntWithoutZero(self, inp):
        if (inp.isdigit() and int(inp) != 0) or (inp == ''):
            return(True)
        else:
            return(False)

    def checkDate(self, inp):
        flag, numberList = True, inp.split('.')
        if len(numberList) > 3:
            flag = False
        if len(inp) > 10:
            flag = False
        for number in numberList:
            if number != '' and not number.isdigit():
                flag = False
        return(flag)

    def checkCell(self, inp):
        if (findall('[^A-z0-9]', inp) or
            findall('^\W', inp) or
                findall('_', inp)):
            return(False)
        else:
            return(True)
