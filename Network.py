from Cell import *
from InputCell import *
import random
from time import time
import pickle
class Network():
    warstwy = list() #list of lists of cell objects

    def __init__(self, liczbaKomorek):
        liczbaWarstw = len(liczbaKomorek)
        #warstwa wejściowa
        tmp = list()
        for j in range(0, liczbaKomorek[0]):
            newcell1 = InputCell()
            tmp.append(newcell1)
        self.warstwy.insert(0, tmp)
        for i in range(1, liczbaWarstw):
            tmp = list()
            for j in range(0, liczbaKomorek[i]):
                newcell = Cell()
                for x in range(0, liczbaKomorek[i-1]):
                    newcell.wages.append(random.randint(-1, 1))
                newcell.inputs = self.warstwy[i - 1]  # copy ref
                tmp.append(newcell)
            self.warstwy.insert(i, tmp)
        return None

    def input(self, inputList):
        for cell in self.warstwy[0]:
            cell.inputC(1)
        return None

    def output(self):
        tmp = list()
        last = len(self.warstwy) - 1
        for var in self.warstwy[last]:
            tmp.append(var.makeA())
        return tmp

    def backprop(self, yL):
        dwL=list(yL)
        iloscWarstw = len(self.warstwy) - 1
        for i in range(0, iloscWarstw):
            dwLL=list()
            ind = iloscWarstw - i
            length = len(self.warstwy[ind])
            for cell in self.warstwy[ind]:
                index = self.warstwy[ind].index(cell)
                dwLL.append(cell.prop(dwL[index]))
            dwL=list()
            for j in range(0, len(self.warstwy[ind-1])):
                sumofwages = 0
                for x in range(0, len(dwLL)):
                   sumofwages += dwLL[x][j]
                dwL.append(1 - (sumofwages ) * self.warstwy[ind - 1][j].a)
                                                #/ len(dwLL)
    def changeStuff(self):
        for war in self.warstwy:
            for cell in war:
                cell.changeStuff()
            #policzyć listy dw dla każdego neuronu w warstiwe i
            #dodać poelementowo listy dw
            #wproadzić modyfikacje w warstwie i-1
            #cofnąć się

    def teach(self):
        N = 100
        i = 0
        loss = 1
        try:
            file_pi2 = open('nn.obj', 'rb')
            # network = pickle.load(file_pi2)
        except:
            pass
        inputs = list()
        exps = list()
        for i in range(0, N):
            x = random.uniform(0.0, 1.0)
            y = random.uniform(0.0, 1.0)
            z = random.uniform(0.0, 1.0)
            input = [x]
            inputs.append(input)
            expect = [1 - x]
            exps.append(expect)

        start = time()
        while (loss > 0.00015):
            loss = 0
            for i in range(0, N):
                self.input(inputs[i])
                out = self.output()
                loss += sum([pow((a - b), 2) for a, b in zip(out, exps[i])]) / N
                self.backprop(exps[i])
            # i += 1
            # if (i == 20):
            self.changeStuff()
            print(loss)  # , out, "->", exps[i])
            # loss = 0
            #    i = 0
        end = time()
        print(end - start)

        file_nn = open('nn2.obj', 'wb')
        pickle.dump(self, file_nn)