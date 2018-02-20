"""Functions that implement the functionality of console scripts."""
from wherepy.track.ndi import Tracker
from ._collector import Collector
from ._indicator import run_indicator_cli


def collector_gui():
    """Start tracking data collector in GUI mode."""

    # pylint:disable=unused-variable

    collector = Collector(graphical=True)


def collector_cli():
    """Start tracking data collector in CLI mode."""

    # pylint:disable=unused-variable

    collector = Collector(graphical=False)


def indicator_cli():
    """Live CLI tracking quality and error indicator."""

    tracker = Tracker()
    run_indicator_cli(tracker=tracker)
