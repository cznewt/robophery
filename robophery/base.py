
import logging
import platform
import time
from importlib import import_module
from robophery.utils.rpi import detect_pi_version, detect_pi_revision

class ModuleManager(object):

    SERVICE_NAME = 'robophery-default'
    READ_INTERVAL = 2000
    PUBLISH_INTERVAL = 10000

    LINUX_PLATFORM = 'linux'
    RASPBERRYPI_PLATFORM = 'raspberrypi'
    BEAGLEBONE_PLATFORM = 'beaglebone'
    MINNOWBOARD_PLATFORM = 'minnowboard'
    NODEMCU_PLATFORM = 'nodemcu'
    FT232H_PLATFORM = 'ft232h'

    _instance = None

    _interface = {}
    _module = {}

    _read_cycle = 1
    _read_iter = 1
    _read_cache = []

    def __init__(self, *args, **kwargs):
        self._name = kwargs.get('name', self.SERVICE_NAME)
        self._run_mode = 'single' # multi
        self._config = kwargs.get('config')

        # setting up logging
        self._log_level = kwargs.get('log_level', 'info')
        self._log_handlers = kwargs.get('log_handlers', ['console'])
        self._setup_log()

        self._log.info("[manager] Robophery manager is starting.")


        # setting up platform
        self._platform = kwargs.get('platform', None)
        if self._platform == None:
            self._platform = self._detect_platform()
        self._log.info("[manager] Assuming '%s' platform." % self._platform)
        self._log.info("[manager] Log level set to %s with %s handler(s)." % (self._log_level.upper(), ', '.join(self._log_handlers)))

        # setting up read intervals
        self._read_interval = kwargs.get('read_interval', self.READ_INTERVAL)
        self._publish_interval = kwargs.get('publish_interval', self.PUBLISH_INTERVAL)
        if self._publish_interval % self._read_interval != 0:
            raise ValueError("Robophery manager's publish_interval must be divisible by read_interval.")
        self._read_cycle = self._publish_interval / self._read_interval
        self._log.info("[manager] Read interval is %sms, publish interval is %sms, that gives %s operations in single publish cycle." % (self._read_interval, self._publish_interval, self._read_cycle))

        # setting up models
        self._setup_interfaces(self._config['interface'])
        self._setup_modules(self._config['module'])

        self._log.info("[manager] Robophery manager successfuly started in '%s' mode." % self._run_mode)


    def _setup_log(self):
        self._log = logging.getLogger(self._name)
        self._log.setLevel(logging.DEBUG)
        if 'console' in self._log_handlers:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.DEBUG)
            self._log.addHandler(console_handler)


    def _linux_platforms(self):
        return (
            self.RASPBERRYPI_PLATFORM,
            self.BEAGLEBONE_PLATFORM,
            self.MINNOWBOARD_PLATFORM
        )


    def _detect_platform(self):
        """
        Detect if device is running on the Raspberry Pi, Beaglebone
        Black or MinnowBoard and return the platform type.
        """

        # Detect Raspberry Pi
        pi = detect_pi_version()
        if pi is not None:
            return self.RASPBERRYPI_PLATFORM

        # Detect Beaglebone Black
        plat = platform.platform()
        if plat.lower().find('armv7l-with-debian') > -1:
            return self.BEAGLEBONE_PLATFORM
        elif plat.lower().find('armv7l-with-ubuntu') > -1:
            return self.BEAGLEBONE_PLATFORM
        elif plat.lower().find('armv7l-with-glibc2.4') > -1:
            return self.BEAGLEBONE_PLATFORM

        # Detect Minnowboard
        try:
            import mraa
            if mraa.getPlatformName()=='MinnowBoard MAX':
                return self.MINNOWBOARD_PLATFORM
        except ImportError:
            pass

        # Detect NodeMCU
        try:
            import pyb
            return self.NODEMCU_PLATFORM
        except ImportError:
            pass

        # Could not detect the platform, returning generic linux.
        return self.LINUX_PLATFORM


    def _setup_interfaces(self, interfaces={}):
        for interface_name, interface in interfaces.items():
            InterfaceClass = self._load_class(interface.get('class'))
            self._interface[interface_name] = InterfaceClass(**interface)
            self._log.info("[manager] Loaded interface '%s' with '%s' class." % (interface_name, interface.get('class')))


    def _setup_modules(self, modules={}):
        for module_name, module in modules.items():
            ModuleClass = self._load_class(module.get('class'))
            module['interface'] = self._interface[module['interface']]
            module['manager'] = self
            self._module[module_name] = ModuleClass(**module)
            self._log.info("[manager] Loaded module '%s' with '%s' class." % (module_name, module.get('class')))


    def _load_class(self, name):
        """
        Load class by path string
        """
        if isinstance(name, str):
            module = import_module(".".join(name.split(".")[:-1]))
            if module:
                return getattr(module, name.split(".")[-1], None)
            raise Exception("[manager] Cannot load class '%s'" % name)


    def _read_data(self):
        data = []
        self._log.info("[manager] Reading data %s/%s at %s." % (self._read_iter, self._read_cycle, time.time()))
        for module_name, module in self._module.items():
            data.append(module.read_data())
        self._read_cache.append(data)


    def _publish_data(self):
        self._log.info("[manager] Publishing data %s at %s." % (self._read_cache, time.time()))
        self._read_cache = []
        self._read_iter = 1
        data = []
        return data


    def _single_loop(self):
        """
        Run single global service loop
        """
        while True:
            self._read_data()
            if self._read_iter < self._read_cycle:
                self._read_iter += 1
            else:
                self._publish_data()
            time.sleep(self._read_interval / 1000)


    def run(self, modules=None):
        """
        Run robophery manager service
        """
        if self._run_mode == 'single':
            self._single_loop()
        else:

            for module in modules or self._module:
                if not module.own_loop:
                    self.loop.create_task(self.handle_module(module))
                else:
                    module.start_loop()

            try:
                self.loop.run_forever()
            except KeyboardInterrupt:
                for module in modules or self._module:
                    if module.own_loop:
                        module.stop_loop()
                self.loop.create_task(self.async_stop())
                self.loop.run_forever()
            finally:
                self.loop.close()


class Module(object):

    DEVICE_NAME = 'unknown-device'
    READ_INTERVAL = 2000
    PUBLISH_INTERVAL = 10000

    def __init__(self, *args, **kwargs):
        self._name = kwargs.get('name', self.DEVICE_NAME)
        self._manager = kwargs.get('manager', None)
        self._interface = kwargs.get('interface', None)
        self._read_interval = kwargs.get('read_interval', self.READ_INTERVAL)
        self._log = self._manager._log


    def start_service(self):

        self._cycle_iteration = 1
        self._cache = []
