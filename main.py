import os
import time
from Source.Read_input import ReadSettings
from Source.Reelset import Reelset
start_time = time.time()

###################################### НАДО ВОТ ЭТО ЗАДАТЬ ######################################
GAME_NAME = "CommonFeature"
SETTING_FILE_NAME = "CM_before_elimination"             # Только имя файла в папке Settings, путь и расширение не надо
REELS_FILE_NAME = "Reelset"                       # Только имя файла в папке Reels, путь и расширение не надо
#################################################################################################



reel_data = ReadSettings(SETTING_FILE_NAME, REELS_FILE_NAME, GAME_NAME)
reelset = Reelset(reel_data)
reelset.MakeReelSet()
reelset.PrintReelset()

print("\nTime:", '{:.3f}'.format(time.time() - start_time), "seconds")