import midi.gerador_midi as midi
from projetos import exemplo

#Diretório para exportar midi
diretorio = "/dir"
data = []  

#Fluxo imperativo de execução dos módulos
data.append(exemplo.melodia_1)
data.append(exemplo.melodia_2)
data.append(exemplo.melodias_sobrepostas)
data.append(exemplo.melodias_concatenadas)

if __name__ == "__main__":
    print(f' --- M-dulo\n --- Composição modular-imperativa\n --- v.1.0.0 (2026)\n')
    if not data:
        raise ValueError ("Não há módulos indexados para gravação.")
    print(f'Gravando {len(data)} módulo(s) no disco:\n')
    for modulo in data:
        midi.exporta_midi(modulo, diretorio)
    print('Execução finalizada.')

