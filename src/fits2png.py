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

# Ler os dois arquivos CSV (um com as previsões e outro com os dados reais)

df = pd.read_csv('output/original.csv')

# Garantir que as colunas de coordenadas estejam no formato correto
df['x'] = df['x'].astype(int)
df['y'] = df['y'].astype(int)

# Filtrar as linhas onde 'class(mode)' é 0.0 (caso seja necessário)
df = df[df['class(mode)'] != 0.0]

df['class(mode)'] = df['class(mode)'].astype(int)
# Ler os nomes das galáxias de 'targets.txt'
with open('targets.txt', 'r') as f:
    galaxies = f.read().splitlines()

# Definir os parâmetros
sz = 16  # Tamanho do patch (i.e., sz x sz pixels)

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


for i in range(min(num_objs, len(class_ids[0]))):#precisa alterar para a quantidade de elementos em df******
    fig = plt.figure(figsize=(14, 4), dpi=80, facecolor='w', edgecolor='k')
    
    # O filtro pode ser extraído com base no ID ou outras informações
    filters = ['f275w', 'f336w', 'f438w', 'f435w', 'f555w', 'f606w', 'f814w']
    filter_name = filters[i % len(filters)]  # Aqui você pode ajustar conforme necessário
    
    # Carregar a imagem FITS
    img = load_fits_image(galaxies, filter_name)
    
    if img is not None:
        
        # falta realizar transformação em png****
        # Salvar a imagem gerada em vez de exibir
        output_filename = f'class_{class_label + 1}_obj_{i + 1}.png'#salvar com a classe, a galaxia e o id em df******
        plt.savefig(output_filename)
        plt.close(fig)  # Fechar a figura após salvar para liberar memória

print(f'Imagens para Class {class_label + 1} salvas!')
