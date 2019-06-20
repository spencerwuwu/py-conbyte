import re   # pragma: no cover

def regex(string):
    """This function returns at least one matching digit."""
    #pattern = re.compile(r"\d+") # For brevity, this is the same as r"\d+"
    #pattern = re.compile(r"172\.1[6-9]\.")
    pattern = re.compile(r"ab+?")
    """
    result = pattern.match(string)
    if result:
        return  result.group()
    return None
    """

# Call our function, passing in our string
print(regex("007 James Bond"))   # pragma: no cover
