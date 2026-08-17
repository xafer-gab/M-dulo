from random import randrange
import data.midi_part as mp

def nota_para_midi(notas, duracoes, dinamicas, din_rand=True):
    
    #Verifica se as listas tem o mesmo número de elementos
    if not (len(notas) == len(duracoes) == len(dinamicas)):
        raise ValueError("As listas não possuem o mesmo número de elementos")
    
    #Traduz caracteres para números MIDI    
    notas_midi = []
    for i in range(len(notas)):

        #Altura
        if notas[i] == 'pausa':
            alt = notas[i]
        elif type(notas[i]) == str and notas[i] in mp.alt_midi:
            alt = mp.alt_midi[notas[i]]
        elif type(notas[i]) == float and notas[i] <= 1.0 and notas[i] >= 0:
            alt = int(notas[i] * 127) #Escala pelo espaço disponível de alturas
        elif type(notas[i]) == int and notas[i] <= 127 and notas[i] >= 0:
            alt = notas[i]
        else:
            raise ValueError(f'Os dados de altura são inadequados ao processamento. Índice = {i}; Valor = {notas[i]}')
        
        #Duração
        if type(duracoes[i]) == str and duracoes[i] in mp.duracoes:
            dur = mp.duracoes[duracoes[i]]
        elif type(duracoes[i]) == int and duracoes[i] >= 0:
            dur = duracoes[i]
        elif type(duracoes[i]) == float and duracoes[i] >= 0:
            dur = int(duracoes[i] * 480) #Escala pela semínima
        else:
            raise ValueError(f'Os dados de duração são inadequados ao processamento. Índice = {i}; Valor = {duracoes[i]}')
        
        #Dinâmica
        if type(dinamicas[i]) == str and dinamicas[i] in mp.dinamica:
            if din_rand:
                min_max_din = mp.dinamica[dinamicas[i]]
                din = randrange(min_max_din[0], min_max_din[1])
            else:
                din = mp.dinamica[dinamicas[i]][1]
        elif type(dinamicas[i]) == int and dinamicas[i] <= 127 and dinamicas[i] >= 0:
            if din_rand:
                din_max = dinamicas[i] + 10
                if din_max > 127: 
                    din_max = 127
                din = randrange(dinamicas[i], din_max)
            else:
                din = dinamicas[i]
        elif type(dinamicas[i]) == float and dinamicas[i] <= 1.0 and dinamicas[i] >= 0:
            din_escalado = int(dinamicas[i] * 127)
            if din_rand:
                din_max = din_escalado + 10
                if din_max > 127: 
                    din_max = 127
                din = randrange(din_escalado, din_max)
            else:
                din = din_escalado
        else:
            raise ValueError(f'Os dados de dinâmica são inadequados ao processamento. Índice = {i}; Valor = {dinamicas[i]}')
            
        #Anexa altura, duração e dinâmica
        notas_midi.append([alt, dur, din])

    #Retorna matriz com três parâmetros
    return notas_midi
