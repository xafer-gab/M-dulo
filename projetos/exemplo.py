from modulos import series
from util import edicao

def modulo_exemplo(harmonia, melodia, ritmica, dinamica):
    
    #Produz uma melodia
    melodia_repetida = series.serializa_por_idx(harmonia, melodia, n_notas=len(melodia) * 2)
    
    #Retorna listas do mesmo tamanho
    alturas, duracoes, dinamicas = series.series_paralelas(melodia_repetida, ritmica, dinamica, tipo="aumenta")
    
    #Bloco de retorno -> uma dimensão para cada parâmetro
    return [alturas, duracoes, dinamicas]
    
# --- Execução 1 ---

#Variáveis
harmonia_1 = ['do4', 're4', 'mi4', 'fa4', 'sol4', 'la4', 'si4']
melodia_1 = [0, 3, 2, 5, 4, 6, 0, 1, 2]
ritmica_1 = [0.5, 1.0, 0.5]
dinamica_1 = ["p", "f", "mp"]

melodia_1 = modulo_exemplo(harmonia_1, melodia_1, ritmica_1, dinamica_1)

# --- Execução 2 ---

#Variáveis
harmonia_2 = harmonia_1[:]
melodia_2 = [0, 4, 2, 3, 2, 4]
ritmica_2 = [1.0]
dinamica_2 = ["f", "mp"]

melodia_2 = modulo_exemplo(harmonia_2, melodia_2, ritmica_2, dinamica_2)

#Procedimentos comuns de sobreposição e concatenação de módulos
melodias = [melodia_1, melodia_2]

#1. Sobrepõe vozes
melodias_sobrepostas = edicao.sobrepoe(melodias)

#2. Concatenação de módulos
melodias_concatenadas = edicao.concatena(melodias)
    
