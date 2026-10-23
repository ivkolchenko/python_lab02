import typer
import json
from src.streamstats import models, errors
from pathlib import Path

def json_report(counter: models.LogStatistics, path: Path):
    if path.suffix != ".json":
        raise errors.CliConfigurationError("Неверный формат выходного файла")

    try:
        file = open(path, "r+", encoding="utf-8")
    except FileNotFoundError:
        file = open(path, "w", encoding="utf-8")

    with file:
        data = ""
        if file.mode == "r+":
            for string in file:
                data += string

        result = []

        if data != "":
            try:
                result = json.loads(data)
            except json.JSONDecodeError:
                raise errors.CliConfigurationError("Не удалось расшифровать выходной json файл")

            if isinstance(result, dict):
                result = [result]

        result.append(counter.to_dict())
        result = json.dumps(result, ensure_ascii=False, indent=4, default=str)

        file.seek(0)
        file.write(result)
        file.truncate()
