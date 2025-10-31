from impulse import impulse
from funcao_atraso import atraso


def media_movel(array,unidades):
    
    newarray=[0]*len(array)
    for k in range(unidades):
        arrayatraso = atraso(array, k)
        for i in range(len(array)):
            newarray[i] += arrayatraso[i]
    for i in range(len(newarray)):
        newarray[i]=newarray[i]/unidades

    return newarray



# def media_movel(array, unidades):
#     newarray = []
#     for k in range(unidades):
#         arrayatraso = atraso(array, k)
#         for i in range(len(array)):
#             if i >= unidades - 1:  # Só calcula quando janela está completa
#                 if k == 0:
#                     newarray.append(0)
#                 newarray[i - unidades + 1] += arrayatraso[i]
    
#     # Divide pela quantidade de unidades
#     for i in range(len(newarray)):
#         newarray[i] = newarray[i] / unidades
    
#     return [None] * (unidades - 1) + newarray  # NaN nas primeiras posições

x=[1,2,3,4,5]
print(media_movel(x,3))