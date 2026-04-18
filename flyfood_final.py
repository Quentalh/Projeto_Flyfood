import sys
import os
import numpy as np

'''
Nesse comit implementei uma função que corresponde a busca A* para obter a rota mais curta para o drone realizar seu objetivo.
Fazendo com que esse script seja uma versão apresentavel do projeto, eu uso o termo apresentavel, pois a função que implementei funciona como uma busca A* porém.
provavelmente como o codigo foi escrito manualmente, deve existir alguma forma de escreve-lo de uma forma mais limpa e mais eficiente, mas o código funciona e
entrega o resultado esperado.
'''

"""
Antes de explicar as funções menores vou fornecer uma explicação geral da busca A*:

O A* é um algoritmo de busca em grafos que encontra a rota de menor custo 
entre um estado inicial e um estado objetivo. Ele é amplamente utilizado em 
Inteligência Artificial por ser completo e ótimo (garante encontrar a melhor 
solução possível).

Lógica de Funcionamento:
A cada passo, o algoritmo decide qual caminho seguir avaliando a função: 
f(n) = g(n) + h(n)

Onde:
- g(n): É o custo real exato do ponto de partida até a posição atual (dronômetros gastos).
- h(n): É a função heurística, uma estimativa do custo do nó atual até o objetivo final.

Aplicação no Projeto (Problema do Caixeiro Viajante):
Para que o A* funcione perfeitamente ao visitar múltiplos pontos e retornar à 
base ('R'), a heurística h(n) nunca pode superestimar o custo real. 
Por isso, utilizamos o cálculo da Árvore Geradora Mínima (MST) das sub-redes 
não visitadas. A MST(Árvore Geradora Mínima) fornece uma estimativa otimista e matematicamente segura 
que guia o algoritmo para descartar rotas ruins e focar diretamente no percurso 
mais eficiente.


"""

'''
A função passo_sub_rede calculo o custo estimado da sub-rede, composta de todos os pontos que ainda não foram visitados,
tirando o ponto que está sendo analisado e o ponto em que estamos no momento.

Ela funciona recebendo a lista de pontos não visitados, uma cópia da lista para iterar sobre, uma lista pra guardar uma lista contendo o menor custo encontrado
e o ponto em que ele foi encontrado, o ponto que estamos no momento do loop e o custo final que vai sendo atualizado até o fim do loop, onde ele retorna o custo final da sub-rede.

'''

def passo_sub_rede(lista_nao_visitados, nao_visitados_iteraveis, menor_custo, local_atual, custo_final):
    if len(lista_nao_visitados) <= 1:
        return custo_final
    if len(nao_visitados_iteraveis) <= 1:
        for idx, x in enumerate(lista_nao_visitados):
            if x[0] == menor_custo[1]:
                local_atual = x
        for idx, x in enumerate(lista_nao_visitados):
            if x[0] == menor_custo[0]:
                del lista_nao_visitados[idx]
                break
        custo_final = custo_final + menor_custo[2]
        return passo_sub_rede(lista_nao_visitados, lista_nao_visitados[:], [], local_atual, custo_final)
    else:
        for x in nao_visitados_iteraveis:
            if x == nao_visitados_iteraveis[0]:
                continue
            carga = abs(nao_visitados_iteraveis[0][1] - x[1]) + abs(nao_visitados_iteraveis[0][2] - x[2])
            if menor_custo == []:
                menor_custo = [nao_visitados_iteraveis[0][0], x[0], carga]
            elif carga < menor_custo[2]:
                menor_custo = [nao_visitados_iteraveis[0][0], x[0], carga]
        del nao_visitados_iteraveis[0]
        return passo_sub_rede(lista_nao_visitados, nao_visitados_iteraveis, menor_custo, [], custo_final)

'''
A função passo2 calcula o custo estimado para ir do ponto atual para o ponto mais próximo entre a sub-rede de pontos que ainda não foram visitados.

'''

def passo2(localizacao_atual, nao_visitados):
    if len(nao_visitados) == 0:
        return 0    
    lista_para_comp = []
    for x in nao_visitados:
        distancia_sum = [x[0], abs(localizacao_atual[1] - x[1]) + abs(localizacao_atual[2] - x[2])]
        lista_para_comp.append(distancia_sum)
    lista_para_comp.sort(key=lambda x: x[1])
    return lista_para_comp[0][1]

'''
A função passo3 calcula o custo estimado para ir do ponto mais próximo da sub-rede de pontos não visitados para o ponto de inicio 'R'.
'''

def passo3(local_r, nao_visitados):
    if len(nao_visitados) == 0:
        return 0
    lista_para_comp = []
    for x in nao_visitados:
        distancia_sum = [x[0], abs(local_r[1] - x[1]) + abs(local_r[2] - x[2])]
        lista_para_comp.append(distancia_sum)
    lista_para_comp.sort(key=lambda x: x[1])
    return lista_para_comp[0][1]

'''
Dentro da busca_estrela, cada ponto da lista de localizações é avaliado para encontrar o custo total de visitar aquele ponto, que é a soma do custo real e o custo estimado(que em si é a soma
do custo da sub-rede, passo2 e passo3, funções executadas em cada ponto não visitado). O ponto com menor custo total é escolhido como o próximo a ser visitado,
a função é chamada de forma recursiva até que a lista de localizações fique vazia, e o custo final (custo para voltar a 'R') seja adiciona ao custo total, permitindo o retorno 
da string com a ordem dos pontos visitados e o custo total gasto no caminho.
'''

'''
O MOTOR DO ALGORITMO A* (Versão Pura com Fronteira)
--------------------------------------------------------------------
Ao invés de tomar uma decisão definitiva e apagar as outras opções (Busca Gulosa),
esta versão implementa uma "Fronteira" (Open List). O algoritmo guarda TODOS os 
caminhos simulados e sempre escolhe explorar aquele que tem a menor nota F total.
Isso permite que ele "volte no tempo" e tente rotas alternativas caso o caminho 
atual comece a ficar muito caro, garantindo a solução 100% ótima no final.
'''
def busca_estrela(localizacao_inicial, lista_de_localizacoes, dronometros_iniciais, caminho_inicial, local_r):

    fronteira = []

    fronteira.append([0, 0, localizacao_inicial, '', lista_de_localizacoes[:]])
    
    while len(fronteira) > 0:
        
        fronteira.sort(key=lambda x: x[0])
        estado_atual = fronteira.pop(0)
        custo_real = estado_atual[1]
        local_atual = estado_atual[2]
        caminho_atual = estado_atual[3]
        nao_visitados = estado_atual[4]
        if len(nao_visitados) == 0:
            custo_final = custo_real + abs(local_atual[1] - local_r[1]) + abs(local_atual[2] - local_r[2])
            return caminho_atual, int(custo_final)

        for l1 in nao_visitados:
            custo_passo = abs(local_atual[1] - l1[1]) + abs(local_atual[2] - l1[2])
            novo_custo_real = custo_real + custo_passo
            novo_caminho = caminho_atual + l1[0]
            novos_nao_visitados = nao_visitados[:]
            for idx, x in enumerate(novos_nao_visitados):
                if x == l1:
                    del novos_nao_visitados[idx]
                    break

            h_sub_rede = passo_sub_rede(novos_nao_visitados[:], novos_nao_visitados[:], [], '', 0)
            h_passo2 = passo2(l1, novos_nao_visitados)
            h_passo3 = passo3(local_r, novos_nao_visitados)
            custo_imaginario_estimado = h_sub_rede + h_passo2 + h_passo3
            custo_total_estimado = novo_custo_real + custo_imaginario_estimado
            fronteira.append([custo_total_estimado, novo_custo_real, l1, novo_caminho, novos_nao_visitados])

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
for lugar in alfabeto_sem_R[:(pontos)]:
    localizacao_linha, localizacao_coluna = np.where(matriz == lugar)
    lista_de_localizacoes.append([lugar, localizacao_linha, localizacao_coluna])

#Teste da busca_gulosa com o arquivo mapa.txt
print(busca_estrela(localizacao_r, lista_de_localizacoes, 0 , '', localizacao_r))
