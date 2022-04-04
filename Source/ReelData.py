class ReelData:
    def __init__(self, working_mode, game_name="test_game", section_name="test_section", short_info="test_info"):
        self.working_mode = working_mode # 0 - генерация и рилов и весов; 1 - генерация только рилов; 2 - генерация только весов

        self.reelset_name = 'Test reelset'
        self.reelset_betsindices = [1, 2, 3]
        self.reelset_range = [0, 0]
        self.reelset_isfortunebet = False
        self.reelset_ismaincycle = True
        self.reelset_isstartscreen = True
        self.reelset_isfreespin = False
        self.reelset_sectionname = section_name
        self.reelset_section = -1

        self.game_name = game_name  # Это строка
        self.short_info = short_info # Можешь написать там коротенькую инфу по рилсету

        self.window_height = -1 # Это интегер
        self.number_of_reels = -1 # Это интегер

        self.special_symbols = [] # Список словарей, каждый словарь отвечает за свой рил, ключ - символ - значение [кол-во стаков - длина стака]
        self.dist_between_sp_symbols = [] # Список интегеров, где каждый интегер - расстояние между специальными символами в каждом риле (вдруг он не одинаковы)
        self.common_symbols = [] # Список словарей, каждый словарь отвечает за свой рил, ключ - символ, значение [кол-во стаков - длина стака]

        self.weight_percentage = []  # Список чисел, где каждое число - процент выпадения паттерна на этом риле
        self.loop_indexes = []  # Индексы чисел в weight_percentage которые должные быть зациклены
        self.weight_patterns = []  # Список из N списков (N - кол-во рилов), в каждом из этих списков M списков (М - высота окна борда)

        self.read_symbol_weights = []  # Для режима работы при котором создаются только веса
        # в каждом из этих списков списки паттернов
        """
        Пример weight_patterns:
        [[1], [], [], [], []] - вот у нас основной список, в нем 5 списков для 5 рилов
        [1] = [[[2], [3], [4]],[],[]] - 2,3,4 - отвечают за позицию в окне (у нас окно высотой 3 допустим)
        2 = [1,2,3] - пример паттерна, это значит что на 0 позиции в окне мы будем искать символы 1,2,3

        Пример weight_percentage:
        [[95,56], [60,10], [74,6], [89,6], [90,5]] - это значит что на нужные паттерны накинется столько массы, чтобы паттерны выпадали с такой вероятностью
        """

    def PrintMode(self):
        print(["Creating Reels and Weights",
               "Creating only Reels",
               "Creating only Weights"][self.working_mode])

    def InfoAboutSymbols(self):
        """
        Этот метод просто перепечатывает сеттинги для проверки правильности их считвания
        :return: just print
        """
        if (self.working_mode == 2):
            print("You are in weight creating mode, no information about symbols")
            return 0

        print("\nGame name:", self.game_name)
        print("Section name:", self.reelset_sectionname)
        print("Short info:", self.short_info)
        print("Board size:", self.window_height, "x", self.number_of_reels)

        print("\nSPECIAL SYMBOLS BY REELS:")
        for i, dic in enumerate(self.special_symbols):
            print("Reel ", i+1, ":", sep = "")
            print("\t Distance between special symbols:", self.dist_between_sp_symbols[i])
            for key, val in dic.items():
                print("\t", key, val)

        print("\nCOMMON SYMBOLS BY REELS:")
        for i, dct in enumerate(self.common_symbols):
            print("Reel ", i+1, ":", sep='')
            for key, val in dct.items():
                print("\t", key, val)

    def InfoAboutWeights(self):
        if (self.working_mode == 1):
            print("You are in reel creating mode, no information about weights")
            return 0
        print("\nWEIGHT INFO:")
        for i, val in enumerate(self.weight_patterns):
            print("Reel ", i + 1, ":", sep='')
            for j, pattern in enumerate(val):
                print("\t", self.weight_percentage[i][j], "%:")
                for pat in pattern:
                    print("\t\t", pat)



    def SetWindowSize(self, height, width):
        self.window_height = height
        self.number_of_reels = width

    def GetWindowHeight(self):
        return self.window_height

    def GetWindowWidth(self):
        return self.number_of_reels


    def SetSpecialSymbolsInfo(self, sp_symbols, dist_between_sp_symbols):
        self.special_symbols = sp_symbols
        self.dist_between_sp_symbols = dist_between_sp_symbols

    def GetSpecialSymbolsInfo(self, reel_ind):
        return self.special_symbols[reel_ind]

    def GetSpecialSymbolDist(self, reel_ind):
        return self.special_symbols[reel_ind]


    def SetCommonSymbolsInfo(self, common_symbols):
        self.common_symbols = common_symbols

    def GetCommonSymbols(self, reel_ind):
        return self.common_symbols[reel_ind]


    def SetNewReelInfo(self, game_name, section_name, short_info):
        self.game_name = game_name
        self.section_name = section_name
        self.short_info = short_info


    def SetWeightInfo(self, weight_patterns, loop_indexes, weight_percentage):
        self.weight_patterns = weight_patterns
        self.loop_indexes = loop_indexes
        self.weight_percentage = weight_percentage

    def GetWeightPatterns(self, reel_ind):
        return self.weight_patterns[reel_ind]

    def GetWeightPercentage(self, reel_ind):
        return self.weight_percentage[reel_ind]








