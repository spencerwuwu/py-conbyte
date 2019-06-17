
def simplify_path(path):
    result = []
    plist = path.split('/')
    for pos in plist:
        if pos:
            if pos == '..':
                try:
                    # up one level
                    result.pop()
                except:
                    # arrive top level
                    result = []
            elif pos != '.':
                result.append(pos)
    return '/'+'/'.join(result)

print(simplify_path("../../a/../../bcd/ef"))    # pragma: no cover
