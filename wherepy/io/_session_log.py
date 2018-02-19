"""Internal module that keeps the SessionLog class."""

from os.path import (exists, dirname)
from os import (utime, makedirs)


class SessionLog(object):
    """This class takes care of logging all tracking data."""

    def __init__(self, filepath):
        """Create a blank session file in passed path.

        :param filepath: taken as-is, with absolutely no
        manipulation
        :raise OSError: if file creation fails for any reason
        :raise ValueError: if the file already exists, this is
        a safety measure not to overwrite existing data
        """
        if exists(filepath):
            raise ValueError('Filepath {} already exists, refusing'
                             ' to overwrite!'.format(filepath))

        directory = dirname(filepath)
        if not exists(directory):
            makedirs(directory)

        try:
            with open(filepath, 'w'):
                utime(filepath, None)
        except IOError as io_error:
            raise OSError('Creation of session log file {} failed'
                          ' due to {}'.format(filepath, io_error)
                          )

        self.__filepath = filepath

    @property
    def filepath(self):
        """Get this session log's filepath."""
        return self.__filepath

    @filepath.setter
    def filepath(self, filepath):
        """Do nothing: setting deliberately disallowed."""
        pass

    def append(self, tool_pose):
        """Append passed tool pose to session file.

        :type tool_pose: ToolPose
        """
        pass
