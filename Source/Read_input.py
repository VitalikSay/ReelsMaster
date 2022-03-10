import re
from collections import defaultdict
from Source.ReelData import ReelData


def ReadSettings(settings_path):

    inp_file = open(settings_path, 'r')
    row_lines = inp_file.readlines()
    row_lines[-1] = row_lines[-1] + "\n"
    lines = []
    window_height = -1
    number_of_reels = -1
    number_of_sp_symbols = []
    number_of_common_symbols = []
    dist_between_sp_symbols = []
    sp_symbol = -1
    number_of_sp_symbols = -1
    dist_between_reel_info = 0
    weight_percentage = []




    ############# ЧИСТИМ ВХОДНОЙ ФАЙЛИК ОТ КОММЕНТАРИЕВ И ПУСТЫХ СТРОЧЕК #####################
    i = 0
    while(i != len(row_lines)):
        if row_lines[i][-1] == '\n':
            line = row_lines[i][:-1]  # Убрали \n
        for j in range(len(line)):  # Убираем комметарий со строки
            if line[j] == "#":
                line = row_lines[i][:j]
                break
        if line == "":  # Если осталась только пустота, то пропускаем эту строчку
            del row_lines[i]
            continue
        i += 1
        lines.append(line)
    ############################################################################################

    ############### ЧИТАЕМ РАЗМЕР ПОЛЯ ########################################
    res = re.match(r'\d{1,3}\s\d{1,3}', lines[0])  # READ WINDOW HEIGHT AND WIDTH
    if (not res):
        print("ERROR in reading window height and width")
        return 0
    window_height, number_of_reels = [int(t) for t in res.group(0).split()]
    ############################################################################

    weight_percentage = [[] for _ in range(number_of_reels)]
    weight_patterns = [[] for _ in range(number_of_reels)]
    line_ind = 1

    working_mode = [False, False, False]  # 0 - генерация и рилов и весов; 1 - генерация только рилов; 2 - генерация только весов
    if re.match(r'.{0,5}\[\[', lines[2]):
        working_mode[2] = True

    if (not working_mode[2]):

        ############## ИНИЦИИРУЕМ ВСЕ НЕОХОДИМЫЕ ДАННЫЕ (ТИПО КОНСТРУКТОР ПО УМОЛЧАНИЮ) ###############
        number_of_sp_symbols = [-1 for _ in range(number_of_reels)]
        dist_between_sp_symbols = [-1 for _ in range(number_of_reels)]
        sp_symbols = [defaultdict(list) for _ in range(number_of_reels)]
        number_of_common_symbols = [-1 for _ in range(number_of_reels)]
        common_symbols = [defaultdict(list) for _ in range(number_of_reels)]
        ##############################################################################################



        ################## ЧИТАЕМ ИНФО ПРО СПЕЦИАЛЬНЫЙ СИМВОЛ (СКОЛЬКО ИХ И КАКОЕ РАССТОЯНИЕ МЕЖДУ НИМИ) #############
        for j in range(number_of_reels):
            res = re.match(r'\d{1,3}\s\d{1,3}', lines[line_ind])  # Читаем инфо про специальные символы
            if (not res):
                print("ERROR in reading special symbol info in reel ", j)
                return 0
            number_of_sp_symbols[j], dist_between_sp_symbols[j] = [int(t) for t in res.group(0).split()]
            line_ind += 1
        #############################################################################################################



        ############## ЧИТАЕМ ИНДЕКС СПЕЦИАЛЬНОГО СИМВОЛА ################################################
            for t in range(number_of_sp_symbols[j]):  # Читаем сам специальный символ и его стаки
                res = re.match(r'\d{1,3}', lines[line_ind])
                if (not res):
                    print("ERROR in reading special symbol in reel ", j)
                    return 0
                cur_sp_symbol = int(res.group(0))
                sp_symbols[j][cur_sp_symbol] = []
        ###########################################################################################################



        ################### ЧИТАЕМ ИНФО ПО СТАКАМ СПЕЦИАЛЛЬНОГО СИМВОЛА ###########################################
                res = re.findall(r'\[\d{1,3}\s\d{1,3}\]', lines[line_ind])
                if (not res):
                    print("ERROR in reading special symbol stacks in reel ", j)
                    return 0
                for item in res:
                    sp_symbols[j][cur_sp_symbol].append([int(r) for r in item[1:-1].split()])
                line_ind += 1
        ###########################################################################################################



        ###################### ЧИТАЕМ КОЛИЧЕСВО ОБЫЧНЫХ СИМВОЛОВ ##############################
                res = re.match(r'\d{1,3}', lines[3 + dist_between_reel_info * j])
                if (not res):
                    print("ERROR in reading number of common symbols in reel ", j)
                    return 0
                number_of_common_symbols[j] = int(res.group(0))
                line_ind += 1
        ######################################################################################



        ########################## ЧИТАЕМ ИНДЕКС ОБЫЧНОГО СИМВОЛА #################################################
            for u in range(number_of_common_symbols[j]):
                res = re.match(r'\d{1,3}', lines[line_ind])
                if (not res):
                    print("ERROR in reading common symbol in reel ", j, " in index ", u)
                    return 0
                cur_common_symbol = int(res.group(0))
                common_symbols[j][cur_common_symbol] = []
        ###########################################################################################################



        ############################## ЧИТАЕМ СТАКИ ОБЫЧНОГО СИМВОЛА #############################################
                res = re.findall(r'\[\d{1,3}\s\d{1,3}\]', lines[line_ind])
                if (not res):
                    print("ERROR in reading special symbol stacks in reel ", j)
                    return 0
                for item in res:
                    common_symbols[j][cur_common_symbol].append([int(r) for r in item[1:-1].split()])
                line_ind += 1
        ##########################################################################################################


        if (line_ind + 2) < len(lines):
            working_mode[0] = True
        else:
            working_mode[1] = True

    if working_mode[2] or working_mode[0]:
        loop_pattern_indexes = [[] for _ in range(number_of_reels)]
        ################### ЧИТАЕМ ПРОЦЕНТ ВЫПАДЕНИЯ ПАТТЕРНА ###################################################
        pat_cre = False
        for j in range(number_of_reels):
            res = re.findall(r'(\d{1,3})|(!\d{1,3})', lines[line_ind])
            if (not res):
                print("ERROR in reading weight percentage for reel ", j)
                return 0

            proc_res = []
            for tup in res:
                proc_res.append(tup[bool(tup[1])])
            res = proc_res

            for i, perc in enumerate(res):
                if perc[0] == '!':
                    loop_pattern_indexes[j].append(i)
                    for _ in range(window_height):
                        weight_percentage[j].append(int(perc[1:])/window_height)
                else:
                    weight_percentage[j].append(int(perc))
            res = None
            line_ind += 1
        ########################################################################################################



        #################### ЧИТАЕМ ПАТТЕРНЫ ВЕСОВ ############################################################
            for u in range(window_height):
                res = re.findall(r'\[[^\[^\]]{1,100}\]', lines[line_ind])
                if not res:
                    print("ERROR in reading patterns for reel ", j, " in position ", u)
                    return 0
                if not pat_cre:
                    weight_patterns[j] = ([[] for _ in range(len(res))])
                    pat_cre = True
                for p, item in enumerate(res):
                    r = re.match(r'\d{1,3}-\d{1,3}', item[1:-1])
                    if '+' in item:
                        weight_patterns[j][p].append([-1])

                    elif r:
                        ranges = [int(t) for t in r.group(0).split('-')]
                        weight_patterns[j][p].append([*range(ranges[0], ranges[1] + 1)])

                    else:
                        weight_patterns[j][p].append([int(e) for e in item[1:-1].split(',')])

                res = None
                line_ind += 1
            pat_cre = False
        ####################################################################################################



        ####################### ДОБАВЛЯЕМ ЗАЦИКЛИВАНИЕ #####################################################
        for reel_ind, item in enumerate(loop_pattern_indexes):
            step = 0
            if not item:
                continue
            for ind in item:
                looping_pattern = weight_patterns[reel_ind][ind + step].copy()
                for _ in range(window_height - 1):
                    looping_pattern = [looping_pattern[-1]] + looping_pattern[:-1]
                    weight_patterns[reel_ind].insert(ind + step, looping_pattern)
                step += (window_height - 1)
        ####################################################################################################

    Reel_Data = ReelData(working_mode.index(True))
    if working_mode[0]:
        Reel_Data.SetWindowSize(window_height, number_of_reels)
        Reel_Data.SetSpecialSymbolsInfo(sp_symbols, dist_between_sp_symbols)
        Reel_Data.SetCommonSymbolsInfo(common_symbols)
        Reel_Data.SetWeightInfo(weight_patterns, weight_percentage)
    elif working_mode[1]:
        Reel_Data.SetWindowSize(window_height, number_of_reels)
        Reel_Data.SetSpecialSymbolsInfo(sp_symbols, dist_between_sp_symbols)
        Reel_Data.SetCommonSymbolsInfo(common_symbols)
    elif working_mode[2]:
        Reel_Data.SetWeightInfo(weight_patterns, weight_percentage)

    return Reel_Data


def ReadReel(reelset_path: str, board_width: int):
    inp_file = open(reelset_path, 'r')
    row_lines = inp_file.readlines()
    row_lines[-1] = row_lines[-1] + "\n"
    lines = []
    number_of_reels = 0
    number_of_reelsets = 0
    reelset_settings_index = []

    ############# ЧИСТИМ ВХОДНОЙ ФАЙЛИК ОТ КОММЕНТАРИЕВ И ПУСТЫХ СТРОЧЕК #####################
    i = 0
    while (i != len(row_lines)):
        if row_lines[i][-1] == '\n':
            line = row_lines[i][:-1]  # Убрали \n
        for j in range(len(line)):  # Убираем комметарий со строки
            if line[j] == "#":
                line = row_lines[i][:j]
                break
        if line == "":  # Если осталась только пустота, то пропускаем эту строчку
            del row_lines[i]
            continue
        if "<reelset " in line.lower():
            number_of_reelsets += 1
            reelset_settings_index.append(i)
        if "<reel>" in line.lower():
            number_of_reels += 1
        i += 1
        lines.append(line)

    ##########################################################################################

    if (number_of_reels / number_of_reelsets) != board_width:
        print(number_of_reels / number_of_reelsets)
        print("ERROR: Wrong reels. The number of reels is not equal to the width of the board in the settings")
        return 0

    reelset_settings = []
    for j in reelset_settings_index:
        reelset_settings_line = lines[j]
        reelset_settings.append(ReadReelsetSettings(reelset_settings_line))

    symbols_weights_by_reelsets = [] # [[[[symbols], [weights]], [], [], [], []], [], [], []]
    for reelset_index in reelset_settings_index:
        current_index = reelset_index
        reels = []
        for reel_index in range(board_width):
            current_index += 2 # Пропускаем <Reel>
            symbols = ReadReelSymbols(lines[current_index])
            current_index += 1
            weights = ReadReelWeights(lines[current_index])
            current_index += 1
            reels.append([symbols, weights])
        symbols_weights_by_reelsets.append(reels)
    print(symbols_weights_by_reelsets)






def ReadReelsetSettings(line):
    line = line.lower()
    reel_name = ''
    reel_betsindices = []
    reel_range = [0, 0]
    reel_isfortunefet = False
    reel_ismaincycle = True
    reel_isstartscreen = True
    reel_sectionname = ""
    reel_section = -1

    res = re.search(r'reelname\s?=\s?"([^"]*)"', line)
    if res:
        raw_line = res.group()
        reel_name = raw_line[raw_line.index('"')+1:-1]
        print(reel_name)
    res = None

    res = re.search(r'betsindices\s?=\s?"([^"]*)"', line)
    if res:
        raw_line = res.group()
        reel_betsindices = [int(num) for num in raw_line[raw_line.index('"') + 1:-1].split()]
        print(reel_betsindices)
    res = None

    res = re.search(r'range\s?=\s?"([^"]*)"', line)
    if res:
        raw_line = res.group()
        reel_range = [int(num) for num in raw_line[raw_line.index('"') + 1:-1].split()]
        print(reel_range)
    res = None

    res = re.search(r'isfortunebet\s?=\s?"([^"]*)"', line)
    if res:
        raw_line = res.group()
        reel_isfortunebet = True if raw_line[raw_line.index('"') + 1:-1][0] == 't' else False
        print(reel_isfortunebet)
    res = None

    res = re.search(r'ismaincycle\s?=\s?"([^"]*)"', line)
    if res:
        raw_line = res.group()
        reel_ismaincycle = True if raw_line[raw_line.index('"') + 1:-1][0] == 't' else False
        print(reel_ismaincycle)
    res = None

    res = re.search(r'isstartscreen\s?=\s?"([^"]*)"', line)
    if res:
        raw_line = res.group()
        reel_isstartscreen = True if raw_line[raw_line.index('"') + 1:-1][0] == 't' else False
        print(reel_isstartscreen)
    res = None

    res = re.search(r'isfreespin\s?=\s?"([^"]*)"', line)
    if res:
        raw_line = res.group()
        reel_isfreespin = True if raw_line[raw_line.index('"') + 1:-1][0] == 't' else False
        print(reel_isfreespin)
    res = None

    res = re.search(r'sectionname\s?=\s?"([^"]*)"', line)
    if res:
        raw_line = res.group()
        reel_sectionname = raw_line[raw_line.index('"') + 1:-1]
        print(reel_sectionname)
    res = None

    res = re.search(r'section\s?=\s?"([^"]*)"', line)
    if res:
        raw_line = res.group()
        reel_section = int(raw_line[raw_line.index('"') + 1:-1])
        print(reel_section)
    res = None

    return reel_name, reel_betsindices, reel_range, reel_isfortunefet, reel_ismaincycle, reel_isstartscreen, reel_sectionname, reel_section

def ReadReelSymbols(line):
    line = line.lower()
    symbols = []
    res = re.search(r'<symbols>.{1,2000}</symbols>', line)
    if res:
        symbols = [int(num) for num in res.group()[9:-10].split(',')]
    return symbols

def ReadReelWeights(line):
    line = line.lower()
    weights = []
    res = re.search(r'<weights>.{1,2000}</weights>', line)
    if res:
        weights = [int(num) for num in res.group()[9:-10].split(',')]
    return weights


if __name__ == "__main__":
    ReadReel("../Reels/PoL/Reelset.txt", 5)

