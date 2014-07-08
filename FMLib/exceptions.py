class MultipleObjectsReturned(Exception):
    pass


class FMActionException(Exception):
    pass


class ZeroObjectsReturned(FMActionException):
    pass


class FMConversionException(Exception):
    pass