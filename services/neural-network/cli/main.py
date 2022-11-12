import typer
from cli.helpers import set_reasonable_logging_settings


def main():
    set_reasonable_logging_settings()
    from cli.app import generate_model

    typer.run(generate_model)


if __name__ == "__main__":
    main()
