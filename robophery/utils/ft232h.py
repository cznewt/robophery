
import ftdi1 as ftdi

FT232H_VID = 0x0403   # Default FTDI FT232H vendor ID
FT232H_PID = 0x6014   # Default FTDI FT232H product ID


def enumerate_device_serials(vid=FT232H_VID, pid=FT232H_PID):
    """
    Return a list of all FT232H device serial numbers connected to the
    machine. You can use these serial numbers to open a specific FT232H device
    by passing it to the FT232H initializer's serial parameter.
    """
    try:
        # Create a libftdi context.
        ctx = None
        ctx = ftdi.new()
        # Enumerate FTDI devices.
        device_list = None
        count, device_list = ftdi.usb_find_all(ctx, vid, pid)
        if count < 0:
            raise RuntimeError('ftdi_usb_find_all returned error {0}: {1}'.format(count, ftdi.get_error_string(self._ctx)))
        # Walk through list of devices and assemble list of serial numbers.
        devices = []
        while device_list is not None:
            # Get USB device strings and add serial to list of devices.
            ret, manufacturer, description, serial = ftdi.usb_get_strings(ctx, device_list.dev, 256, 256, 256)
            if ret < 0:
                raise RuntimeError('ftdi_usb_get_strings returned error {0}: {1}'.format(ret, ftdi.get_error_string(self._ctx)))
            devices.append(serial)
            device_list = device_list.next
        return devices
    finally:
        # Make sure to clean up list and context when done.
        if device_list is not None:
            ftdi.list_free(device_list)
        if ctx is not None:
            ftdi.free(ctx)