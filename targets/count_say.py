
# 038_Count_and_Say.py
def count_s(x):
    m = list(x)
    res = []
    m.append(None)
    i , j = 0 , 0
    while i < len(m) - 1:
        j += 1
        if m[j] != m[i]:
            # note j - i is the count of m[i]
            res += [j - i, m[i]]
            i = j
    return ''.join(str(s) for s in res)

def count_say(n):
    """
    :type n: int
    :rtype: str
    """
    if n == 1:
        return '1'
    x = '1'
    while n > 1:
        # each round, read itself
        x = count_s(x)
        n -= 1
    return x

print(count_say(1))
print(count_say(4))
