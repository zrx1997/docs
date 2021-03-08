import random
def yanzhengma():
    strvar = ""
    for i in range(4):
        s_char = chr(random.randrange(97, 123))
        b_char = chr(random.randrange(65, 91))
        num = str(random.randrange(10))
        lst = [s_char, b_char, num]
        strvar += random.choice(lst)
    return strvar

res = yanzhengma()
print(res)
