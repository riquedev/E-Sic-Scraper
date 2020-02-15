class InvalidYear(Exception):
    """
    Generally used when the year is less than the year available.
    """
    pass

class InvalidFile(Exception):
    """
    The file is not compatible with the expected formats.
    """
    pass