import time
from functools import partial
from pathlib import Path

import typer
from cli.formatters import create_progress_spinner
from etl_service.data_set_helper import DataSetHelper
from etl_service.file_convertor import FileConvertor
from etl_service.handler import handle
from rich import print, progress


def start_etl_service(
    directory: Path = typer.Argument(
        Path().home() / "gtzan",
        exists=True,
        file_okay=False,
        dir_okay=True,
        readable=True,
        resolve_path=True,
        help=(
            "Directory to watch for '.wav' files. "
            "Processed files are moved to '<directory>/processed'"
        ),
    ),
    seconds_to_sleep: int = typer.Option(
        60,
        "--sleep",
        min=10,
        max=600,
        help="Number of seconds to sleep between checks for newly added files",
    ),
):
    data_set_helper = DataSetHelper(directory)
    file_converter = FileConvertor(data_set_helper)

    print(f"\n[yellow] Watching {directory}...[/]")
    print(" Press [yellow]CTRL+C[/] to exit.\n")

    progress_indicator, pause_spinner = create_progress_spinner(
        progress.TextColumn("Total spectrograms processed: {task.completed}."),
        progress.TextColumn("{task.description}"),
    )
    spectrograms_task = progress_indicator.add_task(description="", total=None)
    update_task = partial(progress_indicator.update, spectrograms_task)

    spectrograms_processed = 0
    while True:
        update_task(description="[bold italic green]Checking for and processing files...[/]")
        spectrograms_processed += handle(file_converter)
        time.sleep(2)  # smooth animation (if no files are processed)

        with pause_spinner():
            update_task(
                description=f"[bold italic black]Sleeping for {seconds_to_sleep} seconds...[/]",
                completed=spectrograms_processed,
            )
            time.sleep(seconds_to_sleep)


def main():
    typer.run(start_etl_service)
