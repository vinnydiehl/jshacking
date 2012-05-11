from os import urandom
open('key.pvt', 'w+').write(urandom(24).encode('string-escape'))
