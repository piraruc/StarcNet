import pandas as pd
from confusion_matrix import generate_percentage_cm
from confusion_matrix import save_confusion_matrix_as_image

# Substituindo a leitura de dados pelo arquivo CSV
df = pd.read_csv("output/total.csv")

for index, row in df.iterrows():
    # Usando .iloc para acessar a primeira coluna
    row_name = row.iloc[0]  # Agora acessando a primeira coluna de maneira correta
    
    # Extraindo os valores das colunas restantes para formar a matriz 4x4
    row_data = row.iloc[1:].values.reshape(4, 4)  # Aqui, você cria a matriz 4x4
    
    # Gerando e salvando a matriz absoluta como imagem
    save_confusion_matrix_as_image(row_data, filename=f"{row_name}_absolute.png")
    
    # Gerando a matriz de porcentagens
    cm_percentage = generate_percentage_cm(row_data)
    
    # Salvando a matriz de porcentagens como imagem
    save_confusion_matrix_as_image(cm_percentage, filename=f"{row_name}_percentage.png")
# Calcular o total de cada coluna (somar todas as linhas de cada coluna)
col_totals = df.iloc[:, 1:].sum(axis=0)


# Transformando a Série de totais em uma matriz NumPy
# Aqui, vamos transformar a Série de totais (col_totals) para uma matriz (array NumPy)
matrix = col_totals.values.reshape(4, -1)  # Isso cria uma matriz 4xN

# Mostra a matriz NumPy
print("Matriz NumPy com totais por coluna:")
print(matrix)
cm_percentage = generate_percentage_cm(matrix)

save_confusion_matrix_as_image(matrix, filename="confusion_matrix_total_absolute.png")
save_confusion_matrix_as_image(cm_percentage, filename="confusion_matrix_total_percentage.png")