from mido import MetaMessage, Message, MidiFile, MidiTrack
from random import randrange

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
    for evt in alt_dur_din:
        track.append(Message('note_on', note=evt[0], velocity=evt[2], time=0, channel=1))
        track.append(Message('note_off', note=evt[0], velocity=evt[2], time=evt[1], channel=1))
    return track

def arq_midi(tracks):
    mid = MidiFile(type=1)
    for trk in tracks:
        mid.tracks.append(trk)
    return mid

def grava_midi(mido_obj, diretorio):
    titulo = randrange(1000, 9999)
    mido_obj.save(f"{diretorio}/{titulo}.mid")
