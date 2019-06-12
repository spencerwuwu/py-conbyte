
def do_numbers(a, b):
    d = 1 if a > b else -2
    if a > d:
        c = a + b
    else:
        c = a - b
    if c > 100:
        if a > b:
            return 0
        else:
            return 2
    else:
        return 1
    return c
