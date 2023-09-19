import numpy as np
import random
import pandas as pd

"""

    Helton Pereira de Aguiar

    
"""

# Função de aptidão para o algoritmo genético
def aptidao(individuo, itens, peso_max):
    peso, valor = 0, 0
    for i in range(len(individuo)):
        if individuo[i] == 1:  # se o item está na mochila
            peso += itens[i][0]
            valor += itens[i][1]
    if peso > peso_max:
        return 0  # peso ultrapassa o limite da mochila
    return valor

# Crossover para o algoritmo genético
def crossover(pai1, pai2):
    indice = random.randint(1, len(pai1)-2)
    filho1 = pai1[:indice] + pai2[indice:]
    filho2 = pai2[:indice] + pai1[indice:]
    return filho1, filho2

# Mutação para o algoritmo genético
def mutacao(individuo):
    indice = random.randint(0, len(individuo)-1)
    individuo[indice] = 1 - individuo[indice]

# Algoritmo genético
def algoritmo_genetico(itens, tam_pop, n_geracoes, taxa_mutacao, peso_max):
    # Inicialização da população
    populacao = [[random.randint(0, 1) for _ in range(len(itens))] for _ in range(tam_pop)]
    
    for _ in range(n_geracoes):
        populacao.sort(reverse=True, key=lambda x: aptidao(x, itens, peso_max))
        
        # Seleção dos pais
        pai1, pai2 = populacao[0], populacao[1]
        
        # Crossover e mutação
        for i in range(2, tam_pop):
            if i % 2 == 0:
                populacao[i], _ = crossover(pai1, populacao[i])
                if random.random() < taxa_mutacao:
                    mutacao(populacao[i])
            else:
                _, populacao[i] = crossover(pai2, populacao[i])
                if random.random() < taxa_mutacao:
                    mutacao(populacao[i])
    
    # Retorna o melhor indivíduo da última geração
    populacao.sort(reverse=True, key=lambda x: aptidao(x, itens, peso_max))
    return populacao[0]

# Algoritmo dinâmico
def mochila(tamanho, itens, capacidade, dp):
    if tamanho == 0 or capacidade == 0:
        return 0
    if dp[tamanho - 1][capacidade] != -1:
        return dp[tamanho - 1][capacidade]
    if itens[tamanho - 1][0] > capacidade:
        dp[tamanho - 1][capacidade] = mochila(tamanho - 1, itens, capacidade, dp)
        return dp[tamanho - 1][capacidade]
    a = itens[tamanho - 1][1] + mochila(tamanho - 1, itens, capacidade - itens[tamanho - 1][0], dp)
    b = mochila(tamanho - 1, itens, capacidade, dp)
    dp[tamanho - 1][capacidade] = max(a,b)
    return dp[tamanho - 1][capacidade]

# Comparação dos algoritmos
def comparar_algoritmos(n_execucoes):
    resultados = []

    for i in range(n_execucoes):
        itens = [(np.random.randint(10 ,101), np.random.randint(10 ,101)) for _ in range(10)]
        capacidade = np.random.randint(100 ,501)
        tam_pop = np.random.randint(50 ,101)
        n_geracoes = np.random.randint(100 ,201)
        taxa_mutacao = np.random.uniform(0.01 ,0.05)

        # Executa o algoritmo genético e armazene o resultado
        melhor_individuo = algoritmo_genetico(itens,tam_pop,n_geracoes,
                                              taxa_mutacao,capacidade)
        resultado_genetico = aptidao(melhor_individuo ,itens,capacidade)

        # Executa o algoritmo dinâmico e armazene o resultado
        tamanho = len(itens)
        resultado_dinamico = mochila(tamanho, itens, capacidade, np.full((tamanho,capacidade+1),-1,dtype=int))

        resultados.append({"Execução": i+1, "Algoritmo Genético": resultado_genetico, "Algoritmo Dinâmico": resultado_dinamico})

    df = pd.DataFrame(resultados)

    # Altera as opções de exibição para visualizar a tabela completa
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)

    print("\n")
    print(df)
    
    print("\nAlgoritmo Genético: Média =", df["Algoritmo Genético"].mean(), "Desvio Padrão =", df["Algoritmo Genético"].std())
    print("\nAlgoritmo Dinâmico: Média =", df["Algoritmo Dinâmico"].mean(), "Desvio Padrão =", df["Algoritmo Dinâmico"].std())

comparar_algoritmos(100)

print("\n")