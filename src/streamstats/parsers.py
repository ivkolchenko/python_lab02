import csv
import json
import logging
import os
from datetime import datetime
from pathlib import Path

from src.streamstats import analysis, errors, models


def parse_csv(path: Path, skip_invalid: bool, counter: models.LogStatistics, logger: logging.Logger):
    """Парсер формата CSV: Создание объекта EventModel,
    проверка на ошибки, передача в функцию анализа"""
    try:
        with open(path, "r", encoding="utf-8") as file:
            if os.path.getsize(path) == 0:
                raise errors.CliConfigurationError("Пустой файл")

            for string_number, event_data in enumerate(csv.DictReader(file)):
                try:
                    time = datetime.fromisoformat(event_data["timestamp"])

                    if time.tzinfo is None:
                        if skip_invalid:
                            logger.warning(f"Пропущена строка {string_number}")
                            counter.skipped_count += 1
                            continue
                        else:
                            raise errors.InvalidTimestamp("Неверная временная метка")
                except ValueError:
                    if skip_invalid:
                        logger.warning(f"Пропущена строка {string_number}")
                        counter.skipped_count += 1
                        continue
                    else:
                        raise errors.InvalidTimestamp("Неверная временная метка")
                except KeyError:
                    raise errors.CliConfigurationError("Неверный формат событий в файле")


                try:
                    event = models.EventModel(
                        timestamp= time,
                        level= event_data["level"],
                        source= event_data["source"],
                        message= event_data["message"]
                    )
                except ValueError:
                    if skip_invalid:
                        logger.warning(f"Пропущена строка {string_number}")
                        counter.skipped_count += 1
                        continue
                    else:
                        raise errors.InvalidEvent("Неверное событие")
                except KeyError:
                    raise errors.CliConfigurationError("Неверный формат событий в файле")

                analysis.analise(event, counter)
    except FileNotFoundError:
        raise errors.CliConfigurationError("Несуществующий файл")
    except csv.Error:
        raise errors.CliConfigurationError("Ошибка формата входного csv файла")
    except UnicodeDecodeError:
        raise errors.CliConfigurationError("Ошибка кодировки Unicode")


def parse_json(path: Path, skip_invalid: bool, counter: models.LogStatistics, logger: logging.Logger):
    """Парсер формата JSONL: Создание объекта EventModel,
    проверка на ошибки, передача в функцию анализа"""
    try:
        with open(path, "r", encoding="utf-8") as file:
            if os.path.getsize(path) == 0:
                raise errors.CliConfigurationError("Пустой файл")

            for string_number, string in enumerate(file):
                event_data = json.loads(string)
                try:
                    time = datetime.fromisoformat(event_data["timestamp"])

                    if time.tzinfo is None:
                        if skip_invalid:
                            logger.warning(f"Пропущена строка {string_number}")
                            counter.skipped_count += 1
                            continue
                        else:
                            raise errors.InvalidTimestamp("Неверная временная метка")
                except ValueError:
                    if skip_invalid:
                        logger.warning(f"Пропущена строка {string_number}")
                        counter.skipped_count += 1
                        continue
                    else:
                        raise errors.InvalidTimestamp("Неверная временная метка")
                except KeyError:
                    raise errors.InvalidEvent("Неверное событие")


                try:
                    event = models.EventModel(
                        timestamp= time,
                        level= event_data["level"],
                        source= event_data["source"],
                        message= event_data["message"]
                    )
                except ValueError:
                    if skip_invalid:
                        logger.warning(f"Пропущена строка {string_number}")
                        counter.skipped_count += 1
                        continue
                    else:
                        raise errors.InvalidEvent("Неверное событие")
                except KeyError:
                    if skip_invalid:
                        logger.warning(f"Пропущена строка {string_number}")
                        counter.skipped_count += 1
                        continue
                    else:
                        raise errors.InvalidEvent("Неверное событие")

                analysis.analise(event, counter)
    except FileNotFoundError:
        raise errors.CliConfigurationError("Несуществующий файл")
    except json.JSONDecodeError:
        raise errors.CliConfigurationError("Не удалось расшифровать входной jsonl файл")
    except UnicodeDecodeError:
        raise errors.CliConfigurationError("Ошибка кодировки Unicode")
