from sympy import symbols, apart, simplify, factor, degree, div, Poly, cancel, S, Add
from sympy.parsing.sympy_parser import parse_expr
from fractions import Fraction

def extrair_fracoes(expr, var):
    """
    Extrai as frações individuais de uma expressão decomposta.
    
    Retorna uma lista de dicionários com numerador e denominador de cada fração.
    """
    fracoes = []
    
    # Se a expressão é uma soma, separa os termos
    if isinstance(expr, Add):
        termos = expr.as_ordered_terms()
    else:
        termos = [expr]
    
    for termo in termos:
        numer, denom = termo.as_numer_denom()
        if denom != 1:
            fracoes.append({
                'numerador': numer,
                'denominador': denom,
                'fracao': termo
            })
        else:
            # É um termo polinomial, não uma fração
            fracoes.append({
                'numerador': numer,
                'denominador': 1,
                'fracao': termo,
                'eh_polinomial': True
            })
    
    return fracoes

def decomposicao_fracao_parcial(expressao=None, numerador=None, denominador=None, variavel='x', racional=False):
    """
    Decompõe uma fração racional em frações parciais.
    
    Parâmetros:
    -----------
    expressao : str, opcional
        Expressão completa como string (ex: "(2*x + 3)/(x**2 - 1)")
    numerador : str, opcional
        Numerador da fração como string
    denominador : str, opcional
        Denominador da fração como string
    variavel : str, padrão 'x'
        Variável da expressão
    racional : bool, padrão False
        Se True, converte decimais para frações racionais
    
    Retorna:
    --------
    dict : Dicionário com informações da decomposição
        - 'original': expressão original
        - 'simplificada': expressão simplificada (se aplicável)
        - 'parte_polinomial': parte polinomial (se grau num >= grau den)
        - 'decomposicao': decomposição em frações parciais
        - 'resultado_completo': resultado final completo
    
    Exemplos:
    ---------
    >>> resultado = decomposicao_fracao_parcial("(2*x + 3)/(x**2 - 1)")
    >>> resultado = decomposicao_fracao_parcial(numerador="x + 1", denominador="x**2 - 1")
    >>> resultado = decomposicao_fracao_parcial("(x**2)/(x**2 - 0.9*x + 0.9)")
    """
    
    # Define a variável simbólica
    var = symbols(variavel)
    
    # Parse da entrada
    try:
        if expressao is not None:
            if racional:
                # Substitui decimais por frações antes do parse
                import re
                expressao_proc = expressao
                decimais = re.findall(r'\d+\.\d+', expressao)
                for decimal in decimais:
                    frac = Fraction(decimal).limit_denominator()
                    expressao_proc = expressao_proc.replace(decimal, f"({frac.numerator}/{frac.denominator})")
                expr = parse_expr(expressao_proc, local_dict={variavel: var})
            else:
                expr = parse_expr(expressao, local_dict={variavel: var})
            numer, denom = expr.as_numer_denom()
        elif numerador is not None and denominador is not None:
            if racional:
                # Substitui decimais por frações
                import re
                num_proc = numerador
                den_proc = denominador
                for texto in [numerador, denominador]:
                    decimais = re.findall(r'\d+\.\d+', texto)
                    for decimal in decimais:
                        frac = Fraction(decimal).limit_denominator()
                        num_proc = num_proc.replace(decimal, f"({frac.numerator}/{frac.denominator})")
                        den_proc = den_proc.replace(decimal, f"({frac.numerator}/{frac.denominator})")
                numer = parse_expr(num_proc, local_dict={variavel: var})
                denom = parse_expr(den_proc, local_dict={variavel: var})
            else:
                numer = parse_expr(numerador, local_dict={variavel: var})
                denom = parse_expr(denominador, local_dict={variavel: var})
            expr = numer / denom
        else:
            raise ValueError("Forneça 'expressao' ou 'numerador' e 'denominador'")
    except Exception as e:
        return {"erro": f"Erro ao fazer parse da expressão: {e}"}
    
    # Validações
    if denom == 0:
        return {"erro": "Denominador não pode ser zero"}
    
    # Converte para polinômios para análise
    try:
        poly_num = Poly(numer, var)
        poly_den = Poly(denom, var)
    except Exception as e:
        return {"erro": f"Erro ao processar como polinômio: {e}"}
    
    # Cancela fatores comuns (simplificação)
    expr_simplificada = cancel(expr)
    numer_simp, denom_simp = expr_simplificada.as_numer_denom()
    
    # Verifica os graus após simplificação
    try:
        grau_num = degree(numer_simp, var)
        grau_den = degree(denom_simp, var)
    except Exception:
        # Se não conseguir determinar o grau, assume 0
        grau_num = 0 if numer_simp.is_number else -1
        grau_den = 0 if denom_simp.is_number else -1
    
    # Verifica se grau é None (constante)
    if grau_num is None:
        grau_num = 0
    if grau_den is None:
        grau_den = 0
    
    parte_polinomial = S.Zero
    numer_para_decompor = numer_simp
    denom_para_decompor = denom_simp
    
    # Se grau do numerador >= grau do denominador, faz divisão polinomial
    if grau_num >= grau_den and grau_den >= 0:
        try:
            quociente, resto = div(numer_simp, denom_simp, var)
            parte_polinomial = quociente
            numer_para_decompor = resto
        except Exception as e:
            # Se falhar, tenta sem divisão
            parte_polinomial = S.Zero
            numer_para_decompor = numer_simp
    
    # Decomposição em frações parciais
    if numer_para_decompor != 0 and denom_para_decompor != 0:
        fracao_para_decompor = numer_para_decompor / denom_para_decompor
        try:
            # Usa full=True para decomposição completa
            decomposicao = apart(fracao_para_decompor, var, full=True)
        except Exception as e:
            # Se apart falhar, tenta simplificar
            try:
                decomposicao = simplify(fracao_para_decompor)
            except:
                decomposicao = fracao_para_decompor
    else:
        decomposicao = S.Zero
    
    # Extrai as frações individuais
    fracoes_individuais = extrair_fracoes(decomposicao, var)
    
    # Resultado completo
    if parte_polinomial != S.Zero:
        resultado_completo = simplify(parte_polinomial + decomposicao)
    else:
        resultado_completo = decomposicao
    
    # Fatora o denominador para mostrar informações úteis
    try:
        denom_fatorado = factor(denom_simp)
    except:
        denom_fatorado = denom_simp
    
    # Monta o dicionário de retorno
    resultado = {
        'original': expr,
        'original_str': f"({numer})/({denom})",
        'simplificada': expr_simplificada,
        'simplificada_str': f"({numer_simp})/({denom_simp})",
        'denominador_fatorado': denom_fatorado,
        'grau_numerador': grau_num,
        'grau_denominador': grau_den,
        'precisou_divisao': grau_num >= grau_den and grau_den >= 0,
        'parte_polinomial': parte_polinomial if parte_polinomial != S.Zero else None,
        'decomposicao': decomposicao,
        'resultado_completo': resultado_completo,
        'houve_simplificacao': expr != expr_simplificada
    }
    
    return resultado


def exibir_resultado(resultado):
    """
    Exibe o resultado da decomposição de forma formatada.
    
    Parâmetros:
    -----------
    resultado : dict
        Dicionário retornado pela função decomposicao_fracao_parcial
    """
    if 'erro' in resultado:
        print(f"❌ ERRO: {resultado['erro']}")
        return
    
    print("=" * 60)
    print("DECOMPOSIÇÃO EM FRAÇÕES PARCIAIS")
    print("=" * 60)
    print(f"\n📋 Expressão original:")
    print(f"   {resultado['original_str']}")
    
    if resultado['houve_simplificacao']:
        print(f"\n📝 Expressão simplificada:")
        print(f"   {resultado['simplificada_str']}")
    
    print(f"\n🔍 Informações:")
    print(f"   Denominador fatorado: {resultado['denominador_fatorado']}")
    print(f"   Grau do numerador: {resultado['grau_numerador']}")
    print(f"   Grau do denominador: {resultado['grau_denominador']}")
    
    if resultado['precisou_divisao']:
        print(f"\n⚠️  Grau do numerador ≥ grau do denominador")
        print(f"   Foi necessária divisão polinomial!")
        print(f"\n📐 Parte polinomial:")
        print(f"   {resultado['parte_polinomial']}")
    
    print(f"\n✨ Decomposição em frações parciais:")
    print(f"   {resultado['decomposicao']}")
    
    if resultado['parte_polinomial']:
        print(f"\n🎯 Resultado completo:")
        print(f"   {resultado['resultado_completo']}")
    
    print("\n" + "=" * 60)


# # Exemplos de uso
# if __name__ == "__main__":
#     # Exemplo 1: Caso clássico
#     print("\n🔷 EXEMPLO 1: Caso clássico")
#     resultado1 = decomposicao_fracao_parcial("(2*x + 3)/(x**2 - 1)")
#     exibir_resultado(resultado1)
    
#     # Exemplo 2: Caso com decimais
#     print("\n🔷 EXEMPLO 2: Caso com coeficientes decimais")
#     resultado2 = decomposicao_fracao_parcial("(x**2)/(x**2 - 0.9*x + 0.9)")
#     exibir_resultado(resultado2)
    
#     # Exemplo 3: Grau do numerador maior que denominador
#     print("\n🔷 EXEMPLO 3: Grau numerador > denominador")
#     resultado3 = decomposicao_fracao_parcial("(x**3 + 2*x**2 + 3)/(x**2 - 1)")
#     exibir_resultado(resultado3)
    
#     # Exemplo 4: Com frações exatas (usando racional=True)
#     print("\n🔷 EXEMPLO 4: Conversão para frações racionais")
#     resultado4 = decomposicao_fracao_parcial("(x**2)/(x**2 - 0.9*x + 0.9)", racional=True)
#     exibir_resultado(resultado4)

from sympy import apart, symbols

# Exemplo
x = symbols('x')
expressao = (8*x - 19) / (x**2 -5*x + 6)  #(colcoar o denominador comouma expressão inteira, sem multiplicação de polinomios)
# expressao = (x + 1) / (x**2 - 1)
resultado = apart(expressao, x)
print(resultado)