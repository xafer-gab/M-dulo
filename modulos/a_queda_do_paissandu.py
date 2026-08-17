#from data.midi_part import alt_midi, midi_alt
#from modulos.series import serializa_por_idx
import random

# ----- A queda do Paissandú -----
# --- para orquestra sinfônica ---
# ------------- 2026 -------------

# Métodos desenvolvidos para a peça "A Queda do Paissandú" (2026)

''' 
Método 1 - Geração motívica com princípio estocástico

1. Parte-se de um modelo motívico (serie_alt, serie_dur).
2. Define-se um conjunto ordenado de alturas, ou modo (lis_modo).
3. A série de alturas é transposta por valor aleatório (max = len(lis_modo)) e, então, 
   é rotacionada utilizando-se o módulo relativo ao modo (idx % (max)).
4. A duração é escalada utilizando-se uma multiplicação (for v in serie_dur: v * razao).
5. Define-se a densidade de eventos em um número de tempos, gerados aleatoriamente com 
   probabilidades e, então, o gesto é encerrado no limite de densidade (truncado)
6. Distribui-se os objetos truncados no tempo total restante, considerando o número de espaços produzidos
   Espaços = len(objetos) + 1

Estrutura de dados 
    serie_alt = índices em inteiros
    serie_dur = float, sendo 1.0 = semínima
    lis_modo = str com nome de altura (alt_midi)
    n_tempos = int, sendo 1 = um tempo
    preenchimemento = float que estipula a porcentagem de preenchimento (0.0 a 1.0)
    quantizacao = aproximação do valor das pausas para os múltiplos de "q" (fusa, semicolcheia, etc).
'''
def gerador_motivico_estocastico(serie_alt, serie_dur, lis_modo, dur_escala: float, n_tempos, preenchimento, quantizacao):
    
    modo_idx_max = len(lis_modo)
    
    #Valida a adequação das séries
    if len(serie_alt) != len(serie_dur):
        raise ValueError(f"As séries de altura e duração não possuem o mesmo comprimento:\nlis_alt = {len(serie_alt)}\nlis_dur = {len(serie_dur)}")
    
    #Produz motivos que preencham inteiramente n_tempos
    lista_motivos = []; t = 0
    while t < n_tempos:
    
        #Transposição e repetição cíclica da série de alturas
        transposicao = random.randrange(0, modo_idx_max)
        serie_alturas = [(v + transposicao) % modo_idx_max for v in serie_alt]
        
        #Seleção de alturas do modo
        alturas_obj = []
        for v in serie_alturas:
            alt = lis_modo[v]
            alturas_obj.append(alt)
            
        #Escala as durações
        escala_ou_nao = random.random()
        if escala_ou_nao < 0.5:
            duracoes_obj = [v * dur_escala for v in serie_dur]
        else:
            duracoes_obj = serie_dur[:]
        
        #Armazena o objeto
        lista_motivos.append([alturas_obj, duracoes_obj])
        
        #Incrementa contador com a duração total do objeto
        t += sum(duracoes_obj)
        
    #Distribui os objetos no tempo e trunca os objetos excedentes
    #Calcula os tempos brutos
    tempos_tocados = int(preenchimento * n_tempos)
    tempos_pausa = n_tempos - tempos_tocados
    
    #Seleciona os motivos e trunca no limite
    objetos_selecionados = []
    acum_tempo = tempos_tocados
    for motivo in lista_motivos:
        dur_motivo = sum(motivo[1])
        
        #Adiciona objetos inteiros
        if dur_motivo <= acum_tempo:
            objetos_selecionados.append(motivo)
            acum_tempo -= dur_motivo
        
        #Trunca
        elif acum_tempo > 0:
            alturas_t = []
            duracoes_t = []
            i = 0
            for dur in motivo[1]:
                if acum_tempo <= 0:
                    break
                elif dur <= acum_tempo:
                    alturas_t.append(motivo[0][i])
                    duracoes_t.append(motivo[1][i])
                    acum_tempo -= dur
                    i += 1
                elif acum_tempo > 0:
                    t_truncado = acum_tempo
                    alturas_t.append(motivo[0][i])
                    duracoes_t.append(t_truncado)
                    acum_tempo -= t_truncado
           
            #Armazena o objeto truncado
            objetos_selecionados.append([alturas_t, duracoes_t])
        
        else:
            break
    
    #Define a tendência de distribuição das pausas
    n_pausas = len(objetos_selecionados) + 1
    distribuicao = []
    for i in range(n_pausas):
        distribuicao.append(random.random())
    
    #Normaliza a distribuição
    somatoria = sum(distribuicao)
    dist_norm = [v / somatoria for v in distribuicao]
    
    #Produz as durações
    duracoes = [v * tempos_pausa for v in dist_norm]
    
    #Quantiza e armazena
    duracoes_pausas = []
    t_pausas = tempos_pausa
    for dur in duracoes:
        pausa = round(dur / quantizacao) * quantizacao
        if pausa <= t_pausas:
            duracoes_pausas.append(pausa)
            t_pausas -= pausa
        elif t_pausas > 0:
            duracoes_pausas.append(t_pausas)
        else:
            duracoes_pausas.append(0)
        
    #Randomiza novamente para distribuir pausas nulas (i.e. motivos concatenados sem pausa)
    random.shuffle(duracoes_pausas)
    
    #Produz a sequência de saída com motivos espaçados por pausas
    saida = [[],[]]
    elementos_combinados = n_pausas + len(objetos_selecionados)
    idx_p = 0; idx_n = 0
    for i in range(elementos_combinados):
        if i % 2 == 0:
            #Não adiciona pausas nulas
            if not duracoes_pausas[idx_p] == 0:
                saida[0].append('pausa') #pausa = do0
                saida[1].append(duracoes_pausas[idx_p])
            idx_p += 1
        else:
            saida[0].extend(objetos_selecionados[idx_n][0])
            saida[1].extend([float(v) for v in objetos_selecionados[idx_n][1]]) #força tipagem na saída
            idx_n += 1
    
    
    #Garante que não faltou tempos na saída, e adiciona pausas
    tempo_total = sum(saida[1])

    if tempo_total < n_tempos:
        #Adiciona uma pausa no final
        saida[0].append('pausa')
        saida[1].append(n_tempos - tempo_total)
    
    #Retorna o segmentos completo
    return saida[0], saida[1]

'''
modo = ['a', 'b', 'c']
serie_alt = [0, 1, 2]
serie_dur = [0.25, 0.5, 1.0]
preenchimento = 0.99

print("preenchimento: "+ str(preenchimento))

for i in range(4):
    print(gerador_motivico_estocastico(serie_alt, serie_dur, modo, 2.0, 20, preenchimento, 0.5))
'''

'''
Método 4 - Miscigenação Serial
Duas séries podem ser miscigenadas, produzindo uma nova série única. Para isso, um
fragmento de cada série — como um código genético — são combinados estocasticamente

1. Obtém-se o tamanho médio de duas séries escolhidas. Isso é obtido por média simples arredondada.
   O valor obtido será o tamanho da nova série.
2. É gerada uma porcentagem aleatória de mistura, assim como uma porcentagem aleatória de variação espontânea.
3. Segmentos aleatórios (contíguos) são selecionados das séries progenitoras, bem como uma sequência aleatória
   de variação. Estes segmentos são justapostos em ordem aleatória
'''

def miscigenacao_serial(serie_a: list, serie_b: list):
    
    #Determina o tamanho médio
    comp_medio = (len(serie_a) + len(serie_b)) // 2
    
    #Valor aleatório de mistura e mutação
    mistura_a = random.uniform(0.4, 0.6)
    mistura_b = random.uniform(0.4, 0.6)
    variacao = random.uniform(0.1, 0.2)
    
    #Normaliza os valores
    norm = mistura_a + mistura_b + variacao
    mistura_norm = [mistura_a/norm, mistura_b/norm, variacao/norm]
    
    #Escala para o tamanho da série
    selecao = [round(peso * comp_medio) for peso in mistura_norm]
    
    #Garante o tamanho correto na saída
    i = 2
    while sum(selecao) != comp_medio:
        if sum(selecao) > comp_medio:
            selecao[i] -= 1
        else:
            selecao[i] += 1
        i -= 1
        if i < 0: i = 2
    
    #Seleciona um fragmento das séries progenitoras
    #Serie A
    frag_a = []
    idx_a = random.randrange(0, len(serie_a))
    for _ in range(selecao[0]):
        idx_a = idx_a % len(serie_a)
        frag_a.append(serie_a[idx_a] % comp_medio)
        idx_a += 1
        
    #Serie B
    frag_b = []
    idx_b = random.randrange(0, len(serie_b))
    for _ in range(selecao[1]):
        idx_b = idx_b % len(serie_b)
        frag_b.append(serie_b[idx_b] % comp_medio)
        idx_b += 1
        
    #Variação
    frag_var = []
    for _ in range(selecao[2]):
        frag_var.append(random.randrange(0, comp_medio))
        
    #Mistura fragmentos
    fragmentos = [frag_a, frag_b, frag_var]
    random.shuffle(fragmentos)
    
    #Concatena a nova série
    serie_descendente = []
    for frag in fragmentos:
        try:
            for v in frag:
                serie_descendente.append(v)
        except:
            pass
            
    return serie_descendente
        
def progenitura(series, tipo='casais', n_desc=2, n_geracoes=2):
    n_series = len(series)
    
    #Verifica se o conjunto forma casais
    if tipo == 'casais':
        if n_series % 2 != 0 or n_series == 0:
            raise ValueError(f"O número de séries não forma pares. Número de séries: {n_series}.")

        #Gera prole, sempre fazendo cruzamento entre "primos/as"
        prole = [series[:]]
        for i in range(n_geracoes):
            nova_geracao = []
            c = 0
            for r in range(len(prole[i]) // 2):
                s1 = prole[i][c]
                if i == 0:
                    s2 = prole[i][c + 1]
                    c += 2
                else:
                    s2 = prole[i][c + 2]
                    c += 1
                for _ in range(n_desc):
                    nova_geracao.append(miscigenacao_serial(s1, s2))
            prole.append(nova_geracao)
    
    #Faz misturas sem restrição de cruzamento
    elif tipo == 'orgia':
        prole = [series[:]]
        random.shuffle(prole[0])
        for i in range(n_geracoes):
            nova_geracao = []
            c = 0
            for r in range(len(prole[i]) // 2):
                s1 = prole[i][c]
                s2 = prole[i][c + 1]
                c += 2
                for _ in range(n_desc):
                    nova_geracao.append(miscigenacao_serial(s1, s2))
            random.shuffle(nova_geracao)
            prole.append(nova_geracao)
                
    return prole 
                
# --- BLOCO DE TESTE ---
if __name__ == "__main__":
    # Definindo séries iniciais (índices de referência)
    Serie1 = [5, 4, 0, 3, 2, 2, 12, 1, 3, 2, 5, 5, 10]
    Serie2 = [4, 8, 9, 8, 6, 11, 6, 5, 3, 0, 1, 0, 10]
    Serie3 = [4, 6, 2, 10, 6, 5, 4, 1, 1, 0, 8, 9, 1]
    Serie4 = [9, 9, 8, 9, 8, 6, 11, 2, 4, 6, 5, 3, 0]
    
    ancestrais = [Serie1, Serie2, Serie3, Serie4]
    
    print("--- INÍCIO DO TESTE DE PROGENITURA ---")
    arvore_genealogica = progenitura(ancestrais, tipo='orgia', n_desc=2, n_geracoes=4)
    
    for idx_gen, geracao in enumerate(arvore_genealogica):
        print(f"\n[Geração {idx_gen+4}]:")
        for idx_serie, serie in enumerate(geracao):
            print(f"  Série {idx_serie + 1}: {serie}")

                
            
        
    

        
        
            


    
