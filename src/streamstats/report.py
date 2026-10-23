import json
import os
from pathlib import Path

from src.streamstats import errors, models


def json_report(counter: models.LogStatistics, path: Path):
    if path.suffix != ".json":
        raise errors.CliConfigurationError("Неверный формат выходного файла")

    open_format = "r+" if os.path.exists(path) else "w"

    with open(path, open_format, encoding="utf-8") as file:
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
