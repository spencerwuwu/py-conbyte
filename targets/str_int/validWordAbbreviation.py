# 408_Valid_Word_Abbreviation.py
def validWordAbbreviation( word, abbr):
    pos = curr = 0
    for i in range(len(abbr)):
        if abbr[i].isdigit():
            num = int(abbr[i])
            if num == 0 and curr == 0:
                return False
            curr = curr * 10 + num
        else:
            pos += curr
            curr = 0
            if pos >= len(word):
                return False
            if word[pos] != abbr[i]:
                return False
            pos += 1
    pos += curr
    if pos == len(word):
        return True
    return False
    
