class Grider:
    def __init__(self):
        self.pdSt = {'padx': 4, 'pady': 4}
        self.cl0_pdSt = dict(self.pdSt, **{'column': 0})
        self.cl0_pdSt_stW = dict(self.cl0_pdSt, **{'sticky': 'w'})
        self.cl1_pdSt = dict(self.pdSt, **{'column': 1})
        self.cl1_sp2_pdSt = dict(self.cl1_pdSt, **{'columnspan': 2})
        self.cl1_sp2_pdSt_stWE = dict(self.cl1_sp2_pdSt, **{'sticky': 'w, e'})
        self.cl0_sp3_pdSt_stWE = dict(
            self.cl1_sp2_pdSt_stWE,
            **{'column': 0, 'columnspan': 3})
