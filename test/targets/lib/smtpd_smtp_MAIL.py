"""
For:
    arg = _strip_command_keyword('FROM:', arg)
"""
def _strip_command_keyword(keyword, arg):
    keylen = len(keyword)
    if arg[:keylen].upper() == keyword:
        return arg[keylen:].strip()
    return ''



""" 
For:
    address, params = self._getaddr(arg)
"""
def get_angle_addr(value):
    """ angle-addr = [CFWS] "<" addr-spec ">" [CFWS] / obs-angle-addr
        obs-angle-addr = [CFWS] "<" obs-route addr-spec ">" [CFWS]

    """

def _getaddr(arg):
    if not arg:
        return '', ''
    if arg.lstrip().startswith('<'):
        address, rest = get_angle_addr(arg)
    else:
        address, rest = get_addr_spec(arg)
    if not address:
        return address, rest
    return address.addr_spec, rest





def smptd_smtp_MAIL(arg):
    async_chat = ""
    syntaxerr = '501 Syntax: MAIL FROM: <address>'

    if len(arg) == 0:
        async_chat += syntaxerr
        return async_chat

    arg = _strip_command_keyword('FROM:', arg)
    address, params = self._getaddr(arg)
