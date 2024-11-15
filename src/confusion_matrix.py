import pandas as pd
from sklearn.metrics import confusion_matrix
import numpy as np

def generate_confusion_matrix(prediction_file, real_data_file):
    try:
        # Ler os dois arquivos CSV (um com as previsões e outro com os dados reais)
        df_predictions = pd.read_csv(prediction_file)
        df_real_data = pd.read_csv(real_data_file)

        # Filtrar as linhas onde 'class(mode)' é 0.0
        df_real_data = df_real_data[df_real_data['class(mode)'] != 0.0]

        # Unir os dataframes com base na correspondência entre 'Id' e 'source id'
        df_merged = pd.merge(df_predictions, df_real_data, left_on='Id', right_on='source id', how='inner')

        # Agora, temos as colunas 'Prediction' e 'class(mode)' para comparação
        # As previsões estão na coluna 'Prediction' (em inteiro) e as classes reais em 'class(mode)' (em float)
        
        # Garantir que 'Prediction' seja inteiro e 'class(mode)' seja inteiro para comparação
        df_merged['Prediction'] = df_merged['Prediction'].astype(int)
        df_merged['class(mode)'] = df_merged['class(mode)'].astype(int)
        
        # Gerar a matriz de confusão com 4 classes [1, 2, 3, 4]
        cm = confusion_matrix(df_merged['class(mode)'], df_merged['Prediction'], labels=[1, 2, 3, 4])

        # Exibir a matriz de confusão com números absolutos e porcentagens por classe
        print("Matriz de Confusão (Números Absolutos e Percentuais por Classe):")
        
        
        # Exibir os resultados
        print("\nMatriz de Confusão (apenas números absolutos):")
        print(cm)

        

        # Retornar a matriz de confusão para uso posterior, se necessário
        return cm

    except Exception as e:
        print(f"Ocorreu um erro: {e}")

def generate_percentage_cm(cm):
# Criar uma matriz NumPy para armazenar as porcentagens
    cm_percentage = np.zeros_like(cm, dtype=float)

    for i in range(len(cm)):
        total_class_i = np.sum(cm[i])  # Total de instâncias da classe real i
        for j in range(len(cm[i])):
            cm_percentage[i, j] = (cm[i, j] / total_class_i) * 100  # Calcula a porcentagem por classe real

    print("\nMatriz de Confusão (Percentuais por Classe):")
    print(cm_percentage)

    return cm_percentage

def save_confusion_and_percentage_to_csv(prediction_file, cm, output_file='output/total.csv'):
    try:
        # 1. Ler o nome da primeira coluna da segunda linha do arquivo de previsões
        df_predictions = pd.read_csv(prediction_file)
        first_column_name = df_predictions.iloc[1, 0]  # Posição [1, 0] é a segunda linha, primeira coluna
        
        # 2. Organizar os valores das matrizes cm (confusão)
        cm_values = cm.flatten()  # Flatten da matriz de confusão
        
        
        # 3. Criar um dicionário com os dados a serem salvos
        data_to_save = {'Galaxy': [first_column_name]}  # Começamos com o nome da primeira coluna da segunda linha
        
        # 4. Gerar as colunas dinâmicas para as matrizes de confusão (cm) e porcentagem (cm_percentage)
        for i in range(4):
            for j in range(4):
                # Para a matriz de confusão (cm)
                data_to_save[f'{i+1}v{j+1}'] = [cm_values[i*4 + j]]
                
        
        # 5. Criar um DataFrame a partir do dicionário de dados
        df_to_save = pd.DataFrame(data_to_save)
        
        # 6. Se o arquivo já existir, carrega e adiciona a nova linha, senão cria um novo
        try:
            # Tenta carregar o arquivo CSV existente
            df_existing = pd.read_csv(output_file)
            # Usando pd.concat() para adicionar as novas linhas
            df_existing = pd.concat([df_existing, df_to_save], ignore_index=True)
            df_existing.to_csv(output_file, index=False)
        except FileNotFoundError:
            # Se o arquivo não existir, cria um novo arquivo com os dados
            df_to_save.to_csv(output_file, index=False)
        
        print(f"Dados salvos em '{output_file}' com sucesso!")
    
    except Exception as e:
        print(f"Ocorreu um erro ao salvar os dados: {e}")

# Exemplo de uso
prediction_file = 'output/predictions.csv'  # Caminho para o arquivo com previsões do modelo
real_data_file = 'output/original.csv'  # Caminho para o arquivo com dados reais

cm = generate_confusion_matrix(prediction_file, real_data_file)
cm_percentage = generate_percentage_cm(cm)

# Salvar as informações no arquivo CSV
save_confusion_and_percentage_to_csv(prediction_file, cm)