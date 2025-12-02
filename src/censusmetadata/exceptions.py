class CensusMetaDataError(Exception):
    """Base exception for censusmetadata errors."""


class FailedRequestError(CensusMetaDataError):
    """Raised when error reported by the API."""
    def __init__(self, message):
        self.message = message
        msg = message
        super().__init__(msg)


class MissingKeyError(CensusMetaDataError):
    """Raised when expected key is missing from API response."""
    def __init__(self, value, value_type):
        self.value = value
        if value:
            msg = f"Expected {value_type} '{value}' not found in API response."
        super().__init__(msg)
