import os
import time
import numpy as np
from Source.Read_input import ReadSettings
from Source.Reelset import Reelset
start_time = time.time()

###################################### НАДО ВОТ ЭТО ЗАДАТЬ ######################################
GAME_NAME = "CommonFeature"
INNER_DIRECTORY = "NewNewCMReels"   # Имя папки внутри основной папки GAME_NAME, если таковой нет, то просто оставляй пустую строчку ""
SETTING_FILE_NAME = "CF_3scat_5"             # Только имя файла в папке Settings, путь и расширение не надо
REELS_FILE_NAME = "CF_trigger_reelset"                       # Только имя файла в папке Reels, путь и расширение не надо
#################################################################################################



reel_data = ReadSettings(SETTING_FILE_NAME, INNER_DIRECTORY, REELS_FILE_NAME, GAME_NAME)
reelset = Reelset(reel_data)
reelset.MakeReelSet()

symbls = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
weight = [2,  2,  3,  8,  13,  15,  18,  15,  10,  8,  6,  4,  2]
symb_lst = []
for i in range(len(symbls)):
    for c in range(weight[i]):
        symb_lst.append(symbls[i])

symb_positions_by_reels = []
for reel in reelset.reels:
    symb_pos = []
    for i in range(len(reel.symbols)):
        if (reel.symbols[i] == 11) and (reel.symbols[i-1] == 11 or reel.symbols[(i+1) % len(reel.symbols)] == 11):
            symb_pos.append(i)
            rand_symb = np.random.choice(symb_lst)
            reel.symbols[i] = rand_symb
    symb_positions_by_reels.append(symb_pos)

for i in range(len(reelset.reels)):
    if len(symb_positions_by_reels[i]) == 0:
        continue
    reel = reelset.reels[i]
    for symbl in symbls:
        if symbl not in reel.symbols:
            rand_index = np.random.choice(symb_positions_by_reels[i])
            while reel.symbols.count(reel.symbols[rand_index]) <= 1:
                rand_index = np.random.choice(symb_positions_by_reels[i])
            reel.symbols[rand_index] = symbl
            del symb_positions_by_reels[i][symb_positions_by_reels[i].index(rand_index)]


reelset.PrintReelset()

print("\nTime:", '{:.3f}'.format(time.time() - start_time), "seconds")




