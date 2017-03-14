
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

    _comm = {}
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

        # setting up base classes
        self._setup_communication(self._config['comm'])
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


    def _setup_communication(self, comms={}):
        for comm_name, comm in comms.items():
            CommClass = self._load_class(comm.get('class'))
            comm['manager'] = self
            self._comm[comm_name] = CommClass(**comm)
            self._log.info("[manager] Loaded communication channel '%s' with '%s' class." % (comm_name, comm.get('class')))


    def _setup_interfaces(self, interfaces={}):
        for interface_name, interface in interfaces.items():
            InterfaceClass = self._load_class(interface.get('class'))
            if 'uses' in interface:
                interface['uses']['interface'] = self._interface[interface['uses']['interface']]
            interface['manager'] = self
            self._interface[interface_name] = InterfaceClass(**interface)
            self._log.info("[manager] Loaded platform interface '%s' with '%s' class." % (interface_name, interface.get('class')))


    def _setup_modules(self, modules={}):
        for module_name, module in modules.items():
            ModuleClass = self._load_class(module.get('class'))
            module['interface'] = self._interface[module['interface']]
            module['manager'] = self
            if module_name != 'module':
                module['name'] = module_name
            self._module[module_name] = ModuleClass(**module)
            self._log.info("[manager] Loaded device module '%s' with '%s' class." % (self._module[module_name]._name, module.get('class')))


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
        self._log.info("[manager] Started reading data iteration %s/%s at %s." % (self._read_iter, self._read_cycle, time.time()))
        for module_name, module in self._module.items():
            module_data = module.read_data()
            data = data + module_data
            if module_data == None:
                self._log.info("[%s] Failure reading the data at %s." % (module._name, time.time()))
            else:
                self._log.info("[%s] Received data %s at %s." % (module._name, module_data, time.time()))
        self._read_cache.append(data)


    def _publish_data(self):
        self._log.info("[manager] Publishing data at %s." % (time.time()))
        cache = self._read_cache
        self._log.info("[manager] Publishing data at %s." % cache)
        data = {}
        for i in range(self._read_cycle):
            #iter = cache[i]
            pass
            #if not data.get()
        for comm_name, comm in self._comm.items():
            comm.send_data(data)
        self._read_cache = []
        self._read_iter = 1


    def _single_loop(self):
        """
        Run single global service loop
        """
        while True:
            time_start = time.time()
            self._read_data()
            time_stop = time.time()
            time_delta = time_stop - time_start
            self._log.info("[manager] Finished reading data iteration %s/%s took %sms." % (self._read_iter, self._read_cycle, time_delta * 1000))
            sleep_delta = (self._read_interval / 1000) - time_delta
            if self._read_iter < self._read_cycle:
                self._read_iter += 1
            else:
                self._publish_data()
            time.sleep(sleep_delta)


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
