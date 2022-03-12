from Source.Read_input import ReadSettings, ReadReel, ReadReelsetSettings, ReadReelSymbols, ReadReelWeights
from Source.ReelData import ReelData
from Source.Reelset import Reelset
from Source.Reel import Reel
import os

import time
start_time = time.time()

###################################### НАДО ВОТ ЭТО ЗАДАТЬ ######################################
GAME_NAME = "PoL"
SETTING_FILE_NAME = "symbol_weight_settings"             # Только имя файла в папке Settings, путь и расширение не надо
REELS_FILE_NAME = "Reelset"                       # Только имя, путь и расширение не надо
#################################################################################################

os.chdir("Reels")
if not os.path.isdir(GAME_NAME):
     os.mkdir(GAME_NAME)
os.chdir("..")



reel_data = ReadSettings("Settings"+"/"+GAME_NAME+"/"+SETTING_FILE_NAME+".txt",
                         "Reels"+"/"+GAME_NAME+"/"+REELS_FILE_NAME+".txt")
reelset = Reelset(reel_data)
reelset.MakeReelSet()
reelset.PrintReelset()

print("\nTime:", '{:.3f}'.format(time.time() - start_time), "seconds")