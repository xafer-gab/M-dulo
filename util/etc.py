def iguala_maior(lis1, lis2):
    l_1 = []
    l_2 = []
    if len(lis1) > len(lis2):
        l_1 = lis1[:]
        c = 0; i = 0
        while c < len(lis1):
            l_2.append(lis2[i])
            i = (i + 1) % len(lis2)
            c += 1
    elif len(lis1) < len(lis2):
        l_2 = lis2[:]
        c = 0; i = 0
        while c < len(lis2):
            l_1.append(lis1[i])
            i = (i + 1) % len(lis1)
            c += 1
    else:
        l_1 = lis1[:]
        l_2 = lis2[:]
    
    return l_1, l_2
    
