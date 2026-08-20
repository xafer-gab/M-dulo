import data.midi_part as midi_part
import random

#Modulação intervalar progressiva (MIPRO)

'''
MIPRO_MATRIZ
Gera matriz bi-intervalar a partir de fundamental.

--- Entrada
fundamental = 'do' (0); 
inter_A = 1; 
inter_B = 2;

--- Saída
[0, 1, 3, 4, ...]
'''
def mipro_matriz(fundamental: str, inter_A: int, inter_B: int, n_linhas=1, comprimento=10):
    fund = midi_part.alt_classe[fundamental]
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
        
    #Saída = Classe de Alturas    
    return arranjo

'''
MIPRO_CONJUNTO
Modula um conjunto harmônico a partir de uma lista de modulação por semitons.

--- Entrada
cjt_harmonico = ['do4', 'dos4', 'res4'] (série de alturas)
semitons = [1, -1]

--- Saída
['do4', 're4', 'res4']
'''
def mipro_conjunto(cjt_harmonico: list, semitons: list):
    
    #Converte para altura MIDI
    alturas_int = [midi_part.alt_midi[n] for n in cjt_harmonico]
    
    #Obtém os intervalos modulados
    intervalos_mod = []
    c = 0
    for i in range(len(alturas_int) - 1):
        inter_ori = alturas_int[i+1] - alturas_int[i]
        inter_mod = inter_ori + semitons[c]
        intervalos_mod.append(inter_mod)
        c += 1
        c = c % len(semitons)
        
    #Obtém a lista de intervalos de saída
    cjt_saida_midi = [alturas_int[0]]
    for i, inter in enumerate(intervalos_mod):
        altura = cjt_saida_midi[i] + inter
        cjt_saida_midi.append(altura)
    
    #Converte para nome de nota
    cjt_saida_notas = []
    for altura_midi in cjt_saida_midi:
        
        #Garante que a altura esteja no limite 12-119 (do0 a si8)
        while altura_midi > 119:
            altura_midi -= 12
        while altura_midi < 12:
            altura_midi += 12
            
        cjt_saida_notas.append(midi_part.midi_alt[altura_midi])
        
    return cjt_saida_notas
    
def mipro_cjt_gradual(cjt_harmonico: list, semitons: list, passos: int, modo="linear"):

    #Escala a lista de semitons para o cjt_harmonico
    n_intervalos = len(cjt_harmonico) - 1
    semitons_escalados = []
    c = 0
    for i in range(n_intervalos):
        semitons_escalados.append(semitons[c])
        c += 1
        c = c % len(semitons)
    
    #Passos
    inter_passo = n_intervalos / passos
    
    #Produz uma escala linear de modulação
    modulacoes = []
    acum = 0; idx = 0
    for i in range(passos):
        
        #Atualiza o acumulador de fase
        acum += inter_passo
        if abs(1.0 - acum) < 1e-7: #Arredonda decimal
            acum = 1.0
        acum_int = int(acum)
        
        #Modifica apenas os indices selecionados
        print(acum)
        secao_estado = [0 for _ in range(n_intervalos)]
        for i in range(acum_int):
            secao_estado[idx] = semitons_escalados[idx]
            idx += 1
            
        #Armazena estado 
        modulacoes.append(secao_estado[:])
        
        #Acumula o resto
        acum = acum - acum_int
            
    #Ordena a modulação conforme o tipo        
    if modo == "linear":
        pass
    elif modo == "aleatorio":
        random.shuffle(modulacoes)
    else:
        raise KeyError("Selecione um modo válido de disposição da modulação ('linear', 'aleatorio').")
    
    #Itera cada modulação
    saida_cjts = [cjt_harmonico[:]]; cjt_h = cjt_harmonico[:]
    for mods in modulacoes:
        print(mods)
        cjt_modulado = mipro_conjunto(cjt_h, mods)
        cjt_h = cjt_modulado[:]
        saida_cjts.append(cjt_modulado)
            
    return saida_cjts
