import random
from modulos import a_queda_do_paissandu as paissandu

def exe_modulos():
    
    alturas = []
    duracoes = []
    dinamicas = []
    
    a1_a = ['re4', 'res4', 'mi4', 'fas4', 'sols4', 'la4', 'las4', 'do5']
    a1_b = ['sol4', 'sols4', 'la4', 'si4', 'dos5', 're5', 'res5', 'fa5']
    a2_a = ['re4', 'res4', 'mi4', 'fas4', 'sol4', 'sols4', 'la4', 'si4']
    a2_b = ['sol4', 'sols4', 'la4', 'si4', 'do5', 'dos5', 're5', 'mi5']
    a3_a = ['re4', 'res4', 'mi4', 'fas4', 'sol4', 'sols4', 'la4', 'las4']
    a3_b = ['sol4', 'sols4', 'la4', 'si4', 'do5', 'dos5', 're5', 'res5']
    a4_a = ['sol4', 'sols4', 'la4', 'las4', 'si4', 'do5', 'dos5', 're5']
    a4_b = ['re4', 'res4', 'mi4', 'fa4','fas4', 'sol4', 'sols4', 'la4']
    
    divisao_compassos = [2] * 13
    preenchimento = [0.16, 0.32, 0.48, 0.64, 0.8, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]
    harm = [[a1_a, a1_a, a1_a, a1_a, a1_a, a2_a, a2_a, a2_a, a2_a, a3_a, a3_a, a4_a, a4_a], 
        [a1_b, a1_b, a1_b, a1_b, a1_b, a2_b, a2_b, a2_b, a2_b, a3_b, a3_b, a4_b, a4_b]]
    
    for i in range(7):
        inst = [[],[],[]]
        for j, comp in enumerate(divisao_compassos):
            h = random.choice(harm)
            alt, dur = paissandu.gerador_motivico_estocastico([0], [2.5], h[j], 2.0, comp*3, preenchimento[j], 0.25)
            inst[0].extend(alt)
            inst[1].extend(dur)
            for v in alt:
                inst[2].append(80)
        alturas.append(inst[0])
        duracoes.append(inst[1])
        dinamicas.append(inst[2])
    
    #Bloco de retorno -> uma ou mais dimensões para cada parâmetro
    return alturas, duracoes, dinamicas
