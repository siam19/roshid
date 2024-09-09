from typing import Optional

class RoshidError(Exception):
    #base error class for any errors inside of roshid
    pass

class RoshidAttributeError(RoshidError):
    def __init__(self, message):
        super().__init__(message)
