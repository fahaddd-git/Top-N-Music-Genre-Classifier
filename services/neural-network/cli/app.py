from pathlib import Path

import typer
from cli.formatters import progress_spinner, results_table
from neural_network.data_ingestion_helpers import train_test_split
from neural_network.genre_classification_model import GenreClassificationModel
from rich import print


def generate_model(
    epochs: int = typer.Option(
        ...,
        "--epochs",
        min=1,
        max=100,
        prompt="Please enter the number of epochs per run",
        help="The number of neural network epochs (cycles) to run.",
    ),
    output_directory: Path = typer.Option(
        ...,
        "--output",
        exists=False,
        file_okay=False,
        dir_okay=True,
        writable=True,
        resolve_path=True,
        prompt="Please enter an output directory for the model",
        help="Directory where model output should be saved.",
    ),
):
    while True:
        # create and fit
        with progress_spinner("Loading data...", "Done loading data."):
            spectrogram_data = train_test_split()
            spectrogram_model = GenreClassificationModel(spectrogram_data)

        print("  [yellow]Creating model[/yellow]...")
        spectrogram_model.fit(epochs)
        # progress indicator breaks keras output w/o callback adjust
        # with progress_spinner("Loading model...", "Done loading model.") as progress:
        #     spectrogram_model.fit(epochs)

        # evaluate and display results
        results = spectrogram_model.evaluate()
        table = results_table(results)
        print(table)

        # prompt for save
        should_save = typer.confirm(f"Save model to {output_directory}?")
        should_write = should_save and (
            not output_directory.exists() or typer.confirm("Overwrite existing model?")
        )
        if should_save and should_write:
            print(f"Saving to {output_directory}...")
            spectrogram_model.save(output_directory)
            print("[green]Success![/green]", end="\n\n")

        should_exit = not typer.confirm("Try again?")
        if should_exit:
            raise typer.Exit()


if __name__ == "__main__":
    typer.run(generate_model)
