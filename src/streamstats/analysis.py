from src.streamstats import models

def analise(event: models.EventModel, counter: models.LogStatistics):
    """Обновление статистики событий"""
    counter.event_count += 1
    counter.levels[event.level] += 1
    counter.sources[event.source] += 1

    if event.level == "ERROR":
        counter.error_sources[event.source] += 1
    elif event.level == "CRITICAL":
        counter.critical_sources[event.source] += 1

    if counter.first_timestamp is None:
        counter.first_timestamp = event.timestamp
    elif counter.first_timestamp > event.timestamp:
        counter.first_timestamp = event.timestamp

    if counter.last_timestamp is None:
        counter.last_timestamp = event.timestamp
    elif counter.last_timestamp < event.timestamp:
        counter.last_timestamp = event.timestamp
