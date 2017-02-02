import sys
import time
sys.path.append('/root/sdcard/git/robophery-dev/')

from robophery.i2c.bh1750 import Bh1750Module

def main():
    cfg = {'name': 'hydro-light', 'bus': 2, 'resolution_mode': 0, 'additional_delay': 0}
    
    bh1750 = Bh1750Module(cfg);
    
    while True:
        bh1750.set_resolution_mode(0)
        print "Light Level (resolution 0) : {:3.2f} lx".format(bh1750.get_data)

        bh1750.set_resolution_mode(1)
        bh1750.set_additional_delay(1)
        print "Light Level (resolution 1) : {:3.2f} lx".format(bh1750.get_data)

        bh1750.set_resolution_mode(2)
        bh1750.set_additional_delay(1)
        print "Light Level (resolution 2) : {:3.2f} lx".format(bh1750.get_data)


if __name__=="__main__":
    main()
