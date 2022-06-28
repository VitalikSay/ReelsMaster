from Source.Reel import Reel


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
        self.MakeSymbols()
        self.MakeWeights()


    def MakeSymbols(self):
        for i in range(self.data.number_of_reels):
            current_reel = Reel(i)
            if self.data.working_mode != 2:
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
                                 self.data.loop_indexes[i],
                                 self.data.weight_percentage[i],
                                 self.data.window_height)


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



