import argparse

'''
Produz um rampa linear normalizada e arredondada (quantizada).
'''

def quantizar(valor, passo):
    return round(valor / passo) * passo


def rampa_linear(partes, total, quantizacao=0.01):
    passo = 100 / partes

    pesos = [
        passo * i
        for i in range(1, partes + 1)
    ]

    soma_pesos = sum(pesos)

    resultado = [
        (peso / soma_pesos) * total
        for peso in pesos
    ]

    return [
        quantizar(valor, quantizacao)
        for valor in resultado
    ]


def main():
    parser = argparse.ArgumentParser(
        description="Produz um rampa linear normalizada e arredondada (quantizada)."
    )

    parser.add_argument(
        "partes",
        type=int,
        help="Número de partes (pontos) da rampa."
    )

    parser.add_argument(
        "total",
        type=float,
        help="Escala da rampa (1.0 = de 0 a 1)."
    )

    parser.add_argument(
        "-q",
        type=float,
        default=0.01,
        help="Passo de quantização (ex: 0.25)"
    )

    args = parser.parse_args()

    if args.partes <= 0:
        parser.error("partes deve ser maior que zero.")

    if args.quantizacao <= 0:
        parser.error("quantizacao deve ser maior que zero.")

    resultado = rampa_linear(
        args.partes,
        args.total,
        args.quantizacao
    )

    print([f"{valor:.2f}" for valor in resultado])
    print(f"Soma: {sum(resultado):.2f}")


if __name__ == "__main__":
    main()
