from os.path import isfile
from pickle import load as loadPickle, dump as dumpPickle


class DataBase:
    def __init__(self):
        self.filename = 'pricelist.pmd'
        self.default = {
            'version': 0.15,
            'price_list': list(),
            'item_list': list(),
            'provider_list': list(),
            'manufacturer_list': list()}
        self.data = self.default

    def openData(self):
        if isfile(self.filename):
            with open(self.filename, 'rb') as filePickle:
                bufer = loadPickle(filePickle)
                if 'provider' in bufer:
                    self.data = bufer
                else:
                    with open(self.filename, 'wb') as filePickle:
                        dumpPickle(self.default, filePickle, protocol=4)
        else:
            with open(self.filename, 'wb') as filePickle:
                dumpPickle(self.default, filePickle, protocol=4)

    def saveData(self):
        with open(self.filename, 'wb') as filePickle:
            dumpPickle(self.data, filePickle, protocol=4)

    def getNewCode(self, index):
        code = 0
        for rec in self.data[index]:
            if code <= rec['code']:
                code = rec['code'] + 1
        return(code)

    def getName(self, index, code):
        name = ''
        for rec in self.data[index]:
            if rec['code'] == code:
                name = rec['name']
                break
        return(name)

    def getCode(self, index, name):
        code = None
        for rec in self.data[index]:
            if rec['name'] == name:
                code = rec['code']
                break
        if code is None:
            code = -1
        return(code)

    def checkName(self, index, string):
        flag = True
        string = string.lower()
        for rec in self.data[index]:
            if rec['name'].lower() == string:
                flag = False
                break
        return(flag)

    def deleteRecord(self, index, code):
        for rec in self.data[index]:
            if rec['code'] == code:
                self.data[index].remove(rec)
                break

    def clear_records_from_provider(self, prv_code):
        index = 0
        while index < len(self.data['price_list']):
            record = self.data['price_list'][index]
            if record['code'][2] == prv_code:
                self.data['price_list'].remove(record)
            else:
                index += 1
