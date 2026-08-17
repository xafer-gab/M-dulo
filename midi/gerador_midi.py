from mido import MetaMessage, Message, MidiFile, MidiTrack
from random import randrange
import util.conv as conv

'''
Gerador de arquivo MIDI a partir de lista de listas com três parâmetros: 

            [[alt, dur, din], [alt, dur, din], ...]

Funções:
    track_midi ->  recebe lista de notas e retorna o objeto MidiTrack, que é uma voz
    arq_midi   ->  recebe uma lista de MidiTrack e retorna um objeto MidiFile, com todas as tracks
    grava_midi ->  grava o objeto MidiFile no disco
'''

def track_midi(alt_dur_din, comp_num=4, comp_den=4):
    track = MidiTrack()
    track.append(MetaMessage("time_signature", numerator=comp_num, denominator=comp_den))
    acc = 0
    for i, evt in enumerate(alt_dur_din):
        if evt[0] == 'pausa':
            acc += evt[1]
        else:
            track.append(Message('note_on', note=evt[0], velocity=evt[2], time=acc, channel=1))
            track.append(Message('note_off', note=evt[0], velocity=evt[2], time=evt[1], channel=1))
            acc = 0
    return track

def arq_midi(tracks):
    mid = MidiFile(type=1)
    for trk in tracks:
        mid.tracks.append(trk)
    return mid

def grava_midi(mido_obj, diretorio):
    titulo = randrange(1000, 9999)
    mido_obj.save(f"{diretorio}/{titulo}.mid")
    print(f" --- Arquivo MIDI '{titulo}.mid' gravado.")
    
#Função de execução
def exporta_midi(parametros: list, diretorio):
        
    #Produz listas de parâmetros
    alturas = parametros[0]
    duracoes = parametros[1]
    dinamicas = parametros[2]
    
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
        mido_trk.append(track_midi(trk))
        
    #Cria objeto mido e exporta
    mid = arq_midi(mido_trk)
    grava_midi(mid, diretorio)
