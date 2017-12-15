from re import findall


class Translater:
    def getNameSting(self, string):
        string = string.strip()
        string = string.replace('  ', '')
        return(string)

    def getBoolean(self, string):
        if string == 'Да':
            return(True)
        else:
            return(False)

    def getNatMnsOrZero(self, string):
        if string and int(string) > 0:
            return(int(string) - 1)
        else:
            return(0)

    def getNatOrNone(self, string):
        if string and int(string) > 0:
            return(int(string))
        else:
            return(None)

    def getNatOrZero(self, string):
        if string:
            return(int(string))
        else:
            return(0)

    def getFltOrZero(self, string):
        try:
            return(float(string))
        except ValueError:
            return(0)

    def getWrdList(self, string):
        string = string.replace('_', ' ')
        return(findall('\w+', string))
