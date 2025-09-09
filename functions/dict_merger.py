def merge_dicts(dest, new):
    for key, value in new.items():
        if key in dest and isinstance(dest[key], dict) and isinstance(value, dict):
            merge_dicts(dest[key], value)
        elif key in dest and isinstance(dest[key], str) and isinstance(value, str):
            dest[key] += " " + value
        else:
            dest[key] = value
    return dest