"""Functions that implement the functionality of console scripts."""
from ._collector import Collector


def collector_gui():
    """Start tracking data collector in GUI mode."""

    # pylint:disable=unused-variable

    collector = Collector(graphical=True)


def collector_cli():
    """Start tracking data collector in CLI mode."""

    # pylint:disable=unused-variable

    collector = Collector(graphical=False)
