def concatena(melodias):
    melodias_concatenadas = [[],[],[]]
    for serie in melodias:
        for i, param in enumerate(serie):
            melodias_concatenadas[i].extend(param)
    return melodias_concatenadas

def sobrepoe(melodias):
    melodias_sobrepostas = [[],[],[]]
    for serie in melodias:
        for i, param in enumerate(serie):
            melodias_sobrepostas[i].append(param)
    return melodias_sobrepostas
