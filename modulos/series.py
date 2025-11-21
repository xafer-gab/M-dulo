import random
from util import etc as ut_etc

#Filtra listas de alturas, durações e dinâmicas em séries do mesmo comprimento
def series_paralelas(serie_altura, serie_duracao, serie_dinamica, tipo="aumenta"):
    
    #Lista de de saída
    lis_alt = []
    lis_dur = []
    lis_din = []
    
    l_notas = len(serie_altura)
    l_duracoes = len(serie_duracao)
    l_dinamicas = len(serie_dinamica)
    
    #Alonga ou encurta séries
    if not (l_notas == l_duracoes == l_dinamicas):
        
        #Decide se a série é aumentada ou diminuída 
        if tipo == "aumenta":
            rev = True
        elif tipo == "diminui":
            rev = False
        else:
            raise ValueError("Parâmetros de tipo: 'aumenta' ou 'diminui' série")
        
        ordenado = sorted([l_notas, l_duracoes, l_dinamicas], reverse=rev)
        
        #Reconstrói ciclicamente as três séries
        c0 = 0; cA = 0; cB = 0; cC = 0
        while c0 < ordenado[0]:
            lis_alt.append(serie_altura[cA])
            lis_dur.append(serie_duracao[cB])
            lis_din.append(serie_dinamica[cC])
            cA = (cA + 1) % l_notas
            cB = (cB + 1) % l_duracoes
            cC = (cC + 1) % l_dinamicas
            c0 += 1
    
    #Copia e mantém o mesmo número de elementos
    else:
        lis_alt = serie_altura[:]
        lis_dur = serie_duracao[:]
        lis_din = serie_dinamica[:]
    
    #Retorna três listas ampliadas/diminuídas
    return lis_alt, lis_dur, lis_din
          
          
#Produz uma série a partir de uma lista de índices (ou outra série)            
def serializa_por_idx(serie_selecionada, serie_seletora, n_notas=10):
    
    #Certifica-se de que não há índices fora do limite
    selec_len = len(serie_selecionada)
    s_seletora = [v for v in serie_seletora if v < selec_len and v >= 0]
    
    s_saida = []
    c = 0; c_selet = 0; l = len(s_seletora)
    while c < n_notas:
        sele = serie_selecionada[s_seletora[c_selet]]
        s_saida.append(sele)
        c_selet = (c_selet + 1) % l
        c += 1
    return s_saida
    
#Gera uma combinação de séries rotativas fixas e seleções randômicas de uma série
#fix_rot = configuração de rotação e aleatoriedade (0 = aleatoriza; 1 = rotaciona)
def serie_rand_rotativa(serie_altura, serie_duracao, serie_dinamica, n_notas=10, fix_rot=[1, 0, 0]):
    
    #Comprimento de séries
    l_alt = len(serie_altura)
    l_dur = len(serie_duracao)
    l_din = len(serie_dinamica)
    
    lis_alt = []
    lis_dur = []
    lis_din = []
    
    #Iterações
    c = 0; cAlt = 0; cDur = 0; cDin = 0
    while c < n_notas:
        if fix_rot[0] == 1:
            lis_alt.append(random.choice(serie_altura))
        else:
            lis_alt.append(serie_altura[cAlt])
            cAlt = (cAlt + 1) % l_alt
        if fix_rot[1] == 1:
            lis_dur.append(random.choice(serie_duracao))
        else:
            lis_dur.append(serie_duracao[cDur])
            cDur = (cDur + 1) % l_dur
        if fix_rot[2] == 1:
            lis_din.append(random.choice(serie_dinamica))
        else:
            lis_din.append(serie_dinamica[cDin])
            cDin = (cDin + 1) % l_din
        c += 1
    
    return lis_alt, lis_dur, lis_din
