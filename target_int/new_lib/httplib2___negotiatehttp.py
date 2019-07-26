def httplib2___negotiatehttp(recv):
    resp = recv.pop(0)
    while resp.find("\r\n\r\n") == -1 and len(recv) > 0:
        resp = resp + recv.pop(0)

    statusline = resp.splitlines()[0].split(" ", 2)
    if statusline[0] not in ["HTTP/1.0", "HTTP/1.1"]:
        return "Close"

    statuscode = int(statusline[1])
    if statuscode < 0:
        return "Error"

    if statuscode != 200:
        return "Close"

    return "Continue"

print(httplib2___negotiatehttp(["HTTP/1.1 200 Pa", "rtial content\nDate: Wed, 15 ", "Nov 1995 06:25:24 GMT\r\n\r\n"]))   # pragma: no cover
