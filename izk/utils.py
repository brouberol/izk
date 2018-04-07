def bool_from_str(s):
    if s.isdigit():
        return bool(int(s))
    return s.lower() in ['yes', 'true']
