
def while_loop(a, b):
    i = 0
    j = 0
    cnt = 0
    while i < a:
        while j < b:
            cnt += 1
            j += 1
        i += 1

    return cnt
