from contextlib import contextmanager

from rich import console, padding, progress, style, table


@contextmanager
def progress_spinner(loading_text: str, completed_text: str) -> progress.Progress:
    """Displays a spinning progress indicator

    :param loading_text: message displayed while task is running
    :param completed_text: message displayed when task is complete
    """
    # Inspired by: https://typer.tiangolo.com/tutorial/progressbar/#spinner
    # Date: 11/11/2022
    progress_indicator = progress.Progress(
        progress.SpinnerColumn(),
        progress.TextColumn("[progress.description]{task.description}"),
        transient=completed_text is None,
    )
    try:
        with progress_indicator:
            task = progress_indicator.add_task(
                description=f"[yellow]{loading_text}[/yellow]",
                total=None,
            )
            yield progress_indicator
            progress_indicator.update(task, description=completed_text, completed=True)
    finally:
        progress_indicator.stop()


def results_table(results: dict[str, float]) -> console.ConsoleRenderable:
    """Return results as a printable table"""
    formatted_results_table = table.Table(
        table.Column("Metric", justify="left"),
        table.Column("Value", justify="left"),
        title="Results",
        title_justify="left",
        title_style=style.Style(bold=True, color="blue"),
    )
    for key, value in results.items():
        formatted_results_table.add_row(f"{key}".title(), f"{value:.4f}")
    return padding.Padding(formatted_results_table, (1, 0))
