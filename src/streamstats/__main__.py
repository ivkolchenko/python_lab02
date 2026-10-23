from pathlib import Path
from typing import Annotated

import typer

from src.streamstats import errors, models, parsers, report

app = typer.Typer()

@app.command()
def analyze(
        path: Annotated[Path, typer.Argument()],
        events_format: Annotated[str, typer.Option('--format')],
        output: Annotated[Path, typer.Option('--output')],
        skip_invalid: Annotated[bool, typer.Option("--skip-invalid")] = False):

    counter = models.LogStatistics()

    try:
        if events_format == "csv":
            parsers.parse_csv(path, skip_invalid, counter)
        elif events_format == "jsonl":
            parsers.parse_json(path, skip_invalid, counter)
        else:
            raise errors.UnsupportedFormat("Неправильный формат файла")

        report.json_report(counter, output)

    except errors.StreamstatsError as error:
        typer.echo(f'Ошибка: {error}', err=True)
        raise typer.Exit(code=2)


@app.callback()
def main():
    pass


if __name__ == '__main__':
    app()
