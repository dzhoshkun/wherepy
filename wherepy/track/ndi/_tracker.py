"""Internal module that keeps the Tracker class for NDI devices."""

from time import sleep
import wherepy.track
try:
    import ndicapy as pyndicapi
except ImportError:
    import pyndicapi  # legacy
from pyndicapi import (ndiDeviceName, ndiProbe, ndiOpen, ndiClose,
                       ndiCommand, NDI_OKAY, ndiGetError, ndiErrorString,
                       ndiGetGXTransform, NDI_XFORMS_AND_STATUS,
                       NDI_115200, NDI_8N1, NDI_NOHANDSHAKE)


class Tracker(wherepy.track.Tracker):
    """This class is an abstraction for NDI trackers.

    Currently only NDI Aurora trackers with only one tool
    plugged in are supported.
    """

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

        # initialise device, initialise and enable tool ports, and start tracking
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

        # stop tracking, disable tool ports and put device back to pristine state
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

        # disconnect from device
        ndiClose(self.device)

        # all fine, reset connected status
        self.device = None
        self.__connected = False

    def capture(self, tool_id):
        if not self.connected:
            raise IOError('Not connected to an NDI tracker')

        # currently only first port of an Aurora supported
        if tool_id != self.tool_port_id:
            raise ValueError('Tool ID {} not supported currently. Only {}'
                             ' supported.'.format(tool_id, self.tool_port_id))

        # send command to get tracking data
        command = 'GX:{:04x}'.format(NDI_XFORMS_AND_STATUS)
        ndiCommand(self.device, command)
        error = ndiGetError(self.device)
        if error != NDI_OKAY:
            raise IOError('Could not send command {} to NDI device. The error'
                          ' was: {}'.format(command, ndiErrorString(error)))

        # acquire transform
        transform = ndiGetGXTransform(self.device, str(tool_id))
        error = ndiGetError(self.device)
        if error != NDI_OKAY:
            raise IOError('Could not capture tool with ID {}. The error was:'
                          ' {}'.format(tool_id, ndiErrorString(error)))

        # parse obtained transformation numbers
        try:
            quaternion = [float(value) for value in transform[:4]]
            coordinates = [float(value) for value in transform[4:7]]
            error = float(transform[-1])
        except ValueError:
            raise IOError('Could not parse returned data of tool with ID {}. The'
                          ' data was: {}'.format(tool_id, transform))

        quality = wherepy.track.utils.quality(error, 3.00, 0.00)

        # return the actual tool pose, at long last...
        return wherepy.track.ToolPose(
            tid=tool_id, quaternion=quaternion, coordinates=coordinates,
            quality=quality, error=error,
        )
