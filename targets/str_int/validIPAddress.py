
# https://leetcode.com/problems/validate-ip-address/discuss/298894/Python3%3A-Simple-code-or-more-than-99-beats
def validIPAddress(IP: str) -> str:
    if '.' in IP:
        octa = IP.split('.')
        if len(octa) != 4:
            return "Neither"
        for i in octa:
            if not i.isdigit() or int(i) > 255 or( i[0] == '0' and len(i) > 1):
                return "Neither"
        return "IPv4"
    octa = IP.split(":")
    if len(octa) != 8:
        return "Neither"
    for i in octa:
        if len(i) > 4 or len(i) < 1:
            return "Neither"
        for val in i:
            if (val >= 'a' and val <= 'f') or (val >= 'A' and val <= 'F') or (val >= '0' and val <= '9'):
                continue
            else:
                return "Neither"
    return "IPv6"
