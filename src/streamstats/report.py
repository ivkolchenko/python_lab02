import typer
from streamstats import models

def console_report(counter: models.LogStatistics):
    typer.echo(f"Общее количество событий: {counter.event_count}")

    typer.echo("\nКоличество событий по уровням:")
    for level in counter.levels.keys():
        typer.echo(f" - {level}: {counter.levels[level]}")

    typer.echo("\nКоличество событий по источникам:")
    for source in counter.sources.keys():
        typer.echo(f" - {source}: {counter.sources[source]}")

    typer.echo("\nТОП-5 источников уровня ERROR:")
    for element in counter.error_sources.most_common(5):
        typer.echo(f" - {element[0]}: {element[1]}")

    typer.echo("\nТОП-5 источников уровня CRITICAL:")
    for element in counter.critical_sources.most_common(5):
        typer.echo(f" - {element[0]}: {element[1]}")

    typer.echo(f"\nПервая временная метка: {counter.first_timestamp}")
    typer.echo(f"Последняя временная метка: {counter.last_timestamp}")
