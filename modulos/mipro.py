import data.midi_part as data_midi

#Modulação intervalar progressiva (MIPRO)
def mipro(fundamental, inter_A, inter_B, n_linhas=1, comprimento=10):
    fund = data_midi.alt_classe[fundamental]
    intervalos = [inter_A, inter_B]
    
    arranjo = []
    c_linha = 0
    while n_linhas > 0:
        
        #Itera uma linha completa
        linha_lis = [fund]
        n1 = fund
        for i in range(comprimento):
            n1 = (n1 + inter_A) % 12
            n2 = (n1 + inter_B) % 12
            linha_lis.extend([n1, n2])
            n1 = n2
        arranjo.append(linha_lis)
        
        #Configura próxima iteração
        fund = (fund + intervalos[c_linha]) % 12
        c_linha = (c_linha + 1) % 2
        n_linhas -= 1
        
    return arranjo
