import sys
import os
import numpy as np

def heuristica(localizacao_r, lista_de_localizacoes,distancia,caminho,dronometros_sum, penultimo_ponto):
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
                lista_heuristica = lista_de_localizacoes[:maioridx] + lista_de_localizacoes[maioridx+1:]
                dronometros_sum = dronometros_sum + distancia
                return heuristica(localizacao_r, lista_heuristica,distancia_nova,caminho, dronometros_sum, lista_de_localizacoes[maioridx])
            else:
                distancia_nova = 0
                caminho = caminho + lista_de_localizacoes[maioridx][0]
                lista_de_localizacoes[0] = lista_de_localizacoes[maioridx]
                dronometros_sum = dronometros_sum + distancia
                lista_heuristica = lista_de_localizacoes[:maioridx] + lista_de_localizacoes[maioridx+1:]

                return heuristica(localizacao_r, lista_heuristica,distancia_nova,caminho, dronometros_sum,lista_de_localizacoes[maioridx])
        else:
            if distancia_sum < distancia:
                distancia = distancia_sum
                maioridx = i
    



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
o = 0
alfabeto_sem_R = list("ABCDEFGHIJKLMNOPQSTUVWXYZ")
lista_de_localizacoes = []
linha_r , coluna_r = np.where(matriz == 'R')
localizacao_r = ['R', linha_r, coluna_r]
lista_de_localizacoes.append(['R', linha_r, coluna_r])
for lugar in alfabeto_sem_R[:(pontos)]:
    localizacao_linha, localizacao_coluna = np.where(matriz == lugar)
    lista_de_localizacoes.append([lugar, localizacao_linha, localizacao_coluna])

print(heuristica(localizacao_r, lista_de_localizacoes, 0 , '', 0, []))





        

    