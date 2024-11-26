import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.special import softmax
import os

# Função para gerar imagens RGB
def legus2rgb(im):
    datac = np.zeros((im.shape[1], im.shape[2], 3), dtype=np.float64)
    datac[:, :, 2] = (21.63 * im[0, :, :] + 8.63 * im[1, :, :]) / 2.0
    datac[:, :, 1] = (4.52 * im[2, :, :])
    datac[:, :, 0] = (1.23 * im[3, :, :] + im[4, :, :]) / 2.0
    return np.clip(datac, 0, 1)

# Leitura do arquivo CSV contendo as previsões (ajuste o caminho para o seu arquivo)
df = pd.read_csv('output/predictions.csv')  

# 
predictions = df['Prediction'].values
scores = np.load(os.path.join('output', 'scores.npy'))  # Altere para o caminho correto, se necessário


# Definir os parâmetros
sz = 16  # Tamanho do patch (i.e., sz x sz pixels)
num_objs = 10  # Número de objetos a serem exibidos

# A variável 'data_all' deve ser definida aqui. Assumindo que seja um array contendo as imagens.
# Exemplo: data_all = np.load('path_to_images.npy')  # Ajuste conforme necessário para carregar as imagens

# Processar e exibir as imagens para cada classe
for class_label in range(4):  # Supondo que as classes vão de 0 a 3
    class_ids = np.where(predictions == class_label)
    if len(class_ids[0]) == 0:
        print('[Class %d] No objects predicted' % (class_label + 1))
        continue
    
    # Calcular as probabilidades usando softmax
    scores_ids = softmax(scores, axis=1)[class_ids][:, class_label]
    
    # Ordenar os ids pelas pontuações de maior para menor
    sorted_ids = np.argsort(scores_ids)[::-1]
    
    print('[Class %d] Objects: %d' % (class_label + 1, len(sorted_ids)))
    
    # Criar um gráfico para cada classe
    for i in range(min(num_objs, len(class_ids[0]))):
        fig = plt.figure(figsize=(14, 4), dpi=80, facecolor='w', edgecolor='k')
        
        # Subplot para cada objeto
        plt.subplot(1, num_objs, i + 1)
        
        # Selecionar a imagem do objeto classificado
        img = data_all[class_ids[0][sorted_ids[i]], :, :, :]  # Ajuste conforme necessário para carregar suas imagens
        
        # Gerar a imagem RGB usando a função legus2rgb
        plt.imshow(legus2rgb(img))
        
        # Adicionar título com o Id do objeto e sua pontuação
        plt.title('%d(%.1f%%)' % (df['Id'].iloc[class_ids[0][sorted_ids[i]]], scores_ids[sorted_ids[i]] * 100))
        plt.axis('off')
        
        # Salvar a imagem gerada em vez de exibir
        output_filename = f'class_{class_label + 1}_obj_{i + 1}.png'
        plt.savefig(output_filename)
        plt.close(fig)  # Fechar a figura após salvar para liberar memória

    print(f'Imagens para Class {class_label + 1} salvas!')
