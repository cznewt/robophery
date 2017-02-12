
import logging
import platform
import re


def detect_pi_version():
    """
    Detect the version of the Raspberry Pi.  Returns either 1, 2 or
    None depending on if it's a Raspberry Pi 1 (model A, B, A+, B+),
    Raspberry Pi 2 (model B+), or not a Raspberry Pi.

    Check /proc/cpuinfo for the Hardware field value:
    * 2708 is pi 1
    * 2709 is pi 2
    * Anything else is not a pi.
    """
    with open('/proc/cpuinfo', 'r') as infile:
        cpuinfo = infile.read()
    # Match a line like 'Hardware   : BCM2709'
    match = re.search('^Hardware\s+:\s+(\w+)$', cpuinfo,
                      flags=re.MULTILINE | re.IGNORECASE)
    if not match:
        # Couldn't find the hardware, assume it isn't a pi.
        return None
    if match.group(1) == 'BCM2708':
        # Pi 1
        return 1
    elif match.group(1) == 'BCM2709':
        # Pi 2
        return 2
    else:
        # Something else, not a pi.
        return None


def detect_pi_revision():
    """
    Detect the revision number of a Raspberry Pi, useful for changing
    functionality like default I2C bus based on revision.

    Revision list available at:
    http://elinux.org/RPi_HardwareHistory#Board_Revision_History
    """
    with open('/proc/cpuinfo', 'r') as infile:
        for line in infile:
            # Match a line of the form "Revision : 0002" while ignoring extra
            # info in front of the revsion (like 1000 when the Pi was over-volted).
            match = re.match('Revision\s+:\s+.*(\w{4})$', line, flags=re.IGNORECASE)
            if match and match.group(1) in ['0000', '0002', '0003']:
                # Return revision 1 if revision ends with 0000, 0002 or 0003.
                return 1
            elif match:
                # Assume revision 2 if revision ends with any other 4 chars.
                return 2
        # Couldn't find the revision, throw an exception.
        raise RuntimeError('Could not determine Raspberry Pi revision.')


class Module(object):

    DEVICE_NAME = 'unknown-device'
    READ_INTERVAL = 10000
    PUBLISH_INTERVAL = 60000

    UNKNOWN_PLATFORM = 0
    RASPBERRYPI_PLATFORM = 1
    BEAGLEBONE_PLATFORM = 2
    MINNOWBOARD_PLATFORM = 3
    NODEMCU_PLATFORM = 4
    FT232H_PLATFORM = 5


    def __init__(self, *args, **kwargs):
        self._name = kwargs.get('name', self.DEVICE_NAME)
        self._read_interval = kwargs.get('read_interval', self.READ_INTERVAL)
        self._publish_interval = kwargs.get('publish_interval', self.PUBLISH_INTERVAL)
        self._log_level = kwargs.get('log_level', 'debug')
        self._log = logging.getLogger('robophery.%s' % self._name)
        if kwargs.get('platform') in self._supported_platforms:
            self._platform = kwargs['platform']
        else:
            self._platform = self._detect_platform


    @property
    def _supported_platforms(self):
       return (
           self.RASPBERRYPI_PLATFORM,
           self.BEAGLEBONE_PLATFORM,
           self.MINNOWBOARD_PLATFORM,
           self.NODEMCU_PLATFORM,
           self.FT232H_PLATFORM
       )


    @property
    def _linux_platforms(self):
       return (
           self.RASPBERRYPI_PLATFORM,
           self.BEAGLEBONE_PLATFORM,
           self.MINNOWBOARD_PLATFORM
       )


    @property
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

        # Could not detect the platform, returning unknown.
        return self.UNKNOWN_PLATFORM


    def _service_loop(self):

        while True:
            self._cache[self._cycle_iteration] = self.read_data
            if self._cycle_iteration < self._cycle_size:
                self._cycle_iteration += 1
            else:
                self.publish_data(self._cache)
                self._cache = []
                self._cycle_iteration = 0
            print(self._cycle_iteration)
            sleep(self.READ_INTERVAL)


    def start_service(self):

        if self._publish_interval % self._read_interval != 0:
            raise RuntimeError('publish_interval must be divisible by read_interval.')
        self._cycle_size = self._publish_interval / self._read_interval
        self._cycle_iteration = 0
        self._cache = []
        print(self._cycle_size)
        self._service_loop()


    def publish_data(self, data):
        print(data)
        #mqtt publish

