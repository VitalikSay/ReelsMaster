from Source.Read_input import ReadSettings, ReadReel, ReadReelsetSettings, ReadReelSymbols, ReadReelWeights
from Source.ReelData import ReelData
from Source.Reelset import Reelset
from Source.Reel import Reel


GAME_NAME = "PoL"
SETTING_FILE_NAME = "symbol_settings" # Только имя, путь и расширение не надо
REELS_FILE_NAME = "Reelset"

reel_data = ReadSettings("Settings"+"/"+GAME_NAME+"/"+SETTING_FILE_NAME+".txt")
reelset = Reelset(reel_data)
reelset.MakeReel()
print(reelset.reels[0].weights)