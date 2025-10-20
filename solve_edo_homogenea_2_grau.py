import numpy as np
import matplotlib.pyplot as plt

def solve_edo_homo(coeficientes_entrada,cond_menos_um, cond_menos_dois):
    if(len(coeficientes_entrada)==2):

    # Resolve EDO homogênea discreta de 1ª ordem:
    # a1*y[n] + a0*y[n-1] = 0
        a1, a0 = coeficientes_entrada
        print(f"Equação característica: {a1}*gama + {a0} = 0")

        gama = -a0 / a1
        print(f"Raiz (gama): {gama:.4f}")

        if abs(gama) < 1:
            print("Sistema Estável")
        else:
            print("Sistema Instável")

   
        C = cond_menos_um / gama
        print(f"Constante C = {C:.4f}")

        # Solução geral
        print(f"Solução: y[n] = {C:.4f} * ({gama:.4f})^n , n >= 0")

        
        n = np.arange(0, 30)
        y = C * (gama**n)

        plt.stem(n, y)
        plt.title("Solução da EDO Homogênea de 1ª Ordem")
        plt.xlabel("n")
        plt.ylabel("y[n]")
        plt.grid(True)
        plt.show()

        return y
    elif(len(coeficientes_entrada)==3):
        print(f"eq de segundo grau:{coeficientes_entrada[0]}*gama^2 {coeficientes_entrada[1]}*gama {coeficientes_entrada[2]} ")

        delta=(coeficientes_entrada[1])**2-4*coeficientes_entrada[0]*coeficientes_entrada[2]
        print(f"delta={delta}")

        gama1=(-(coeficientes_entrada[1])-(delta**(1/2)))/(2*coeficientes_entrada[0])
        gama2=(-(coeficientes_entrada[1])+(delta**(1/2)))/(2*coeficientes_entrada[0])
        print(f"gama1: {gama1}")
        print(f"gama2: {gama2}")

        #Resolvendo sistema de equação pra achar as constantes
        A = np.array([[gama1**(-1), gama2**(-1)],
            [gama1**(-2), gama2**(-2)]])
        
        B = np.array([cond_menos_um, cond_menos_dois])

        constantes = np.linalg.solve(A, B)
        print(f"constantes:{constantes}")

        c1 = constantes[0]
        c2 = constantes[1]

        print(f"c1: {c1:.3f}")
        print(f"c2: {c2:.3f}")
    
        if(0<abs(gama1)<1 and 0<abs(gama1)<1):
            print("Sistema Estável")
        else:
            print("Sistema Instável")
        print(f"solução: {c1:.3f}*({gama1})^n + {c2:.3f}*({gama2})^n , n>=0")


        n = np.arange(0, 30)
        eq_resultado = c1 * (gama1**n) + c2 * (gama2**n)

        plt.stem(n,eq_resultado)
        plt.title("Solução da EDO de 2ª Ordem")
        plt.show()
        return eq_resultado



entrada=[1,-0.6,-0.16]

# entrada=[1,-0.6]
solve_edo_homo(entrada,0,25/4)