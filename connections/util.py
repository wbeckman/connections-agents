


def _upper_recursively(arg):
    """
    Function to recursively upper any combination of lists,
    dictionaries, and strings.
    """
    new_arg = arg
    if arg and isinstance(arg, str):
        new_arg = arg.upper()
    if isinstance(arg, list):
        new_arg = []
        for elt in arg:
            new_arg.append(_upper_recursively(elt))
    if isinstance(arg, dict):
        new_arg = {}
        for k,v in arg.items():
            new_arg[_upper_recursively(k)] = _upper_recursively(v)

    return new_arg


def upper_input(func):
    """
    Turns all strings and lists of strings passed as params to uppercase.
    Intended for use as a decorator.

    This is slow because it copies all of the input arguments and iterates
    to their lowest nested levels, but for small inputs, it's an easy way to
    enforce capitalization.
    """
    def wrapper(*args, **kwargs):
        new_args = []
        for arg in args:
            new_arg = _upper_recursively(arg)
            new_args.append(new_arg)
        return func(*tuple(new_args), **kwargs)
    return wrapper
