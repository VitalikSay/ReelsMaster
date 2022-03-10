from Reel import Reel
from ReelData import ReelData
from Read_input import ReadReel


class Reelset():
    def __init__(self, ReelData):
        self.data = ReelData
        self.reels = []
        self.name = ''
        self.betsIndices = "3"
        self.range = []  # список из двух цифр
        self.isFortuneBet = False
        self.isMainCycle = True
        self.isStartScreen = True
        self.sectionname = ''
        self.section = 0

    def MakeReel(self, settings_path, reels_path):
        if self.data.working_mode == 0:  # 0 - генерация и рилов и весов; 1 - генерация только рилов; 2 - генерация только весов
            path = ""
            self.MakeSymbols()
            self.MakeWeights()
        if self.data.working_mode == 1:
            self.MakeSymbols()
        if self.data.working_mode == 2:
            self.ReadReelset()
            self.MakeWeights()

    def MakeSymbols(self):
        for i in range(self.data.number_of_reels):
            current_reel = Reel(i)
            current_reel.MakeReel(self.data.common_symbols[i],
                                  self.data.special_symbols[i],
                                  self.data.dist_between_sp_symbols[i],
                                  self.data.window_height)
            self.reels.append(current_reel)

    def MakeWeights(self):
        if not self.reels:
            print("ERROR: There are no reels. Firstly create or read reels, then make weights.")
            return 0
        for i, reel in enumerate(self.reels):
            reel.MakeWeights(self.data.weight_patterns[i],
                             self.data.weight_percentage[i])

    def PrintReelset(self):
        pass

    def ReadReelset(self, reelset_settings, symbols_weight_list):
        self.name = reelset_settings[0]
        self.betsIndices = reelset_settings[1]
        self.range = reelset_settings[2]
        self.isFortuneBet = reelset_settings[3]
        self.isMainCycle = reelset_settings[4]
        self.isStartScreen = reelset_settings[5]
        self.sectionname = reelset_settings[6]
        self.section = reelset_settings[7]
        for i, symbols, weights in enumerate(symbols_weight_list):
            reel = Reel(i)
            reel.SetSymbols(symbols)
            reel.SetWeights(weights)
            self.reels.append(reel)
        return self


import os

# вывести текущую директорию
print("Текущая деректория:", os.getcwd())



