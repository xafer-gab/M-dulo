from data.midi_part import alt_lis, alt_classe, oit_lis
import random

alfabeto = "abcdefghijklmnopqrstuvxyz"

def dc_alfabeto(fundamental, min_oit, max_oit):
    
    oitavas = oit_lis[min_oit:max_oit+1]
    notas = []
    
    c = alt_classe[fundamental]
    while len(notas) < len(alfabeto):
        nt = alt_lis[c]
        r_oit = str(random.choice(oitavas))
        notas.append(nt + r_oit)
        if c == len(alt_lis)-1:
            c = 0
        else:
            c += 1
    
    dici_alt = {}
    for letra, nota in zip(alfabeto, notas):
        dici_alt[letra] = nota
        
    return dici_alt

def texto_alturas(texto, alfabeto_serial):
    texto = texto.lower()
    return [alfabeto_serial[caractere] for caractere in texto if caractere in alfabeto_serial]

def tradutor_texto_notas(texto, fundamental="do", min_oit=4, max_oit=4):
    dicionario = dc_alfabeto(fundamental, min_oit, max_oit)
    return texto_alturas(texto, dicionario)
