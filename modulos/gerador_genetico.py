import random

# Método desenvolvido para a peça "A Queda do Paissandú" (2026)

'''
Gerador Genético

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
 '''   
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
'''
