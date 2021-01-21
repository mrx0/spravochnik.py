#!/usr/bin/env python3



print('Content-type: text/html')
print()
print('<h1>Hello world!</h1>')



a = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
b = {20, 3, 4, 23, 11, 17, 55, 8}

print('<p>A =', a)
print('<p>B =', b)
print('<p>Объединение Множеств A и B =', a | b)