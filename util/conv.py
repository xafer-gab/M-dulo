from random import randrange
import data.midi_part as mp

def dinamica_rand(din):
    min_max_din = mp.dinamica[din]
    return randrange(min_max_din[0], min_max_din[1])

def nota_para_midi(notas, duracoes, dinamicas, din_rand=True):
    
    #Verifica se as listas tem o mesmo número de elementos
    if not (len(notas) == len(duracoes) == len(dinamicas)):
        raise ValueError("As listas não possuem o mesmo número de elementos")
    
    #Traduz caracteres para números MIDI    
    notas_midi = []
    for i in range(len(notas)):
        if din_rand:
            din = dinamica_rand(dinamicas[i])
        else:
            din = mp.dinamica[dinamicas[i]][1]
        notas_midi.append([
            mp.alt_midi[notas[i]], 
            mp.duracoes[duracoes[i]], 
            din
        ])

    #Retorna matriz com três parâmetros
    return notas_midi
        
            
        
        
