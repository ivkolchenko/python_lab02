from typing import Annotated
import typer
from streamstats import parsers, models, errors, report

app = typer.Typer()

@app.command()
def analyze(
        path: str,
        events_format: Annotated[str, typer.Option('--format')],
        skip_invalid: Annotated[bool, typer.Option("--skip-invalid")] = False):

    counter = models.LogStatistics()

    try:
        if events_format == "csv":
            parsers.parse_csv(path, skip_invalid, counter)
        elif events_format == "jsonl":
            parsers.parse_json(path, skip_invalid, counter)
        else:
            raise errors.CliConfigurationError("Неправильный формат файла")

        report.console_report(counter)

    except errors.StreamstatsError as error:
        typer.echo(f'Ошибка: {error}', err=True)
        raise typer.Exit(code=2)


@app.callback()
def main():
    pass


if __name__ == '__main__':
    app()