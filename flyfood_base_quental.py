import sys
import os
import numpy as np

'''
Inicialmente utilizei a função  de busca gulosa para resolver o problema, apesar de ser uma solução rápida ela é sub-otima.
A função mais eficiente para a gente implementar seria a função de busca A* que eu vou implementar no meu proximo commit.
'''

def busca_gulosa(localizacao_r, lista_de_localizacoes,distancia,caminho,dronometros_sum, penultimo_ponto):
    if len(lista_de_localizacoes) <= 2:
        distanciax = abs(localizacao_r[1] - lista_de_localizacoes[1][1])
        distanciay = abs(localizacao_r[2] - lista_de_localizacoes[1][2])
        distanciax2 = abs(lista_de_localizacoes[1][1] - penultimo_ponto[1])
        distanciay2 = abs(lista_de_localizacoes[1][2] - penultimo_ponto[2])
        distancia_sum = distanciax + distanciay + distanciax2 + distanciay2
        dronometros_sum = dronometros_sum + distancia_sum 
        caminho = caminho + lista_de_localizacoes[1][0]
        return caminho, int(dronometros_sum[0])
    for i in range(1, len(lista_de_localizacoes)):
        distanciax = abs(lista_de_localizacoes[0][1] - lista_de_localizacoes[i][1])
        distanciay = abs(lista_de_localizacoes[0][2] - lista_de_localizacoes[i][2])
        distancia_sum = distanciax + distanciay
        if i == 1:
            distancia = distancia_sum
            maioridx = 1
            continue
        if i == (len(lista_de_localizacoes)-1):
            if distancia_sum < distancia:
                maioridx = i
                distancia_nova = 0
                lista_gulosa = lista_de_localizacoes[:maioridx] + lista_de_localizacoes[maioridx+1:]
                dronometros_sum = dronometros_sum + distancia
                return busca_gulosa(localizacao_r, lista_gulosa,distancia_nova,caminho, dronometros_sum, lista_de_localizacoes[maioridx])
            else:
                distancia_nova = 0
                caminho = caminho + lista_de_localizacoes[maioridx][0]
                lista_de_localizacoes[0] = lista_de_localizacoes[maioridx]
                dronometros_sum = dronometros_sum + distancia
                lista_gulosa = lista_de_localizacoes[:maioridx] + lista_de_localizacoes[maioridx+1:]

                return busca_gulosa(localizacao_r, lista_gulosa,distancia_nova,caminho, dronometros_sum,lista_de_localizacoes[maioridx])
        else:
            if distancia_sum < distancia:
                distancia = distancia_sum
                maioridx = i
    

'''
O código abaixo cria um loop onde ele pede ao usuário para inserir o nome do arquivo que contém a matriz.
Caso o arquivo não seja encontrado ele pede continuamente ao usuário para tentar novamente.
Se o arquivo for encontrado e conter uma entrada viável, como no exemplo do projeto , o código 
recebe a matriz como uma grande string dividida em várias linhas, utilizando os dois numeros da primeira para criar o formato da matriz no numpy e preenche-la inicialmente com zeros,
e as linhas seguintes para definir a localizacao na matriz e o numero de pontos que o drone precisa visitar, além de seu próprio ponto de inicio 'R'.
'''

if len(sys.argv) > 1:
    file_path = sys.argv[1]
else:

    while True:
        file_path = input("Please enter the filename: ")
        
        if os.path.isfile(file_path):
            break
        else:
            print("File not found. Please try again.")

with open(file_path, 'r', encoding='utf-8') as file:
    i = 0
    pontos = 0
    for linha in file:
        if i == 0:
            tamanho = linha.split()
            matriz = np.zeros((int(tamanho[0]),int(tamanho[1])), dtype='object')
            i += 1
        else:
            linha_matriz = linha.split()
            for idx, elemento in enumerate(linha_matriz):
                if elemento != '0' and elemento != 'R':
                    pontos += 1
                matriz[(i-1),(idx)] = linha_matriz[idx]
            i += 1

'''
Este código abaixo cria uma lista com todas as letras do alfabeto,e  uma lista com as localizações de todos os pontos na matriz,
a qual é preenchida em um loop que encontra a localização de cada ponto por sua letra utilizando a lista do alfabeto,
e depois insere na lista uma lista contendo a string da letra do ponto Ex('A','B',etc), um array contendo o numero da linha em que o ponto está na matriz,
e um array contendo o numero da coluna em que o ponto está na matriz.
Além disso a lista com a localização de R é definida antes do loop para que seja sempre o primeiro item da lista de localizações.
'''

alfabeto_sem_R = list("ABCDEFGHIJKLMNOPQSTUVWXYZ")
lista_de_localizacoes = []
linha_r , coluna_r = np.where(matriz == 'R')
localizacao_r = ['R', linha_r, coluna_r]
lista_de_localizacoes.append(['R', linha_r, coluna_r])
for lugar in alfabeto_sem_R[:(pontos)]:
    localizacao_linha, localizacao_coluna = np.where(matriz == lugar)
    lista_de_localizacoes.append([lugar, localizacao_linha, localizacao_coluna])

#Teste da busca_gulosa com o arquivo mapa.txt

print(busca_gulosa(localizacao_r, lista_de_localizacoes, 0 , '', 0, []))





        

    
