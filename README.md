# M-dulo
[![DOI](https://zenodo.org/badge/DOI/zenodo.1100965444.svg)](https://doi.org/10.5281/zenodo.18259764)
![Version](https://img.shields.io/badge/version-v1.0.0-blue)

Ambiente de composição musical com arquitetura modular e fluxo processual imperativo. 

## Descrição 
M-dulo opera com um conjunto de módulos composicionais multiparamétricos que, combinados em um fluxo linear de execução, produzem um ou mais arquivos MIDI multipista. O ambiente pode ser usado tanto para a criação de pequenos blocos de informação musical quanto, por meio da justaposição e combinação de módulos em matrizes de cada parâmetro (altura, duração e dinâmica), composições altamente estruturadas. M-dulo também é um ambiente aberto que suporta a implementação de outros fluxos de geração de dados como, por exemplo, o endereçamento da saída para leitores e reprodutores MIDI em tempo real.

## Instalação
1. Clonar ou realizar download dos arquivos do repositório M-dulo
2. Configurar ambiente virtual (se aplicável)
3. instale as dependências:

```
pip install -r requirements.txt
```

## Uso
O ambiente é estruturado por diversos módulos dispostos como bibliotecas de funções no diretório "modulos". Cada arquivo agrupa um conjunto de funções, tais como as rotações seriais de <code>series.series_paralelas()</code>, ou geração de conteúdo harmônico a partir de algoritmos <code>mipro.mipro()</code>.
Os projetos composicionais são construídos de modo imperativo e modular, como concatenação de eventos musicais. Os dados do projeto são importados como variáveis no arquivo <code>main.py</code> e, então, processados e exportados em formato MIDI. 

Dado o seu aspecto aberto, outros fluxos de criação são propiciados durante a construção da *partitura-texto* (i.e. projeto).

### Exemplo
Crie um projeto <code>exemplo.py</code> no diretório <code>/projetos</code>:

```python
#Importa as bibliotecas de subrotinas do projeto
from modulos import series, mipro

def modulo_exemplo(harmonia, melodia, ritmica, dinamica):
    # ... função específica ...
    
    #Bloco de retorno -> uma dimensão para cada parâmetro
    return [alturas, duracoes, dinamicas]
    
# --- Execução 1 ---

#Variáveis
harmonia_1 = ['do4', 're4', 'mi4', 'fa4', 'sol4', 'la4', 'si4']
melodia_1 = [0, 3, 2, 5, 4, 6, 0, 1, 2]
ritmica_1 = [0.5, 1.0, 0.5]
dinamica_1 = ["p", "f", "mp"]

melodia_1 = modulo_exemplo(harmonia_1, melodia_1, ritmica_1, dinamica_1)
```

Edite o fluxo de execução de <code>main.py</code>:

```python
import midi.gerador_midi as midi
from projetos import exemplo

#Diretório para exportar midi
diretorio = "/dir"
data = []  

#Fluxo imperativo de execução dos módulos
data.append(exemplo.melodia_1)

if __name__ == "__main__":
    # ... rotina de exportação ...
```

Salve ambos os arquivos e execute:

```
python main.py
```

## Estrutura da dados

O framework opera convertendo listas estruturadas de três dimensões primárias (`alturas`, `durações` e `dinâmicas`) em eventos MIDI padrão. 
Os dados aceitam tanto representações textuais (simbólicas) quanto numéricas, processadas pelo módulo utilitário de conversão.

### Alturas (`alturas`)
Define as alturas de cada evento ou pausas. Os formatos aceitos por vetor são:
* **Str:** Notas no formato literal (ex: `'do4'`, mapeadas via dicionário interno `mp.alt_midi`) ou literal `'pausa'` para gerar pausas.
* **Int:** Valores MIDI brutos entre `0` e `127`.
* **Float:** Valores entre `0.0` e `1.0` (escalados linearmente para o espaço MIDI de 0 a 127).

### Durações (`duracoes`)
Define o tempo de duração de cada nota ou pausa. Os formatos aceitos são:
* **Str:** Nomes de figuras rítmicas (ex: `'seminima'`, mapeadas via `mp.duracoes`).
* **Int:** Pulsos em *ticks* absolutos (semínima = 480).
* **Float:** Valores escalados com base no pulso da semínima (ex. colcheia = 0.5).

### Dinâmicas (`dinamicas`)
Define a intensidade (*velocity*) do evento. O sistema aplica suporte opcional a variação randômica controlada (`din_rand=True` por padrão):
* **Str:** Marcações de intensidade (ex: `'p'`, `'f'`, `'mp'`, mapeadas para intervalos de velocidade via `mp.dinamica`).
* **Int:** Valores brutos de velocidade MIDI entre `0` e `127` (com variação estocástica opcional de até +10 unidades).
* **Float:** Valores entre `0.0` e `1.0` (escalados para a faixa de 0 a 127).

### Exemplo de Estrutura de Entrada (`parametros`)
A função de exportação aceita tanto uma única voz (vetor de matriz) quanto múltiplas vozes (matrizes aninhadas):

```
1_voz = [[alt, dur, din]]
2_vozes = [[alt, dur, din],[alt, dur, din]]
```

Exemplo de dados que podem ser processados em uma única voz:

```python
# Exemplo de matriz para uma única voz: [alturas, duracoes, dinamicas]
voz_1 = [
    ['do4', 're4', 'pausa', 'mi4'],       # Alturas
    ['seminima', 480, 0.5, 'colcheia'],   # Durações
    ['p', 'f', 0.8, 100]                  # Dinâmicas
]
```

