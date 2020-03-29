#! /usr/bin/env python3
from pwn import *

def fibonacci(i):
    n1, n2 = 0, 1
    n = 0
    f = [0,1]

    while n < 50:
        nth = n1 + n2
        # update values
        n1 = n2
        n2 = nth
        f.append(n2)
        n += 1
    return f[i]

def decrypt(key, message):
    
    LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    translated = ''

    for symbol in message:
        if symbol in LETTERS:
            num = LETTERS.find(symbol)
            num = num + key
            if num > 25:
                num = num - len(LETTERS)
            translated = translated + LETTERS[num]
        else:
            translated = translated + symbol

    return translated

def modulos(n):
    if n > 26:
        j = n % 26
    else:
        j = n

    return j

r = remote('misc.2020.chall.actf.co', 20300)

a = 1
while a < 51:
    r.recvuntil('Shift ')
    p = r.recvuntil(' ') # Here is the message
    print('Message = '+str(p.strip()))
    r.recvuntil('by n=')
    n = r.recvuntil('\n') # Here is nth Fibonacci sequence number
    message = p.strip() # remove the trailing space

    k = fibonacci(int(n.strip())) # Determine the Fibonacci number
    l = modulos(k) # Check if the number is greater than 26
    m = decrypt(l,str(message)) # Decrypt the message
    m = str(m).strip('b').strip("'")
    r.send(m+'\n') # Send the decrypted message back

    a += 1
r.interactive()
