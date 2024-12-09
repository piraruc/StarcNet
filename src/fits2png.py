import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from astropy.io import fits
import os
import ast
import sys
sys.path.insert(0, './src/utils')
sys.path.insert(0, './model')
from data_utils import load_db

batch_size = 64  # input batch size for testing (default: 64)
data_dir = 'data/'  # dataset directory
dataset = 'raw_32x32'  # dataset file reference
checkpoint = 'model/starcnet.pth'  # trained model
gpu = ''  # CUDA visible device (when using a GPU add GPU id (e.g. '0'))
cuda = False  # enables CUDA training (when using a GPU change to True)

data_all, _, ids = load_db(os.path.join(data_dir, 'test_' + dataset + '.dat'))

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
    galaxies = f.read().splitlines()  # Lê todas as galáxias no arquivo e as coloca numa lista

# Definir os parâmetros
sz = 16  # Tamanho do patch (i.e., sz x sz pixels)

# Função para carregar as imagens FITS
def load_fits_image(galaxy, filter_name):
    fits_filename = f'legus/frc_fits_files/hlsp_legus_hst_uvis_{galaxy}_{filter_name}_v1_drc.fits'
    try:
        with fits.open(fits_filename) as hdul:
            # Suponha que a imagem esteja na primeira extensão
            img_data = hdul[1].data
            return img_data
    except Exception as e:
        print(f"Erro ao carregar {fits_filename}: {e}")
        return None

# Criar a pasta 'output/cropped/{galaxy_name}' se não existir
output_dir = os.path.join('output', 'cropped', galaxies)
os.makedirs(output_dir, exist_ok=True)

# Loop pelas classes de objetos do DataFrame
for idx, row in df.iterrows():  # Iterando sobre as linhas do DataFrame
    class_label = row['class(mode)']
    
    fig = plt.figure(figsize=(14, 4), dpi=80, facecolor='w', edgecolor='k')
    
    # Gerar a imagem RGB
    img_rgb = legus2rgb(data_all[:][:][idx, :, :, :])
    
    # Plotar a imagem no gráfico
    plt.imshow(img_rgb)
    plt.axis('off')  # Desativar os eixos para uma imagem limpa
    
    # Salvar a imagem gerada com base na classe, ID da galáxia e filtro
    output_filename = os.path.join(output_dir, f'class_{class_label}_galaxy_{galaxy_name}_obj_{idx + 1}.png')
    plt.savefig(output_filename, bbox_inches='tight', pad_inches=0)
    plt.close(fig)  # Fechar a figura após salvar para liberar memória

print(f'Imagens para as classes salvas em "output/cropped"!') 
