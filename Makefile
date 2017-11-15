CWD=$(shell pwd)

.PHONY: espsdk micropython micropython-lib

help:
	@echo "Available actions:"
	@echo "  deploy         Build and write everything to device"
	@echo "  flash          Build flash image and write it into device"
	@echo "  image-esp8266  Build flash image for ESP8266"
	@echo "  image-mcu32    Build flash image for MCU32"

deploy: build put

build:
	(ls src/lib/*.py | while read i; do \
		echo "Building $$i"; \
		mpy-cross $$i || exit 1; done)

put-lib: build
	find src/lib -name "*.mpy" -a ! -name "main.mpy" -a ! -name "boot.mpy" | while read i; do \
		echo "Uploading $$i"; \
		ampy -p /dev/ttyUSB0 put $$i || exit 1; done

put-scripts:
	ampy -p /dev/ttyUSB0 put src/boot.py
	ampy -p /dev/ttyUSB0 put src/main.py

put-config:
	[ ! -f conf/.wireless ] || ampy -p /dev/ttyUSB0 put conf/.wireless
	[ ! -f conf/webrepl_cfg.py ] || ampy -p /dev/ttyUSB0 put conf/webrepl_cfg.py
	[ ! -f conf/$(DEVICE).json ] || ampy -p /dev/ttyUSB0 put conf/$(DEVICE).json

put: put-lib put-config put-scripts

flash: micropython flash-erase flash-write

flash-erase: espsdk
	./espsdk/esptool/esptool.py --port /dev/ttyUSB0 erase_flash

flash-write: espsdk micropython
	./espsdk/esptool/esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash --flash_size=detect 0 ./micropython/esp8266/build/firmware-combined.bin

source-init:
	git submodule update --init --recursive

mpy_cross: source-init
	(cd micropython; make -C mpy-cross)

espsdk: source-init
	# XXX: this make always returns failure so pretend it's ok
	(cd espsdk; make -j4 STANDALONE=y || true)

python-lib-esp8266: source-init
	(cd micropython-lib; \
		make install PREFIX=$(CWD)/micropython/esp8266/modules MOD=umqtt.simple; \
		make install PREFIX=$(CWD)/micropython/esp8266/modules MOD=umqtt.robust; \
	)

python-esp8266: source-init espsdk mpy_cross python-lib-esp8266
	mkdir -p micropython/esp8266/modules/robophery/platform/nodemcu
	cp robophery/base.py micropython/esp8266/modules/robophery
	cp robophery/platform/nodemcu/* micropython/esp8266/modules/robophery/platform/nodemcu
	(cd micropython/esp8266; export PATH=$${PATH}:$(CWD)/espsdk/crosstool-NG/bin:$(CWD)/espsdk/xtensa-lx106-elf/bin; make -j4)

image-esp8266: python-esp8266

python-lib-mcu32: source-init
	(cd micropython-lib; \
		make install PREFIX=$(CWD)/micropython/mcu32/modules MOD=umqtt.simple; \
		make install PREFIX=$(CWD)/micropython/mcu32/modules MOD=umqtt.robust; \
	)

python-mcu32: source-init espsdk mpy_cross python-lib-mcu32
	cp src/lib/* micropython/mcu32/modules/
	(cd micropython/mcu32; export PATH=$${PATH}:$(CWD)/espsdk/crosstool-NG/bin:$(CWD)/espsdk/xtensa-lx106-elf/bin; make -j4)

image-mcu32: python-mcu32
