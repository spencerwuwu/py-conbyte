def addBinary( s, in0, in1):
    words = [in0, in1]
    """
    :type s: str
    :type words: List[str]
    :rtype: List[int]
    """
    ls = len(s)
    word_ls = len(words[0])
    target_dict = {}
    for word in words:
        try:
            target_dict[word] += 1
        except KeyError:
            target_dict[word] = 1
    res = []
    for start in range(ls - word_ls * len(words) + 1):
        curr_dict = target_dict.copy()
        for pos in range(start, start + word_ls * len(words), word_ls):
            curr = s[pos:pos + word_ls]
            try:
                curr_dict[curr] -= 1
                if curr_dict[curr] < 0:
                    break
            except KeyError:
                break
        else:
            res.append(start)
    return res

