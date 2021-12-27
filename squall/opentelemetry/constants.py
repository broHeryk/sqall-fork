from enum import Enum


class SpanName(Enum):
    response_preparation = 'Response preparation'
    pulling_request_data = "Getting response data"
    handle = "Handling"
    returning_response = "Send response"
    middleware_processing = "Middleware processing"
