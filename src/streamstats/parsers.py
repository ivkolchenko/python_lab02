import csv
import json
from datetime import datetime
from streamstats import models, errors, analysis

def parse_csv(path: str, skip_invalid: bool, counter: models.LogStatistics):
    """Парсер формата CSV: Создание объекта EventModel,
    проверка на ошибки, передача в функцию анализа"""
    with open(path, "r") as file:

        for event_data in csv.DictReader(file):
            try:
                time = datetime.fromisoformat(event_data["timestamp"])
            except ValueError:
                if skip_invalid:
                    continue
                else:
                    raise errors.InvalidTimestamp("Неверная временная метка")
            except KeyError:
                raise errors.UnsupportedFormat("Неподдерживаемый формат событий")


            try:
                event = models.EventModel(
                    timestamp= time,
                    level= event_data["level"],
                    source= event_data["source"],
                    message= event_data["message"]
                )
            except ValueError:
                if skip_invalid:
                    continue
                else:
                    raise errors.InvalidEvent("Неверное событие")
            except KeyError:
                raise errors.UnsupportedFormat("Неподдерживаемый формат событий")

            analysis.analise(event, counter)

def parse_json(path: str, skip_invalid: bool, counter: models.LogStatistics):
    """Парсер формата JSONL: Создание объекта EventModel,
    проверка на ошибки, передача в функцию анализа"""
    with open(path, "r") as file:

        for string in file:
            event_data = json.loads(string)
            try:
                time = datetime.fromisoformat(event_data["timestamp"])
            except ValueError:
                if skip_invalid:
                    continue
                else:
                    raise errors.InvalidTimestamp("Неверная временная метка")
            except KeyError:
                if skip_invalid:
                    continue
                else:
                    raise errors.UnsupportedFormat("Неподдерживаемый формат события")


            try:
                event = models.EventModel(
                    timestamp= time,
                    level= event_data["level"],
                    source= event_data["source"],
                    message= event_data["message"]
                )
            except ValueError:
                if skip_invalid:
                    continue
                else:
                    raise errors.InvalidEvent("Неверное событие")
            except KeyError:
                if skip_invalid:
                    continue
                else:
                    raise errors.UnsupportedFormat("Неподдерживаемый формат события")

            analysis.analise(event, counter)