import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.special import softmax
from astropy.io import fits
import os

# Função para gerar imagens RGB
def legus2rgb(im):
    datac = np.zeros((im.shape[1], im.shape[2], 3), dtype=np.float64)
    datac[:, :, 2] = (21.63 * im[0, :, :] + 8.63 * im[1, :, :]) / 2.0
    datac[:, :, 1] = (4.52 * im[2, :, :])
    datac[:, :, 0] = (1.23 * im[3, :, :] + im[4, :, :]) / 2.0
    return np.clip(datac, 0, 1)

# Leitura do arquivo CSV contendo as previsões
df = pd.read_csv('output/predictions.csv')  

# Previsões e scores
predictions = df['Prediction'].values
scores = np.load(os.path.join('output', 'scores.npy'))  # Ajuste para o caminho correto

# Ler os nomes das galáxias de 'targets.txt'
with open('targets.txt', 'r') as f:
    galaxies = f.read().splitlines()

# Definir os parâmetros
sz = 16  # Tamanho do patch (i.e., sz x sz pixels)
num_objs = 10  # Número de objetos a serem exibidos

# Função para carregar as imagens FITS
def load_fits_image(galaxy, filter_name):
    fits_filename = f'legus/frc_fits_files/hlsp_legus_hst_{filter_name}_{galaxy}_v1_drc.fits'
    try:
        with fits.open(fits_filename) as hdul:
            # Suponha que a imagem esteja na primeira extensão
            img_data = hdul[1].data
            return img_data
    except Exception as e:
        print(f"Erro ao carregar {fits_filename}: {e}")
        return None

# Processar e exibir as imagens para cada classe
for class_label in range(4):  # Supondo que as classes vão de 0 a 3
    class_ids = np.where(predictions == class_label)
    if len(class_ids[0]) == 0:
        print(f'[Class {class_label + 1}] No objects predicted')
        continue
    
    # Calcular as probabilidades usando softmax
    scores_ids = softmax(scores, axis=1)[class_ids][:, class_label]
    
    # Ordenar os ids pelas pontuações de maior para menor
    sorted_ids = np.argsort(scores_ids)[::-1]
    
    print(f'[Class {class_label + 1}] Objects: {len(sorted_ids)}')
    
    # Criar um gráfico para cada classe
    for i in range(min(num_objs, len(class_ids[0]))):
        fig = plt.figure(figsize=(14, 4), dpi=80, facecolor='w', edgecolor='k')
        
        # Subplot para cada objeto
        plt.subplot(1, num_objs, i + 1)
        
        # Obtendo o ID da galáxia e o filtro
        galaxy_id = df['Id'].iloc[class_ids[0][sorted_ids[i]]]
        galaxy_name = galaxies[galaxy_id]  # Obtém o nome da galáxia correspondente
        
        # O filtro pode ser extraído com base no ID ou outras informações
        filters = ['f275w', 'f336w', 'f438w', 'f435w', 'f555w', 'f606w', 'f814w']
        filter_name = filters[i % len(filters)]  # Aqui você pode ajustar conforme necessário
        
        # Carregar a imagem FITS
        img = load_fits_image(galaxy_name, filter_name)
        
        if img is not None:
            # Gerar a imagem RGB usando a função legus2rgb
            plt.imshow(legus2rgb(img))
            
            # Adicionar título com o Id do objeto e sua pontuação
            plt.title(f'{galaxy_name} ({df["Id"].iloc[class_ids[0][sorted_ids[i]]]}): {scores_ids[sorted_ids[i]] * 100:.1f}%')
            plt.axis('off')
            
            # Salvar a imagem gerada em vez de exibir
            output_filename = f'class_{class_label + 1}_obj_{i + 1}.png'
            plt.savefig(output_filename)
            plt.close(fig)  # Fechar a figura após salvar para liberar memória

    print(f'Imagens para Class {class_label + 1} salvas!')
