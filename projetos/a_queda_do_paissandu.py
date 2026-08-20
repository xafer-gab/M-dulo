import random
from util import edicao
from modulos.gerador_motivico import gerador_motivico_estocastico
from modulos.gerador_motivico import construtor_melodico

# ----- A queda do Paissandú -----
# --- para orquestra sinfônica ---
# ------------- 2026 -------------

# --- SEÇÃO A ---

def secao_A_F1():
    
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
    
    linhas = []
    for i in range(7):
        inst = [[],[],[]]
        for j, comp in enumerate(divisao_compassos):
            h = random.choice(harm)
            alt, dur = gerador_motivico_estocastico([0], [2.5], h[j], 2.0, comp*3, preenchimento[j], 0.25)
            inst[0].extend(alt)
            inst[1].extend(dur)
            for v in alt:
                inst[2].append(80)
        linhas.append(inst)
        
    return edicao.sobrepoe(linhas)
    
def secao_A_F2():
    
    linhas = []
    for i in range(2):
        inst = [[],[],[]]
        inst[0], inst[1] = gerador_motivico_estocastico([0], [6.0], ['do4'], 1.5, 26*3, 0.30, 0.25)
        for v in inst[0]:
            inst[2].append(80)
        linhas.append(inst)
    return edicao.sobrepoe(linhas)

# --- SEÇÃO B ---


    
# --- EXECUÇÃO ---

#Seção A, F1
A_F1 = secao_A_F1()
A_F2 = secao_A_F2()
