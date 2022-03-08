from Reel import Reel
from Reelset_info import ReelData

class Reelset():
    def __init__(self, ReelData):
        self.data = ReelData
        self.reels = []
        self.name = ''
        self.betsIndices = "3"
        self.range = 0  # наверно будет в процентах
        self.isFortuneBet = False
        self.isMainCycle = True
        self.isStartScreen = True
        self.sectionname = ''
        self.section = 0

    def MakeReels(self):
        for i in range(self.data.number_of_reels):
            current_reel = Reel()
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

    def ReadReels(self):
        pass

