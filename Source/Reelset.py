from Source.Reel import Reel
from Source.ReelData import ReelData
from Source.Read_input import ReadReel


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

    def MakeReelSet(self):
        if self.data.working_mode == 0:  # 0 - генерация и рилов и весов; 1 - генерация только рилов; 2 - генерация только весов
            self.MakeSymbols()
            self.MakeWeights()
        elif self.data.working_mode == 1:
            self.MakeSymbols()
            self.MakeWeights()
        elif self.data.working_mode == 2:
            self.MakeSymbols(True)
            self.MakeWeights()

    def MakeSymbols(self, set_symbols=False):
        for i in range(self.data.number_of_reels):
            current_reel = Reel(i)
            if not set_symbols:
                current_reel.MakeReel(self.data.common_symbols[i],
                                      self.data.special_symbols[i],
                                      self.data.dist_between_sp_symbols[i],
                                      self.data.window_height)
            else:
                current_reel.SetSymbols(self.data.read_symbol_weights[i][0])
                current_reel.ln = len(current_reel.symbols)
            self.reels.append(current_reel)

    def MakeWeights(self):
        if not self.reels:
            print("ERROR: There are no reels. Firstly create or read reels, then make weights.")
            return 0
        for i, reel in enumerate(self.reels):
            if self.data.working_mode == 1:
                reel.SetWeights([1 for _ in range(reel.ln)])
            else:
                reel.MakeWeights(self.data.weight_patterns[i],
                                 self.data.weight_percentage[i],
                                 self.data.number_of_reels)


#"<Reelset reelName="Base" betsIndices="0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22" range="0 999" isFortuneBet="false" isMainCycle="true" isStartScreen="true" isFreeSpin="true" sectionName="Base Game" section="0">"
    def PrintReelset(self):
        reelset_settings_str = ''
        reelset_settings_str += '<Reelset '
        reelset_settings_str += 'reelName="' + self.data.reelset_name + '" '
        reelset_settings_str += 'betsIndices="' + ' '.join([str(h) for h in self.data.reelset_betsindices]) + '" '
        reelset_settings_str += 'range="' + ' '.join([str(h) for h in self.data.reelset_range]) + '" '
        reelset_settings_str += 'isFortuneBet="' + ['false', 'true'][self.data.reelset_isfortunebet] + '" '
        reelset_settings_str += 'isMainCycle="' + ['false', 'true'][self.data.reelset_ismaincycle] + '" '
        reelset_settings_str += 'isStartScreen="' + ['false', 'true'][self.data.reelset_isstartscreen] + '" '
        reelset_settings_str += 'isFreeSpin="' + ['false', 'true'][self.data.reelset_isfreespin] + '" '
        reelset_settings_str += 'sectionName="' + str(self.data.reelset_sectionname) + '" '
        reelset_settings_str += 'section="' + str(self.data.reelset_section) + '"'
        reelset_settings_str += '>'

        print('\n\n')
        print(reelset_settings_str)
        for i in range(self.data.number_of_reels):
            print('\t<Reel>')
            self.reels[i].PrintReel("\t\t")
            print('\t</Reel>')
        print("</Reelset>")


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



