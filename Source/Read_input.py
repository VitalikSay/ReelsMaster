import re
import os
from collections import defaultdict
from Source.ReelData import ReelData


def ReadSettings(settings_file_name, inner_directory, reels_file_name, game_name):

    reels_path = "Reels"
    source_path = ".."
    if __name__ == "__main__":
        reels_path = "../Reels"
        source_path = "../Source"
    os.chdir(reels_path)
    if not os.path.isdir(game_name):
        os.mkdir(game_name)

    if inner_directory != "":
        os.chdir(game_name)
        if not os.path.isdir(inner_directory):
            os.mkdir(inner_directory)
        os.chdir("..")
    os.chdir(source_path)

    print(os.getcwd())
    raw_settings_lines = ReadSettingLines(settings_file_name, game_name, inner_directory)
    settings_lines = ReadClearInpFile(raw_settings_lines)
    working_mode = SetWorkingMode(settings_lines)
    window_height, window_width = ReadWindowSize(settings_lines[0])
    del settings_lines[0]  # Удалить строчку с размерами борда

    if working_mode[0]:
        symbol_lines = FindSymbolSettings(settings_lines, window_width)
        weight_lines = FindPatternSettings(settings_lines)
        special_symbols, dst_bet_sp_symbosl, common_symbols = ReadSymbolSettings(symbol_lines, window_width)
        weight_percentage, loop_indexes, weight_patterns = ReadWeightSettings(weight_lines, window_height, window_width)
        reel_data_obj = MakeReelDataObject(working_mode,
                                           window_height,
                                           window_width,
                                           sp_symbols=special_symbols,
                                           dist_between_sp_symbols=dst_bet_sp_symbosl,
                                           common_symbols=common_symbols,
                                           weight_percentage=weight_percentage,
                                           loop_indexes=loop_indexes,
                                           weight_patterns=weight_patterns)

    elif working_mode[1]:
        symbol_lines = FindSymbolSettings(settings_lines, window_width)
        special_symbols, dst_bet_sp_symbosl, common_symbols = ReadSymbolSettings(symbol_lines, window_width)
        reel_data_obj = MakeReelDataObject(working_mode,
                                           window_height,
                                           window_width,
                                           sp_symbols=special_symbols,
                                           dist_between_sp_symbols=dst_bet_sp_symbosl,
                                           common_symbols=common_symbols)

    elif working_mode[2]:
        reelset_settings, reels = ReadReelset(reels_file_name, game_name, inner_directory, window_width)
        weight_lines = FindPatternSettings(settings_lines)
        weight_percentage, loop_indexes, weight_patterns = ReadWeightSettings(weight_lines, window_height, window_width)
        reel_data_obj = MakeReelDataObject(working_mode,
                                           window_height,
                                           window_width,
                                           weight_percentage=weight_percentage,
                                           loop_indexes=loop_indexes,
                                           weight_patterns=weight_patterns,
                                           reelset_settings=reelset_settings,
                                           symbols_weights=reels)
    return reel_data_obj


def MakeReelDataObject(working_mode,
                       window_height,
                       window_width,
                       sp_symbols=None,
                       dist_between_sp_symbols=None,
                       common_symbols=None,
                       weight_percentage=None,
                       loop_indexes=None,
                       weight_patterns=None,
                       reelset_settings=None,
                       symbols_weights=None):

    Reel_Data = ReelData(working_mode.index(True))
    if working_mode[0]:
        Reel_Data.SetWindowSize(window_height, window_width)
        Reel_Data.SetSpecialSymbolsInfo(sp_symbols, dist_between_sp_symbols)
        Reel_Data.SetCommonSymbolsInfo(common_symbols)
        Reel_Data.SetWeightInfo(weight_patterns, loop_indexes, weight_percentage)
    elif working_mode[1]:
        Reel_Data.SetWindowSize(window_height, window_width)
        Reel_Data.SetSpecialSymbolsInfo(sp_symbols, dist_between_sp_symbols)
        Reel_Data.SetCommonSymbolsInfo(common_symbols)
    elif working_mode[2]:
        Reel_Data.SetWindowSize(window_height, window_width)
        Reel_Data.SetWeightInfo(weight_patterns, loop_indexes, weight_percentage)
        Reel_Data.read_symbol_weights = symbols_weights
        Reel_Data.reelset_name = reelset_settings[0]
        Reel_Data.reelset_betsindices = reelset_settings[1]
        Reel_Data.reelset_range = reelset_settings[2]
        Reel_Data.reelset_isfortunebet = reelset_settings[3]
        Reel_Data.reelset_ismaincycle = reelset_settings[4]
        Reel_Data.reelset_isstartscreen = reelset_settings[5]
        Reel_Data.reelset_isstartscreen = reelset_settings[6]
        Reel_Data.reelset_sectionname = reelset_settings[7]
        Reel_Data.reelset_section = reelset_settings[8]
    return Reel_Data


def FindSymbolSettings(lines, window_width):
    """
    :param lines: Отчищеные от пустых строчек сеттинги
    :return: Возвращает строчки содержащие только настройки символов
    """
    first_symb_set_index = len(lines)  # Чтобы если что ошибку выдавало
    last_symb_set_index = len(lines)

    lines_indexes_with_sp_symbol_info = []
    for i, line in enumerate(lines):
        if re.match(r'\s{0,3}\d{1,3} \d{1,3}', line):
            lines_indexes_with_sp_symbol_info.append(i)
    lines_indexes_with_sp_symbol_info = lines_indexes_with_sp_symbol_info[:window_width]

    first_symb_set_index = lines_indexes_with_sp_symbol_info[0]
    number_of_sp_symbols = int(re.findall(r'\d{1,3}', lines[lines_indexes_with_sp_symbol_info[-1]])[0])
    number_of_common_symbols = int(re.findall(r'\d{1,3}', lines[(lines_indexes_with_sp_symbol_info[-1] +
                                                                 number_of_sp_symbols + 1)])[0])
    last_symb_set_index = (lines_indexes_with_sp_symbol_info[-1] +
                           number_of_sp_symbols + 1 +
                           number_of_common_symbols + 1)
    return lines[first_symb_set_index: last_symb_set_index]


def FindPatternSettings(lines):
    """
      :param lines: Отчищеные от пустых строчек сеттинги
      :return: Возвращает строчки содержащие только настройки весов
      """

    first_pattern_set_index = len(lines)
    last_pattern_set_index = len(lines)

    lines_indexes_with_patterns = []
    for i, line in enumerate(lines):
        if re.match(r'\s{0,3}\[\[', line):
            lines_indexes_with_patterns.append(i)

    first_pattern_set_index = lines_indexes_with_patterns[0] - 1
    last_pattern_set_index = lines_indexes_with_patterns[-1] + 1

    return lines[first_pattern_set_index: last_pattern_set_index]


def ReadSettingLines(settings_file_name, game_name, inner_directory):
    settings_path = "Settings"
    source_path = "../../"
    if __name__ == "__main__":
        source_path = "../../Source"
        settings_path = "../Settings"
    os.chdir(settings_path)
    os.chdir(game_name)

    if inner_directory != "":
        os.chdir(inner_directory)
    file = open(settings_file_name + '.txt', 'r', encoding='utf-8')
    raw_lines = file.readlines()
    file.close()
    if inner_directory != "":
        os.chdir("..")

    os.chdir(source_path)
    return raw_lines


def ReadReelsetLines(reelset_file_name, game_name, inner_directory):
    reels_path = "Reels"
    source_path = "../../"
    if __name__ == "__main__":
        source_path = "../../Source"
        reels_path = "../Reels"
    os.chdir(reels_path)
    os.chdir(game_name)

    if inner_directory != "":
        os.chdir(inner_directory)
    file = open(reelset_file_name + '.txt', 'r', encoding='utf-8')
    raw_lines = file.readlines()
    file.close()
    if inner_directory != "":
        os.chdir("..")

    os.chdir(source_path)
    return raw_lines


def ReadClearInpFile(raw_lines) -> list:
    """
    Чистим сеттинги от комментариев и пустых строчек
    :param file:
    :return:
    """

    raw_lines[-1] = raw_lines[-1] + "\n"
    lines = []
    i = 0
    while (i != len(raw_lines)):
        if raw_lines[i][-1] == '\n':
            line = raw_lines[i][:-1]  # Убрали \n
        for j in range(len(line)):  # Убираем комметарий со строки
            if line[j] == "#":
                line = raw_lines[i][:j]
                break
        if line == "":  # Если осталась только пустота, то пропускаем эту строчку
            del raw_lines[i]
            continue
        i += 1
        lines.append(line)
    return lines


def ReadWindowSize(line):
    res = re.match(r'\d{1,3}\s\d{1,3}', line)  # READ WINDOW HEIGHT AND WIDTH
    if not res:
        raise AttributeError("ERROR in -> Read_input.py -> ReadWindowSize()")
    return [int(t) for t in res.group(0).split()]  # (height x width)


def SetWorkingMode(lines):
    working_mode = [False, False, False]  # 0 - генерация и рилов и весов; 1 - генерация только рилов; 2 - генерация только весов
    symbol_settings_in_file = False;
    for line in lines:
        if re.match(r'\d{1,3}\s{0,5}\[', line):
            symbol_settings_in_file = True
            break

    if symbol_settings_in_file:
        if re.match(r'.{0,5}\[\[', lines[-1]):
            working_mode[0] = True
        else:
            working_mode[1] = True
    else:
        working_mode[2] = True
    return working_mode


def ReadSpecialSymbolInfo(line):
    res = re.match(r'\d{1,3}\s\d{1,3}', line)  # Читаем инфо про специальные символы
    if (not res):
        raise AttributeError("ERROR in -> Read_input.py -> ReadSpecialSymbolInfo()")
    return [int(t) for t in res.group(0).split()] # (number_of_sp_symbols, dist_between_sp_symbols)


def ReadSpecialSymbolsStack(line):
    sp_symbol_stacks = []
    res = re.match(r'\d{1,3}', line)
    if (not res):
        raise AttributeError("ERROR in -> Read_input.py -> ReadSpecialSymbolsStack() (reading special symbol error)")
    cur_sp_symbol = int(res.group(0))

    res = re.findall(r'\[\d{1,3}\s\d{1,3}\]', line)
    if (not res):
        raise AttributeError("ERROR in -> Read_input.py -> ReadSpecialSymbolsStack() (reading special symbol stacks error)")
    for item in res:
        sp_symbol_stacks.append([int(r) for r in item[1:-1].split()])
    return cur_sp_symbol, sp_symbol_stacks  # (symbol, stacks) ex: (10, [[5 1], [2,2]])


def ReadNumberofCommonSymbols(line):
    res = re.match(r'\d{1,3}', line)
    if (not res):
        raise AttributeError("ERROR in -> Read_input.py -> ReadNumberofCommonSymbols()")
    return int(res.group(0))


def ReadCommonSymbolStack(line):
    common_symbol_stacks = []
    res = re.match(r'\d{1,3}', line)
    if (not res):
        raise AttributeError("ERROR in -> Read_input.py -> ReadCommonSymbolStack() (reading common symbols error)")
    cur_common_symbol = int(res.group(0))

    res = re.findall(r'\[\d{1,3}\s\d{1,3}\]', line)
    if (not res):
        raise AttributeError("ERROR in -> Read_input.py -> ReadCommonSymbolStack() (reading common symbols stack error)")
    for item in res:
        common_symbol_stacks.append([int(r) for r in item[1:-1].split()])
    return cur_common_symbol, common_symbol_stacks  # (symbol, stacks) ex: (5, [[5 1], [2,2], [1 3])


def ReadPatternsPercentage(line):
    pattern_weights = []
    loop_pattern_indexes = []
    res = re.findall(r'(\d{1,20})|(!\d{1,20})', line)
    if (not res):
        raise AttributeError("ERROR in -> Read_input.py -> ReadPatternsPercentage()")
    proc_res = []
    for tup in res:
        proc_res.append(tup[bool(tup[1])])
    res = proc_res

    for i, perc in enumerate(res):
        if perc[0] == '!':
            loop_pattern_indexes.append(i)
            perc = perc[1:]
        pattern_weights.append(int(perc))
    return pattern_weights, loop_pattern_indexes


def ReadWeightPatterns(lines):  # Передаем количество линий равное высоте борда
    number_of_patterns = -1
    for i, line in enumerate(lines):
        res = re.findall(r'\[[^\[^\]]{1,100}\]', line)
        if not res:
            raise AttributeError("ERROR in -> Read_input.py -> ReadWeightPatterns()")
        if number_of_patterns == -1:
            number_of_patterns = len(res)
            weight_patterns = [[] for _ in range(number_of_patterns)]
        elif len(res) != number_of_patterns:
            raise AttributeError("ERROR in -> Read_input.py -> ReadWeightPatterns() Number of patterns not the same at different lines")

        for j, row_pattern in enumerate(res):
            r = re.match(r'\d{1,3}-\d{1,3}', row_pattern[1:-1])
            if '+' in row_pattern:
                weight_patterns[j].append([-1])
            elif r:
                ranges = [int(t) for t in r.group(0).split('-')]
                weight_patterns[j].append([*range(ranges[0], ranges[1] + 1)])
            else:
                weight_patterns[j].append([int(e) for e in row_pattern[1:-1].split(',')])
    if weight_patterns:
        return weight_patterns
    else:
        raise ValueError("ERROR in -> Read_input.py -> ReadWeightPatterns() Weight patterns are not created")


def ReadSymbolSettings(symbol_lines, window_width):
    current_line_index = 0

    sp_symbols = [defaultdict(list) for _ in range(window_width)]
    common_symbols = [defaultdict(list) for _ in range(window_width)]
    dst_bet_spec_symbols = [0 for _ in range(window_width)]

    for reel_index in range(window_width):
        number_of_sp_symbols, dist_between_sp_symbols = ReadSpecialSymbolInfo(symbol_lines[current_line_index])
        dst_bet_spec_symbols[reel_index] = dist_between_sp_symbols
        current_line_index += 1
        for special_symbol_index in range(number_of_sp_symbols):
            special_symbol, sp_symbol_stacks = ReadSpecialSymbolsStack(symbol_lines[current_line_index])
            sp_symbols[reel_index][special_symbol] = sp_symbol_stacks
            current_line_index += 1

        number_of_common_symbols = ReadNumberofCommonSymbols(symbol_lines[current_line_index])
        current_line_index += 1
        for common_symbol_index in range(number_of_common_symbols):
            common_symbol, common_symbol_stacks = ReadCommonSymbolStack(symbol_lines[current_line_index])
            common_symbols[reel_index][common_symbol] = common_symbol_stacks
            current_line_index += 1
    return sp_symbols, dst_bet_spec_symbols, common_symbols


def ReadWeightSettings(weight_lines, window_height, window_width):
    current_line_index = 0
    percentage_for_all_reels = []
    loop_indexes_for_all_reels = []
    patterns_for_all_reels = []

    for reel_index in range(window_width):
        percentage_list, loop_indexes = ReadPatternsPercentage(weight_lines[current_line_index])
        percentage_for_all_reels.append(percentage_list)
        loop_indexes_for_all_reels.append(loop_indexes)
        current_line_index += 1
        patterns = ReadWeightPatterns(weight_lines[current_line_index: current_line_index + window_height])
        patterns_for_all_reels.append(patterns)
        current_line_index += window_height
    return percentage_for_all_reels, loop_indexes_for_all_reels, patterns_for_all_reels


def ClearReelsetFile(raw_lines):
    i = 0
    lines = []
    while (i != len(raw_lines)):
        line = raw_lines[i]
        i += 1
        if line[-1] == '\n':
            line = line[:-1]  # Убрали \n
        if line == "":  # Если осталась только пустота, то пропускаем эту строчку
            continue
        else:
            lines.append(line.strip())
    return lines


def CountReels(lines):
    symbol_indexes = []
    for i, line in enumerate(lines):
        if "<symbols>" in line.lower():
            symbol_indexes.append(i)
    return symbol_indexes


def ReelsetSettingsIndex(lines):
    for i, line in enumerate(lines):
        if "<reelset " in line.lower():
            return i
    return -1


def ReadReelset(reelset_file_name, game_name, inner_directory, board_width):
    raw_lines = ReadReelsetLines(reelset_file_name, game_name, inner_directory)
    lines = ClearReelsetFile(raw_lines)
    symbol_indexes = CountReels(lines)
    number_of_reels = len(symbol_indexes)
    reelset_settings_line_index = ReelsetSettingsIndex(lines)

    working_without_reelset_settings = False
    if reelset_settings_line_index == -1:
        working_without_reelset_settings = True

    if number_of_reels != board_width:
        print("\n!!!! ERROR in reading reelset from file: number of reels not equal to board width")
        return 0

    reelset_settings = ReadReelsetSettings(lines[reelset_settings_line_index], working_without_reelset_settings)

    symbols_weights = []
    for reel_index in symbol_indexes:
        symbols = ReadReelSymbols(lines[reel_index])
        weights = ReadReelWeights(lines[reel_index + 1])
        symbols_weights.append([symbols, weights])

    return reelset_settings, symbols_weights


def ReadReelsetSettings(line, working_without_reelset_settings):
    line = line.lower()
    reel_name = 'Test'
    reel_betsindices = [1, 2, 3]
    reel_range = [0, 0]
    reel_isfortunefet = False
    reel_ismaincycle = True
    reel_isstartscreen = True
    reel_isfreespin = False
    reel_sectionname = "Test section"
    reel_section = -1

    if working_without_reelset_settings:
        return reel_name, reel_betsindices, reel_range, reel_isfortunefet, reel_ismaincycle, reel_isstartscreen, reel_sectionname, reel_section

    res = re.search(r'reelname\s?=\s?"([^"]*)"', line)
    if res:
        raw_line = res.group()
        reel_name = raw_line[raw_line.index('"')+1:-1]
    res = None

    res = re.search(r'betsindices\s?=\s?"([^"]*)"', line)
    if res:
        raw_line = res.group()
        reel_betsindices = [int(num) for num in raw_line[raw_line.index('"') + 1:-1].split()]
    res = None

    res = re.search(r'range\s?=\s?"([^"]*)"', line)
    if res:
        raw_line = res.group()
        reel_range = [int(num) for num in raw_line[raw_line.index('"') + 1:-1].split()]
    res = None

    res = re.search(r'isfortunebet\s?=\s?"([^"]*)"', line)
    if res:
        raw_line = res.group()
        reel_isfortunebet = True if raw_line[raw_line.index('"') + 1:-1][0] == 't' else False
    res = None

    res = re.search(r'ismaincycle\s?=\s?"([^"]*)"', line)
    if res:
        raw_line = res.group()
        reel_ismaincycle = True if raw_line[raw_line.index('"') + 1:-1][0] == 't' else False
    res = None

    res = re.search(r'isstartscreen\s?=\s?"([^"]*)"', line)
    if res:
        raw_line = res.group()
        reel_isstartscreen = True if raw_line[raw_line.index('"') + 1:-1][0] == 't' else False
    res = None

    res = re.search(r'isfreesoin\s?=\s?"([^"]*)"', line)
    if res:
        raw_line = res.group()
        reel_isfreespin = True if raw_line[raw_line.index('"') + 1:-1][0] == 't' else False
    res = None

    res = re.search(r'isfreespin\s?=\s?"([^"]*)"', line)
    if res:
        raw_line = res.group()
        reel_isfreespin = True if raw_line[raw_line.index('"') + 1:-1][0] == 't' else False
    res = None

    res = re.search(r'sectionname\s?=\s?"([^"]*)"', line)
    if res:
        raw_line = res.group()
        reel_sectionname = raw_line[raw_line.index('"') + 1:-1]
    res = None

    res = re.search(r'section\s?=\s?"([^"]*)"', line)
    if res:
        raw_line = res.group()
        reel_section = int(raw_line[raw_line.index('"') + 1:-1])
    res = None

    return reel_name, reel_betsindices, reel_range, reel_isfortunefet, reel_ismaincycle, reel_isstartscreen, reel_isfreespin, reel_sectionname, reel_section

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
    data = ReadSettings("weight_settings", "Reelset", "PoL")
    print(data.read_symbol_weights)
