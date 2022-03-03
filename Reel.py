class Reel():
    def __init__(self, ind):
        self.symbols = []
        self.weights = []
        self.ln = 0
        self.index = ind

    def SetSymbols(self, symbols):
        self.symbols = symbols
        self.ln = len(self.symbols)
        self.weights = [1 for _ in range(self.ln)]

    def MakeReel(self):
        pass

    def MakeWeights(self):
        pass

    def PrintReel(self):
        pass
