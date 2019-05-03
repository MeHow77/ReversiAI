import math
import random
class Cell():
    wages = list()  # ints
    inputs = list()  # cell objects
    bias = 0
    a = 0
    db = 0
    dw = list()
    def sigma(self, x):
        s = 1/(math.exp(-x)+1)
        #s = (math.atan(x) + math.pi/2)/math.pi
        if (math.isnan(x)):
            s = 0
        return s
    def __init__(self):
        self.wages = list()  # ints
        self.inputs = list()  # cell objects
        self.bias = 0
        self.a = 0
        self.db = 0
        self.dw = list()
        return None

    def makeA(self):
        if(len(self.dw)<len(self.wages)): #inicjalizacja listy zmian wag
            for each in self.wages:
                self.dw.append(0)
        inputvals = list()
        for cell in self.inputs:
            inputvals.append(cell.makeA()) #getting inputs into vector
        mul = [a*b for a,b in zip(self.wages, inputvals)] #mutliply vectors elementwise
        a = sum(mul) + self.bias
        self.a = a
        if (math.isnan(a)):
            s = 0
        a = self.sigma(a)
        self.a = a
        return a

    def inputC(self, x):
        pass

    def adjustwages(self, y):
        dwL = list()
        for cell in self.inputs:
            index = self.inputs.index(cell)
            #z = self.wages[index] * cell.a + self.b #dla sieci głębokiej, z powinno być a
            dw = 2*(self.a - y)*cell.a*self.a*(1-self.a)
            #self.wages[index] -= dw
            self.dw[index] += dw
            dwL.append(dw)
        return dwL

    def adjustbias(self, y):
        db = 2*self.a*(self.a-y)
        self.db += db

    def derCostbyA(self, y):
        da = 2*self.a*(self.a - y) #will have to be multiplied by sum of wages

    def prop(self, y):
        self.adjustbias(y)
        return self.adjustwages(y)

    def changeStuff(self):
        self.bias -= self.db/len(self.wages)
        for i in range(0, len(self.wages)):
            self.wages[i] -= self.wages[i]/len(self.wages)
        self.db = 0
        self.dw = list()

        #pochodna funkcji kosztu po wadze:
        #2(różnica między wyjściem, a oczekiwanym wyjściem)*aktywacja poprzedniego neuronu[x]
        # * (waga połączenia * x + bias obecnej komórki)[z] * (1 - z)
        #daje nam pochodną kosztu po wadze
        #zmieniamy wagę tego połącznia o tę wartość

        #pochodzna kosztu po biasie:
        #2*z[jak wyżej]*(a-y)*waga obecnej komórki
