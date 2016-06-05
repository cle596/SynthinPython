from msvcrt import getch
from time import time
while True:
    key = ord(getch())
    time1 = time()
    if key == 32: #space
        time2 = time()
        print((time2-time1)*1000.0)
