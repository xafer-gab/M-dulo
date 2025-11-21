# M-dulo
Ambiente de composição musical com arquitetura modular e fluxo processual imperativo. 

### Descrição 
M-dulo opera com um conjunto de módulos composicionais multiparamétricos que, combinados em um fluxo linear de execução, produzem um único aqruivo MIDI multipista. O ambiente pode ser usado tanto para a criação de pequenos blocos de informação musical quanto, por meio da justaposição e combinação de módulos em matrizes de cada parâmetro (altura, duração e dinâmica), composições altamente estruturadas. M-dulo também é um ambiente aberto que suporta a implementação de outros fluxos de geração de dados como, por exemplo, o endereçamento da saída para leitores e reprodutores MIDI em tempo real.

### Instalação
1. Clonar ou realizar download dos arquivos do repositório M-dulo
2. Configurar ambiente virtual (se aplicável)
3. instale as dependências:

```
pip install -r requirements.txt
```

### Uso
O ambiente é estruturado por diversos módulos dispostos como bibliotecas de funções no diretório "modulos". Cada arquivo agrupa um conjunto de funções, tais como as rotações seriais de <code>series.series_paralelas()</code>, ou geração de conteúdo harmônico a partir de algoritmos <code>MIDO.mido()</code>.
Os módulos são compostos de maneira imperativa, como concatenação de eventos musicais, no interior da função <code>exe_modulos()</code> em <code>main.py</code>. 

Dado o seu aspecto aberto, outros fluxos de criação são propiciados durante a construção da *partitura-texto*.
Para renderizar o resultado em um arquivo MIDI, grave o arquivo <code>main.py</code> modificado e execute:

```
python3 main.py
```

### Exemplo
Modifique a função <code>exe_modulos()</code>:

```
def exe_modulos():
    
    #Exemplo de geração de alturas com o módulo "mipro"
    serie_alt = []
    inter = 1; comp = 20
    for i in range(4):
        s_alt = mipro("do", inter, 5, comprimento=comp)
        for e in s_alt[0]:
            oit = randrange(3, 5)
            serie_alt.append(f"{data_midi.int_class[e]}{oit}")
        inter += 1; comp -= 5
    
    #Constantes de duração e dinâmica (dicionário de nomes em data/midi_part.py)
    serie_dur = ["semicolcheia", "colcheia", "tercina_colcheia", "minima", "colcheia_p"]
    serie_din = ["f", "p", "mf", "fff"]
    
    #Exemplo de rotação serial com o módulo "serie_rand_rotativa"
    alturas, duracoes, dinamicas = serial.serie_rand_rotativa(
        serie_alt, 
        serie_dur, 
        serie_din, 
        n_notas=len(serie_alt), 
        fix_rot=[0, 1, 1]
        )
    
    #Bloco de retorno -> uma ou mais dimensões para cada parâmetro
    return alturas, duracoes, dinamicas

```
Salve e execute:

```
python3 main.py
```



