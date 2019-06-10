class GraniteException(Exception):
    """Base of all exceptions."""


class NodesUnavailable(GraniteException):
    """Either no nodes are currently active or all current nodes are not available"""


class InvalidCredientials(GraniteException):
    """Invalid credentials were passed"""


class HTTPException(GraniteException):
    """HTTP request failed"""
