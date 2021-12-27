from enum import Enum


class SpanName(str, Enum):
    response_preparation = 'Response preparation'
    pulling_request_data = "Getting response data"
    handle = "Handling"
    returning_response = "Send response"
    middleware_processing = "Middleware processing"

    def __str__(self):
        return self.value
