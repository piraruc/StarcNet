import pandas as pd
from confusion_matrix import generate_percentage_cm

# Substituindo a leitura de dados pelo arquivo CSV
df = pd.read_csv("output/total.csv")

# Calcular o total de cada coluna (somar todas as linhas de cada coluna)
col_totals = df.iloc[:, 1:].sum(axis=0)


# Transformando a Série de totais em uma matriz NumPy
# Aqui, vamos transformar a Série de totais (col_totals) para uma matriz (array NumPy)
matrix = col_totals.values.reshape(4, -1)  # Isso cria uma matriz 4xN

# Mostra a matriz NumPy
print("Matriz NumPy com totais por coluna:")
print(matrix)
cm_percentage = generate_percentage_cm(matrix)