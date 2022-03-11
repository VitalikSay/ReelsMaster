from Source.Read_input import ReadSettings, ReadReel, ReadReelsetSettings, ReadReelSymbols, ReadReelWeights
from Source.ReelData import ReelData
from Source.Reelset import Reelset
from Source.Reel import Reel


###################################### НАДО ВОТ ЭТО ЗАДАТЬ ######################################
GAME_NAME = "PoL"
SETTING_FILE_NAME = "symbol_weight_settings"             # Только имя файла в папке Settings, путь и расширение не надо
REELS_FILE_NAME = "Reelset"                       # Только имя, путь и расширение не надо
#################################################################################################



reel_data = ReadSettings("Settings"+"/"+GAME_NAME+"/"+SETTING_FILE_NAME+".txt",
                         "Reels"+"/"+GAME_NAME+"/"+REELS_FILE_NAME+".txt")
reelset = Reelset(reel_data)
reelset.MakeReelSet()
reelset.PrintReelset()