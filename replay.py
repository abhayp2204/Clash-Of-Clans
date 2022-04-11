import os
import time
from pathlib import Path

Folder = Path("replays/")
File = Folder / "replay.txt"
Len = Folder / "len.txt"

F = open(File, "r")
L = open(Len, "r")

TEXT_SIZE = 5096
# while True:
#     os.system("clear")
#     text = F.read(TEXT_SIZE)
    
#     if not len(text):
#         print("Replay is over!")
#         break
    
#     print(F.read(TEXT_SIZE))
#     time.sleep(1)

lines = L.readlines()
for line in lines:
    os.system("clear")
    
    text = F.read(int(line))
    
    # if not len(text):
    #     print("Replay is over!")
    #     break
    
    print(text)
    time.sleep(0.1)