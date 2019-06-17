
# 067_Add_Binary

def add_binary(a, b):
    res = ''
    lsa, lsb = len(a), len(b)
    pos, plus, curr = -1, 0, 0
    # plus a[pos], b[pos] and curr % 2
    while (lsa + pos) >= 0 or (lsb + pos) >= 0:
        if (lsa + pos) >= 0:
            curr += int(a[pos])
        if (lsb + pos) >= 0:
            curr += int(b[pos])
        res = str(curr % 2) + res
        curr /= 2
        pos -= 1
    if curr == 1:
        res = '1' + res
    return res

print(add_binary("10111", "111"))   # pragma: no cover
