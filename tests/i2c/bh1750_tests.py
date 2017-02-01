from robophery.i2c import Bh1750Module

def main():
    cfg = {'name': 'hydro-light', 'bus': 2}

    Bh1750Module sensor(cfg);

    while True:
        print('while loop')
        time.sleep(1)


if __name__=="__main__":
    main()
