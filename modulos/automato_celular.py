from data.midi_part import alt_midi, midi_alt
import random

#O autômato celular é regido por regras que definem um princípio gerativo
#Neste caso, utilizaremos dois princípios aplicados a qualquer sequência de n alturas:
#
#1. Caso as alturas adjacentes estejam dentro de uma oitava, salta o intervalo em direção aleatória
#2. Caso alguma das alturas adjacentes esteja distante mais de uma oitava, salta em direção ao intervalo mais distante

def automato_celular(seq_ini_alt, n_iteracoes, inter_padrao=7, lim_inf=48, lim_sup=84):
    seq_midi = [alt_midi[alt] for alt in seq_ini_alt]
    seq_out = [midi_alt[alt] for alt in seq_midi] 
    n_ele = len(seq_midi)
    for vezes in range(n_iteracoes):
        seq_mod = []
        for i in range(n_ele):
            inter_esq = seq_midi[i]-seq_midi[i-1]
            inter_dir = seq_midi[i]-seq_midi[(i+1) % n_ele]
            if inter_esq >= 12 or inter_dir >= 12:
                alt = seq_midi[i]-inter_padrao
            elif inter_esq <= -12 or inter_dir <= -12:
                alt = seq_midi[i]+inter_padrao
            else:
                if random.randrange(0, 2) == 0:
                    alt = seq_midi[i]+inter_padrao
                else:
                    alt = seq_midi[i]-inter_padrao
            #Ajusta para o limite de oitavas
            if alt <= lim_inf:
                alt+=12
            elif alt >= lim_sup:
                alt-=12 
            seq_mod.append(alt)
        #Converte midi > nota
        seq_out.extend([midi_alt[alt] for alt in seq_mod])
        #Atualiza lista para novo estado
        seq_midi = seq_mod[:]
    return seq_out



