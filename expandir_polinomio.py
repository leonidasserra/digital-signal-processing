from sympy import symbols, expand, factor

x = symbols('x')
expr = (x - 2)*(x - 3)

print("Forma fatorada:", expr)
print("Forma expandida:", expand(expr))

