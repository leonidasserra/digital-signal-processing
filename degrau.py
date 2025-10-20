def degrau(n):
    array=[]
    for i in range (2*n+1):
        if(i>=n):
            array.append(1)
            
        else:
            array.append(0)
    return array

print(degrau(1))
print(degrau(3))

