class BooleanParseException(Exception):
    pass


def parse_boolean(val):
    if str(val).lower() in ("yes", "y", "t", "true", "1"):
        return True
    elif str(val).lower() in ("no", "n", "f", "false", "0"):
        return False
    else:
        raise BooleanParseException("Cannot parse incoming boolean!")
