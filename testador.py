import time
import subprocess
import random

NUM_NIVEIS = 46
alfabeto = [f"P{i}" for i in range(1, NUM_NIVEIS + 1)]

TAMANHO_MAPA = 15
LINHA_R, COLUNA_R = 7, 7 

random.seed(42)
todas_coordenadas_possiveis = [(r, c) for r in range(TAMANHO_MAPA) for c in range(TAMANHO_MAPA) if (r, c) != (LINHA_R, COLUNA_R)]
random.shuffle(todas_coordenadas_possiveis)

coordenadas_letras = {letra: todas_coordenadas_possiveis[i] for i, letra in enumerate(alfabeto)}

nome_arquivo_log = "prova_limite_recursao.txt"

with open(nome_arquivo_log, "w", encoding="utf-8") as log:
    log.write("--- BENCHMARK: TESTE DE ESTOURO DE PILHA (RECURSION LIMIT) ---\n")
    log.write("Objetivo: Provar o limite da função 'passo_sub_rede' no nível 46.\n\n")

print(f"Iniciando caçada ao RecursionError! Indo até o nível {NUM_NIVEIS}...\n")

for i in range(1, NUM_NIVEIS + 1):
    letras_atuais = alfabeto[:i]

    matriz = [['0' for _ in range(TAMANHO_MAPA)] for _ in range(TAMANHO_MAPA)]
    matriz[LINHA_R][COLUNA_R] = 'R' 

    for letra in letras_atuais:
        linha, coluna = coordenadas_letras[letra]
        matriz[linha][coluna] = letra

    with open("mapa_temp.txt", "w", encoding="utf-8") as f:
        f.write(f"{TAMANHO_MAPA} {TAMANHO_MAPA}\n")
        for linha in matriz:
            f.write(" ".join(linha) + "\n")

    print(f"[{i}/{NUM_NIVEIS}] Calculando rota para {i} entregas...", end=" ")

    inicio = time.perf_counter()
    processo = subprocess.run(
        ["python3", "flyfood_final.py", "mapa_temp.txt"],
        capture_output=True, text=True
    )

    fim = time.perf_counter()
    tempo_gasto = fim - inicio
    
    if processo.returncode == 0:
        resultado_saida = processo.stdout.strip()
        status = f"OK ({tempo_gasto:.4f}s)"
    else:
        resultado_saida = "CRASH DETECTADO: " + processo.stderr.strip().split('\n')[-1]
        status = "FALHA DE MEMÓRIA!"

    print(status)

    log_texto = f"Nível {i} | Entregas: {len(letras_atuais)}\n"
    log_texto += f"Resultado: {resultado_saida}\n"
    log_texto += f"Tempo: {tempo_gasto:.4f} segundos\n"
    log_texto += "-" * 60 + "\n"

    with open(nome_arquivo_log, "a", encoding="utf-8") as log:
        log.write(log_texto)

print(f"\nTeste concluído! O arquivo '{nome_arquivo_log}' está pronto para ser anexado ao seu relatório.")