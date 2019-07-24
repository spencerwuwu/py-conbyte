
def email__header_value_parser(value):
    if len(value) == 0:
        return 0

    CFWS_LEADER = " \t("
    digits = ''
    while len(value) != 0 and value[0] != '.' and value not in CFWS_LEADER:
        digits += value[0]
        value = value[1:]

    if not digits.isdigit():
        return 0
    else:
        major = int(digits)

    if len(value) != 0 and value[0] != '.':
        return str(major)

    value = value[1:]

    if len(value) == 0:
        return str(major)

    digits = ''
    while len(value) != 0 and value[0] != '.' and value not in CFWS_LEADER:
        digits += value[0]
        value = value[1:]

    if not digits.isdigit():
        return 0
    else:
        minor = int(digits)

    return str(major) + "." + str(minor)

print(email__header_value_parser("2.15"))   # pragma: no cover
