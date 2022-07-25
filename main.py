import time
from Source.Read_input import ReadSettings
from Source.Reelset import Reelset
start_time = time.time()

###################################### НАДО ВОТ ЭТО ЗАДАТЬ ######################################
GAME_NAME = "SFS"
INNER_DIRECTORY = ""   # Имя папки внутри основной папки GAME_NAME, если таковой нет, то просто оставляй пустую строчку ""
SETTING_FILE_NAME = "SFS_settings"             # Только имя файла в папке Settings, путь и расширение не надо
REELS_FILE_NAME = "TW_reels_1"                       # Только имя файла в папке Reels, путь и расширение не надо
#################################################################################################



reel_data = ReadSettings(SETTING_FILE_NAME, INNER_DIRECTORY, REELS_FILE_NAME, GAME_NAME)
reelset = Reelset(reel_data)
reelset.MakeReelSet()
reelset.PrintReelset()

print("\nTime:", '{:.3f}'.format(time.time() - start_time), "seconds")




