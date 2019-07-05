def addStrings(num1, num2):
    """
    :type num1: str
    :type num2: str
    :rtype: str
    """
    if len(num1) == 0 :
        num1 = '0'
    if len(num2) == 0 :
        num2 = '0'
    res = []
    carry = 0
    ls = min(len(num1), len(num2))
    pos = -1
    while pos + ls >= 0:
        curr = int(num1[pos]) + int(num2[pos]) + carry
        res.insert(0, str(curr % 10))
        carry = int(curr / 10)
        pos -= 1
    while pos + len(num1) >= 0:
        curr = int(num1[pos]) + carry
        res.insert(0, str(curr % 10))
        carry = int(curr / 10)
        pos -= 1
    while pos + len(num2) >= 0:
        curr = int(num2[pos]) + carry
        res.insert(0, str(curr % 10))
        carry = curr / 10
        pos -= 1
    if carry != 0:
        res.insert(0, str(carry))

    ret = ""
    for r in res:
        ret += r

    l_len = max(len(num1), len(num2))
    if len(ret) > l_len:
        return True
    else:
        return False

print(addStrings("923", "123"))   # pragma: no cover
