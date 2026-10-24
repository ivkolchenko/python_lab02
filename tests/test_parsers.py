import logging
from collections import Counter
from datetime import datetime
from pathlib import Path

import pytest

from src.streamstats import errors, models, parsers


def test_valid():
    """Тест удовлетворящих условиям файлов"""
    path_csv = Path("tests/fixtures/valid.csv")
    path_json = Path("tests/fixtures/valid.jsonl")

    for path in [path_csv, path_json]:
        logger = logging.getLogger(__name__)
        counter = models.LogStatistics()

        if path == path_json:
            parsers.parse_json(path, False, counter, logger)
        else:
            parsers.parse_csv(path, False, counter, logger)

        assert counter.event_count == 7
        assert counter.levels == Counter({"DEBUG": 1, "INFO": 1, "WARNING": 1, "ERROR": 2, "CRITICAL": 2})
        assert counter.sources == Counter({"api": 3, "worker": 2, "db": 2})
        assert counter.error_sources == Counter({"db": 1, "api": 1})
        assert counter.critical_sources == Counter({"db": 1, "worker": 1})
        assert counter.first_timestamp == datetime.fromisoformat("2024-06-01T11:30:00+00:00")
        assert counter.last_timestamp == datetime.fromisoformat("2024-06-01T12:30:00+00:00")


def test_mixed():
    """Тест файлов с ошибкой в строке"""
    path_csv = Path("tests/fixtures/mixed_invalid.csv")
    path_json = Path("tests/fixtures/mixed_invalid.jsonl")

    #Негативные тесты
    with pytest.raises(errors.StreamstatsError):
        logger = logging.getLogger(__name__)
        counter = models.LogStatistics()
        parsers.parse_csv(path_csv, False, counter, logger)
    with pytest.raises(errors.StreamstatsError):
        logger = logging.getLogger(__name__)
        counter = models.LogStatistics()
        parsers.parse_json(path_json, False, counter, logger)

    #Позитивные тесты
    for path in [path_csv, path_json]:
        logger = logging.getLogger(__name__)
        counter = models.LogStatistics()

        if path == path_json:
            parsers.parse_json(path, True, counter, logger)
        else:
            parsers.parse_csv(path, True, counter, logger)

        assert counter.event_count == 2
        assert counter.skipped_count == 4
        assert counter.levels == Counter({"INFO": 1, "ERROR": 1})
        assert counter.sources == Counter({"api": 1, "db": 1})
        assert counter.error_sources == Counter({"db": 1})
        assert counter.first_timestamp == datetime.fromisoformat("2024-06-01T10:00:00+00:00")
        assert counter.last_timestamp == datetime.fromisoformat("2024-06-01T10:20:00+00:00")


def test_invalid():
    """Тест файлов с явной ошибкой"""
    #Пустые файлы
    with pytest.raises(errors.StreamstatsError):
        logger = logging.getLogger(__name__)
        counter = models.LogStatistics()
        parsers.parse_csv(Path("fixtures/empty.csv"), False, counter, logger)
    with pytest.raises(errors.StreamstatsError):
        logger = logging.getLogger(__name__)
        counter = models.LogStatistics()
        parsers.parse_json(Path("fixtures/empty.jsonl"), True, counter, logger)

    #Несуществующие файлы
    with pytest.raises(errors.StreamstatsError):
        logger = logging.getLogger(__name__)
        counter = models.LogStatistics()
        parsers.parse_csv(Path("fixtures/not_exists.csv"), False, counter, logger)
    with pytest.raises(errors.StreamstatsError):
        logger = logging.getLogger(__name__)
        counter = models.LogStatistics()
        parsers.parse_json(Path("fixtures/not_exists.jsonl"), True, counter, logger)

    #Ошибка Unicode
    with pytest.raises(errors.StreamstatsError):
        logger = logging.getLogger(__name__)
        counter = models.LogStatistics()
        parsers.parse_csv(Path("fixtures/invalid_utf8.csv"), False, counter, logger)
    with pytest.raises(errors.StreamstatsError):
        logger = logging.getLogger(__name__)
        counter = models.LogStatistics()
        parsers.parse_json(Path("fixtures/invalid_utf8.jsonl"), True, counter, logger)
