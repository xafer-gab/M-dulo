from random import randrange, choice
from modulos.alfabeto_serial import tradutor_texto_notas
from modulos.MIPRO import mipro
import modulos.series as serial
import data.midi_part as data_midi
import util.conv as conv
import midi.gerador_midi as midi

#Diretório para exportar midi
diretorio = "/dir"

#Fluxo imperativo de execução dos módulos
#Exemplo:
def exe_modulos():
    
    #Altura
    serie_alt = []
    inter = 1; comp = 20
    for i in range(4):
        s_alt = mipro("do", inter, 5, comprimento=comp)
        for e in s_alt[0]:
            oit = randrange(3, 5)
            serie_alt.append(f"{data_midi.int_class[e]}{oit}")
        inter += 1; comp -= 5
    
    #Duração e dinâmica    
    serie_dur = ["semicolcheia", "colcheia", "tercina_colcheia", "minima", "colcheia_p"]
    serie_din = ["f", "p", "mf", "fff"]
    
    #Rotaciona
    alturas, duracoes, dinamicas = serial.serie_rand_rotativa(
        serie_alt, 
        serie_dur, 
        serie_din, 
        n_notas=len(serie_alt), 
        fix_rot=[0, 1, 1]
        )
    
    #Bloco de retorno -> uma ou mais dimensões para cada parâmetro
    return alturas, duracoes, dinamicas

#Função de execução
def executa(diretorio):
        
    #Produz listas de parâmetros
    alturas, duracoes, dinamicas = exe_modulos()
    
    #Lida com número diferente de vozes
    tracks = []
    if type(alturas[0]).__name__ == "list":
        n_vozes = len(alturas)
        c = 0
        while c < n_vozes:
            tracks.append([alturas[c], duracoes[c], dinamicas[c]])
            c += 1
    else:
        tracks.append([alturas, duracoes, dinamicas])
        
    #Gera tracks MIDI    
    mido_trk = []
    for voz in tracks:
        trk = conv.nota_para_midi(voz[0], voz[1], voz[2])
        mido_trk.append(midi.track_midi(trk))
        
    #Cria objeto mido e exporta
    m = midi.arq_midi(mido_trk)
    midi.grava_midi(m, diretorio)

if __name__ == "__main__":
    executa(diretorio)

