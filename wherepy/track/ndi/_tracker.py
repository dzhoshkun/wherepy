"""Internal module that keeps the Tracker class for NDI devices."""

import wherepy.track
from pyndicapi import (ndiDeviceName, ndiProbe, ndiOpen, ndiClose,
                       ndiCommand, NDI_OKAY, ndiGetError, ndiErrorString,
                       NDI_115200, NDI_8N1, NDI_NOHANDSHAKE, ndiGetTXTransform)


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

    def disconnect(self):
        if not self.connected:
            raise IOError('Not connected to an NDI tracker')

        ndiClose(self.device)
        self.device = None
        self.__connected = False

    def capture(self, tool_id):
        return super(Tracker, self).capture(tool_id)
