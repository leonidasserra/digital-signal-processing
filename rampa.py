def rampa(n):
    array=[]
    for i in range (2*n+1):
        if(i>=n):
            array.append(i-n)
            
        else:
            array.append(0)
    return array

print(rampa(1))
print(rampa(2))
print(rampa(3))

