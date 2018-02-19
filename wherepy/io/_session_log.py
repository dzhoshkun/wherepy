"""Internal module that keeps the SessionLog class."""

from os.path import (exists, dirname)
from os import (utime, makedirs)
from yaml import dump


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

        # dirname returns empty string if filepath is just a filename
        # ie. to be created within current directory, hence the use
        # of "or"
        directory = dirname(filepath) or '.'
        if not exists(directory):
            makedirs(directory)

        try:
            with open(filepath, 'w'):
                utime(filepath, None)
        except IOError as io_error:
            raise OSError('Creation of session log file {} failed'
                          ' due to {}'.format(filepath, io_error))

        self.__filepath = filepath
        self.__current_index = 0

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
        with open(self.__filepath, 'a') as session_log_file:
            yaml_dict = {
                self.__current_index: {
                    tool_pose.tid(): {
                        'quaternion': tool_pose.quaternion(),
                        'coordinates': tool_pose.coordinates(),
                        'quality': tool_pose.quality(),
                        'error': tool_pose.error(),
                        'timestamp': tool_pose.timestamp(),
                    }
                }
            }
            session_log_file.write(dump(yaml_dict))
            self.__current_index += 1
