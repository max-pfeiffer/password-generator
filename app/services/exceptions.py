"""
Exceptions for Services
"""


class PasswordToShortError(Exception):
    """
    Exception which is raise in case the password is too short.
    """


class PasswordToLongError(Exception):
    """
    Exception which is raise in case the password is too long.
    """
