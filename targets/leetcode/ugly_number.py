
# 263_Ugly_Number

def ugly_number(num):
    if num <= 0:
        return False
    divisors = [2, 3, 5]
    for d in divisors:
        while num % d == 0:
            num /= d
    return num == 1

print(ugly_number(-2147483648))
print(ugly_number(8))
