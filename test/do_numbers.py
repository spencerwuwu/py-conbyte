
def do_numbers(a, b):
    if a > 5:
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
