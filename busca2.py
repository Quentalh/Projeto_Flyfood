from random import randint, shuffle

#lista = [randint(1,1000000) for i in range(1000000)]
lista = list(range(1, 1000001))
shuffle(lista)

print("tamanho da lista: ", len(lista))

print("Primeiros 20 elementos: ", lista[:20])

soma = 0
for _ in range(1000000):
	pos = 1000000 #se nao achar o elemento, vai contabilizar
		      # 1 milhao de posicoes que foram procuradas
	x = randint(1, 1000000)
	for i in range(len(lista)):
		if lista[i] == x:
			pos = i
			break
	soma += pos
print("Somatorio das posicoes: ", soma)
print("Media:", soma/1000000)

print("Programa finalizado")
