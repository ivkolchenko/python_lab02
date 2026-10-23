from collections import Counter
from dataclasses import dataclass, field, fields
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class EventModel(BaseModel):
    timestamp: datetime
    level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    source: str = Field(min_length=1)
    message: str

@dataclass
class LogStatistics:
    event_count: int = 0
    skipped_count: int = 0

    first_timestamp: datetime|None = None
    last_timestamp: datetime|None = None

    levels: Counter = field(default_factory=Counter)
    sources: Counter = field(default_factory=Counter)
    error_sources: Counter = field(default_factory=Counter)
    critical_sources: Counter = field(default_factory=Counter)

    def to_dict(self) -> dict[str, int | str | dict[str, int]]:
        """Преобразование класса в выходной словарь"""
        result: dict = {}

        for class_field in fields(self):
            value = getattr(self, class_field.name)

            if isinstance(value, Counter):
                if class_field.name in ["error_sources", "critical_sources"]:
                    value = dict(value.most_common(5))
                else:
                    value = dict(value)
            elif isinstance(value, datetime):
                value = value.isoformat()

            result[class_field.name] = value

        return result
