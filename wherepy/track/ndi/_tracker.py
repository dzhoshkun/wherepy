"""Internal module that keeps the Tracker class for NDI devices."""

from time import sleep
import wherepy.track
from pyndicapi import (ndiDeviceName, ndiProbe, ndiOpen, ndiClose,
                       ndiCommand, NDI_OKAY, ndiGetError, ndiErrorString,
                       ndiGetGXTransform, NDI_XFORMS_AND_STATUS,
                       NDI_115200, NDI_8N1, NDI_NOHANDSHAKE)


class Tracker(wherepy.track.Tracker):
    """This class is an abstraction for NDI trackers."""

    SERIAL_PORTS_TO_TRY = 20

    def __init__(self):
        """Create an instance ready for connecting."""
        super(Tracker, self).__init__()
        self.device = None
        self.tool_port_id = 1

    def connect(self):
        if self.connected:
            return

        # try to detect a connected NDI device
        serial_port_name = ''
        for serial_port_no in range(Tracker.SERIAL_PORTS_TO_TRY):
            serial_port_name = ndiDeviceName(serial_port_no)
            if not serial_port_name:
                continue
            result = ndiProbe(serial_port_name)
            if result == NDI_OKAY:
                break
        if result != NDI_OKAY:
            raise IOError('Could not detect any attached NDI device.'
                          '\nPlease make sure:'
                          '\n\t* an NDI device is connected'
                          '\n\t* it is switched on'
                          '\n\t* and you have sufficient access rights')

        # try to connect to detected NDI device
        self.device = ndiOpen(serial_port_name)
        if not self.device:
            raise IOError('Could not connect to NDI device on {}'
                          ''.format(serial_port_name))

        commands = [
            'INIT:',
            'COMM:{:d}{:03d}{:d}'.format(NDI_115200, NDI_8N1, NDI_NOHANDSHAKE),
            'PHSR:02',
            'PINIT:{:02x}'.format(self.tool_port_id),
            'PHSR:03',
            'PENA:{:02x}{}'.format(self.tool_port_id, 'D'),  # other options: 'S' or 'B'
            'PHSR:00',
            'TSTART:',
        ]
        for command in commands:
            ndiCommand(self.device, command)
            error = ndiGetError(self.device)
            if error != NDI_OKAY:
                ndiClose(self.device)
                raise IOError('Could not send command {} to NDI device. The error'
                              ' was: {}'.format(command, ndiErrorString(error)))

        # okay! set connected status
        self.__connected = True

        sleep(1)  # artificial, to allow for initialisation

    def disconnect(self):
        if not self.connected:
            raise IOError('Not connected to an NDI tracker')

        commands = [
            'TSTOP:',
            'PHSR:04',
            'PDIS:{:02x}'.format(self.tool_port_id),
            'COMM:00000',
        ]
        for command in commands:
            ndiCommand(self.device, command)
            error = ndiGetError(self.device)
            if error != NDI_OKAY:
                ndiClose(self.device)
                raise IOError('Could not send command {} to NDI device. The error'
                              ' was: {}'.format(command, ndiErrorString(error)))

        ndiClose(self.device)
        self.device = None
        self.__connected = False

    def capture(self, tool_id):
        if not self.connected:
            raise IOError('Not connected to an NDI tracker')

        command = 'GX:{:04x}'.format(NDI_XFORMS_AND_STATUS)
        ndiCommand(self.device, command)
        error = ndiGetError(self.device)
        if error != NDI_OKAY:
            raise IOError('Could not send command {} to NDI device. The error'
                          ' was: {}'.format(command, ndiErrorString(error)))

        transform = ndiGetGXTransform(self.device, str(tool_id))
        error = ndiGetError(self.device)
        if error != NDI_OKAY:
            raise IOError('Could not capture tool with ID {}. The error was:'
                          ' {}'.format(tool_id, ndiErrorString(error)))
        if type(transform) == str:
            if transform.startswith('disabled') or transform.startswith('missing'):
                raise ValueError('Could not capture tool with ID {}. The error was:'
                                 ' {}'.format(tool_id, transform))

        quaternion = list(transform[:4])
        coordinates = list(transform[4:7])
        error = float(transform[-1])

        quality_min, quality_max = 0.00, 1.00  # %
        error_min, error_max = 0.00, 3.00  # mm
        error_range = error_max - error_min

        quality = quality_max * (error_max - error)
        quality += quality_min * (error - error_min)
        quality /= error_range

        return wherepy.track.ToolPose(
            tid=tool_id, quaternion=quaternion, coordinates=coordinates,
            quality=quality, error=error,
        )
