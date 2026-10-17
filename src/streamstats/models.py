from typing import Literal
from pydantic import BaseModel, Field
from datetime import datetime
from collections import Counter

class EventModel(BaseModel):
    timestamp: datetime
    level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    source: str = Field(min_length=1)
    message: str

class LogStatistics:
    event_count: int = 0
    first_timestamp: datetime|None = None
    last_timestamp: datetime|None = None

    def __init__(self):
        self.levels = Counter()
        self.sources = Counter()
        self.error_sources = Counter()
        self.critical_sources = Counter()
