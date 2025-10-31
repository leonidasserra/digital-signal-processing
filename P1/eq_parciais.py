from sympy import symbols, apart

# 1. Definir a variável simbólica
x = symbols('x')

# 2. Definir a expressão
expressao = x**2 / (x**2 - 0.9*x + 0.9)

# 3. Decompor em frações parciais
fracoes_parciais = apart(expressao)

# 4. Imprimir o resultado
print(fracoes_parciais)