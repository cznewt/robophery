import sys
import time
sys.path.append('/root/sdcard/git/robophery-dev/')

from robophery.i2c.bh1750 import Bh1750Module

def main():
    cfg = {'name': 'hydro-light', 'bus': 2}
    
    bh = Bh1750Module(cfg);
    
    while True:
        bh.get_data()
        time.sleep(1)

if __name__=="__main__":
    main()
