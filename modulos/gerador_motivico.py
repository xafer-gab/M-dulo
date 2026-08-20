import random

# Método desenvolvido para a peça "A Queda do Paissandú" (2026)

''' 
Geração motívica com princípio estocástico

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
    
- Método desenvolvido para a peça "A Queda do Paissandú" (2026)
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
    return saida[0], saida[1] #Altura, duração

'''
Construtor melódico

Produz melodias de n tempos a partir da permutação de figuras rítmicas selecionadas,
intercaladas com notas longa, assim como quantização específica por figura.

- Método desenvolvido para a peça "A Queda do Paissandú" (2026)
'''
def construtor_melodico(harm, serie, fig_lis, duracao, prob_nota_longa=0.6):
    
    #Lista de figuras rítmicas [0] = fig; [1] = quantização requerida
    figuras_totais = [
        [[0.125, 0.125, 0.125, 0.125], [0.25]], #0 = Fusas
        [[0.167, 0.167, 0.166], [0.5]],         #1 = Sextina
        [[0.2, 0.2, 0.2, 0.2, 0.2], [1.0]],     #2 = Quintina
        [[0.25, 0.25, 0.25], [0.25]],           #3 = Semicolcheias
        [[0.33, 0.33, 0.33], [1.0]],            #4 = Tercinas
        [[0.75, 0.25], [0.25]],                 #5 = Pontuada
        [[4], [0.5]]                            #6 = Nota longa
    ]
    
    #Seleciona as figuras
    figuras = [figuras_totais[idx] for idx in fig_lis]
    
    #Valida a adequação das séries
    if len(harm) <= max(serie):
        raise ValueError(
        "A série de alturas possue valores incompatíveis com o conjunto harmônico:" +
        f"\nNúmero de elementos no conjunto harmônico = {len(harm)}" +
        f"\nÍndice máximo da série = {max(serie)}"
        )
    
    #Verifica se duração é quantizável
    quantizacao = 0.25
    if duracao % quantizacao != 0:
        raise ValueError(f'O valor {duracao} não é múltiplo de 0.25, o valor de quantização')

    #Constrói a melodia
    melodia = [[],[]]; serie = []
    acc_serie = 0
    c = 0; nota_longa = 0
    while c < duracao:

        #Determina se é nota longa ou não
        r_nota_longa = random.random()
        if r_nota_longa < prob_nota_longa:
            rand_fig = [[duracao + 1],[1]]
        else:
            rand_fig = random.choice(figuras)
        
        #Se quantizado pela figura e cabe no tempo restante
        if c % rand_fig[1][0] == 0 and sum(rand_fig[0]) <= (duracao - c):
            
            #Adiciona a nota longa acumulada
            if nota_longa > 0:
                melodia[0].append(harm[serie[acc_serie]])
                melodia[1].append(nota_longa)
                serie.append(serie[acc_serie])
                nota_longa = 0
                
                #Incrementa idx da série no limite
                acc_serie += 1
                acc_serie = acc_serie % len(serie)
                
            for dur in rand_fig[0]:
                altura = harm[serie[acc_serie]]
                melodia[0].append(altura)
                melodia[1].append(dur)
                serie.append(serie[acc_serie])
                
                #Incrementa idx da série no limite
                acc_serie += 1
                acc_serie = acc_serie % len(serie)

            #Incrementa com a duração da figura
            c += sum(rand_fig[0])
        
        #Aumenta a duração da nota longa
        else:
            nota_longa += quantizacao
            c += quantizacao
    
    #Adiciona nota longa restante, se for o caso
    if nota_longa > 0:
        melodia[0].append(harm[serie[acc_serie]])
        melodia[1].append(nota_longa)
    
    #Retorna a melodia completa e a série
    return melodia[0], melodia[1], serie
