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
