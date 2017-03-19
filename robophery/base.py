
import logging
import platform
import time
from importlib import import_module
from robophery.utils.math import list_avg, list_min, list_max
from robophery.utils.rpi import detect_pi_version, detect_pi_revision

logging.basicConfig(format="%(created)f %(name)s [%(levelname)s] %(message)s", level=logging.DEBUG)

class ModuleManager(object):

    SERVICE_NAME = 'robo01'
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
        self._log = self._get_logger(self._name)
        self._log.info("Service {0} is starting in {1} mode.".format(self._name, self._run_mode))
        self._log.debug("Log level set to {0} with {1} handler(s).".format(logging.DEBUG, ', '.join(self._log_handlers)))

        # setting up platform
        self._platform = kwargs.get('platform', None)
        if self._platform == None:
            self._platform = self._detect_platform()

        # setting up read intervals
        self._read_interval = kwargs.get('read_interval', self.READ_INTERVAL)
        self._publish_interval = kwargs.get('publish_interval', self.PUBLISH_INTERVAL)
        if self._publish_interval % self._read_interval != 0:
            raise ValueError("Robophery publish_interval must be divisible by read_interval.")
        self._read_cycle = self._publish_interval / self._read_interval
        self._log.info("Read interval is {0}ms, publish interval is {1}ms, data bucket contains {2} items.".format(self._read_interval, self._publish_interval, self._read_cycle))

        # setting up base classes
        self._setup_communication(self._config['comm'])
        self._setup_interfaces(self._config['interface'])
        self._setup_modules(self._config['module'])

        self._log.info("Service {0} successfuly started in {1} mode as {2} platform.".format(self._name, self._run_mode, self._platform))


    def _get_logger(self, name):
        log = logging.getLogger(name)
        if 'console' in self._log_handlers:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.DEBUG)
            log.addHandler(console_handler)
        return log


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
        """
        Initialise communication channels
        """
        for comm_name, comm in comms.items():
            CommClass = self._load_class(comm.get('class'))
            comm['name'] = comm_name
            comm['manager'] = self
            self._comm[comm_name] = CommClass(**comm)


    def _setup_interfaces(self, interfaces={}):
        """
        Initialise platform bus interfaces
        """
        for interface_name, interface in interfaces.items():
            InterfaceClass = self._load_class(interface.get('class'))
            interface['name'] = interface_name
            interface['manager'] = self
            if 'parent' in interface:
                interface['parent']['interface'] = self._interface[interface['parent']['interface']]
            self._interface[interface_name] = InterfaceClass(**interface)


    def _setup_modules(self, modules={}):
        """
        Initialise platform modules
        """
        for module_name, module in modules.items():
            ModuleClass = self._load_class(module.get('class'))
            if module_name != 'module':
                module['name'] = module_name
            module['manager'] = self
            module['interface'] = self._interface[module['interface']]
            self._module[module_name] = ModuleClass(**module)


    def _load_class(self, name):
        """
        Load class by path string
        """
        if isinstance(name, str):
            module = import_module(".".join(name.split(".")[:-1]))
            if module:
                return getattr(module, name.split(".")[-1], None)
            raise Exception("Cannot load class {0}".format(name))


    def _read_data(self):
        """
        Read data from all registered modules
        """
        data = []
        time_start = time.time()
        self._log.debug("Started data reading cycle, iteration {0} of {1}.".format(self._read_iter, self._read_cycle))
        for module_name, module in self._module.items():
            module_data = module.read_data()
            data = data + module_data
        self._read_cache.append(data)
        time_stop = time.time()
        time_delta = time_stop - time_start
        self._log.debug("Finished data reading cycle, iteration {0} of {1}, operation took {2} ms.".format(self._read_iter, self._read_cycle, time_delta * 1000))
        return time_delta


    def _publish_data(self):
        self._log.info("Started publishing data.")
        cache = self._read_cache
        data = {}
        output_data = {}
        for i in range(self._read_cycle):
            cycle_data = cache[i]
            for metric in cycle_data:
                name = "{0}.{1}".format(metric[0], metric[1])
                if metric[2] != None:
                    if "{0}.value".format(name) in data:
                        data["{0}.value".format(name)].append(metric[2])
                    else:
                        data["{0}.value".format(name)] = [metric[2]]
                    if len(metric) > 3:
                        if "{0}.read_time".format(name) in data:
                            data["{0}.read_time".format(name)].append(metric[3])
                        else:
                            data["{0}.read_time".format(name)] = [metric[3]]
                else:
                    if "{0}.error".format(name) in data:
                        data["{0}.error".format(name)].append(0)
                    else:
                        data["{0}.error".format(name)] = [0]
        for datum_name, datum in data.items():
            metric_name = '.'.join(datum_name.split('.')[:-1])
            if not metric_name in output_data:
                output_data[metric_name] = {}
            metric_type = datum_name.split('.')[-1]
            if metric_type == 'value':
                value_min = list_min(datum)
                value_max = list_max(datum)
                value_avg = list_avg(datum)
                output_data[metric_name]["min_value"] = value_min
                output_data[metric_name]["max_value"] = value_max
                output_data[metric_name]["avg_value"] = value_avg
            if metric_type == 'read_time':
                read_avg = list_avg(datum)
                output_data[metric_name]["read_time"] = read_avg
            if metric_type == 'error':
                error_avg = list_avg(datum)
                output_data[metric_name]["error_rate"] = error_avg
        for comm_name, comm in self._comm.items():
            comm.send_data(output_data)
        self._read_cache = []
        self._read_iter = 1


    def _single_loop(self):
        """
        Run single global service loop
        """
        while True:
            time_delta = self._read_data()
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


class Interface(object):

    DEVICE_NAME = 'unknown-bus'

    def __init__(self, *args, **kwargs):
        self._name = kwargs.get('name', self.DEVICE_NAME)
        self._class = kwargs.get('class', None)
        self._manager = kwargs.get('manager', None)
        self._log = self._manager._get_logger(self._name)
        self._log.info("Started bus interface {0}.".format(self))


    def __str__(self):
        return self._base_name()


    def _msleep(self, milliseconds):
        """
        Sleep for the specified amount of milliseconds.
        """
        self._log.debug("Sleeping for {0} ms.". format(milliseconds))
        time.sleep(milliseconds / 1000.0)


    def _usleep(self, microseconds):
        """
        Sleep the specified amount of microseconds.
        """
        self._log.debug("Sleeping for {0} us.". format(microseconds))
        time.sleep(microseconds / 1000000.0)


    def _base_name(self):
        return '{0} {1}'.format(self._class.split('.')[-1], self._name)


class Module(object):

    DEVICE_NAME = 'unknown-device'
    READ_INTERVAL = 2000

    def __init__(self, *args, **kwargs):
        self._name = kwargs.get('name', self.DEVICE_NAME)
        self._manager = kwargs.get('manager', None)
        self._interface = kwargs.get('interface', None)
        self._class = kwargs.get('class', None)
        self._read_interval = kwargs.get('read_interval', self.READ_INTERVAL)
        self._log = self._manager._get_logger(self._name)
        self._log.info("Started device module {0}.".format(self))


    def __str__(self):
        return self._base_name()


    def _base_name(self):
        return '{0} {1}'.format(self._class.split('.')[-1], self._name)


    def _log_data(self, data):
        if data == None:
            self._log.error("Failure reading data.")
        else:
            for datum in data:
                self._log.debug("Reading {0}.{1} metric, value {2} {3}.".format(datum[0], datum[1], datum[2], self.meta_data()[datum[1]]['unit']))


    def _msleep(self, milliseconds):
        """
        Sleep for the specified amount of milliseconds.
        """
        self._log.debug("Sleeping for {0} ms.". format(milliseconds))
        time.sleep(milliseconds / 1000.0)


    def _usleep(self, microseconds):
        """
        Sleep the specified amount of microseconds.
        """
        self._log.debug("Sleeping for {0} us.". format(microseconds))
        time.sleep(microseconds / 1000000.0)


    def _service(self):

        self._cycle_iteration = 1
        self._cache = []
