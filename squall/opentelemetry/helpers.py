from opentelemetry import trace


tracer = trace.get_tracer(__name__)


class CurrentSpan:
    """
        Wraps open telemetry start_as_current_span method.
        Intention to have this class is supporting of enabled flag to does nothing
        if open telemtry is disabled on application level.

    """
    def __init__(self, span_name, enabled):
        self.span_name = span_name
        self.enabled = enabled

    def __enter__(self):
        if not self.enabled:
            return
        self.trace = tracer.start_as_current_span(self.span_name)
        self.trace.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.enabled:
            return
        self.trace.__exit__(exc_type, exc_val, exc_tb)
