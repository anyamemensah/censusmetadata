class CensusMetaDataError(Exception):
    """Base class for all censusmetadata exceptions."""


class FailedRequestError(CensusMetaDataError):
    """Exception raised when error reported by the API."""
    def __init__(self, message):
        self.message = message
        msg = message
        super().__init__(msg)


class MissingAPIValueError(CensusMetaDataError, LookupError):
    """ 
    Custom LookupError raised when an expected key/value is 
    missing from the API response.
    """
    def __init__(self, value, value_type):
        self.value = value
        if value:
            msg = f"Expected {value_type} '{value}' not found in API response."
        super().__init__(msg)