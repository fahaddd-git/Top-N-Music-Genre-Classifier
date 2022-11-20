from contextlib import contextmanager

from rich import progress


def create_progress_spinner(
    *columns: progress.TextColumn,
    default_speed: float = 1.0,
    start: bool = True,
):
    """Return a printable ``Progress`` and a context manager that pauses its spinner"""
    # Progress indicator inspired by the example at:
    #  URL: https://rich.readthedocs.io/en/stable/progress.html#advanced-usage
    #  Date: 11/19/22
    spinner = progress.SpinnerColumn()
    progress_indicator = progress.Progress(spinner, *columns, transient=False)

    @contextmanager
    def pause_spinner():
        try:
            spinner.set_spinner(spinner_name="dots", speed=0)
            yield
        finally:
            spinner.set_spinner(spinner_name="dots", speed=default_speed)

    if start:
        progress_indicator.start()

    return progress_indicator, pause_spinner
