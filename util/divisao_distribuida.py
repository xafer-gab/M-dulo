import argparse
import random

'''
Divisão de um valor em n partes com arredondamento e distribuição aleatória das partes (dithering).
'''

def gerar_lista_soma_aleatoria(total, n, passo=0.5):
  media = total / n
  lista = [round(media / passo) * passo for _ in range(n)]

  diferenca = round(total - sum(lista), 10)
  passos_necessarios = int(round(diferenca / passo))

  if passos_necessarios != 0:
    indices = list(range(n))
    random.shuffle(indices)

    direcao = 1 if passos_necessarios > 0 else -1
    qte = abs(passos_necessarios)

    for i in range(qte):
      idx = indices[i % n]
      lista[idx] += direcao * passo

  return lista


if __name__ == "__main__":
  parser = argparse.ArgumentParser(
      description=(
          "Divisão de um valor em n partes com arredondamento e distribuição aleatória das partes (dithering)"
      )
  )
  parser.add_argument(
      "total", type=float, help="Valor total que será dividido"
  )
  parser.add_argument("n", type=int, help="Número divisor")
  parser.add_argument(
      "--passo", type=float, default=0.5, help="Passo de quantização (padrão: 0.5)"
  )

  args = parser.parse_args()

  resultado = gerar_lista_soma_aleatoria(args.total, args.n, args.passo)
  print("Lista:", resultado)
  print("Soma:", sum(resultado))
