class StreamstatsError(Exception):
    pass

class UnsupportedFormat(StreamstatsError):
    pass

class InvalidEvent(StreamstatsError):
    pass

class InvalidTimestamp(StreamstatsError):
    pass

class CliConfigurationError(StreamstatsError):
    pass
