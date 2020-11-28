def try_parse_int(s, base=10, val=None):
    try:
        return int(s, base)
    except ValueError:
        return val
