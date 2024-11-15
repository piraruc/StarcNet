import requests
import os

# Lista de URLs para download
urls = [
    "https://archive.stsci.edu/hlsps/legus/ugca281/ugca281_drc.tar.gz",
    "https://archive.stsci.edu/hlsps/legus/ugc7408/ugc7408_drc.tar.gz",
    "https://archive.stsci.edu/hlsps/legus/ugc7242/ugc7242_drc.tar.gz",
    "https://archive.stsci.edu/hlsps/legus/ugc695/ugc695_drc.tar.gz",
    "https://archive.stsci.edu/hlsps/legus/ugc685/ugc685_drc.tar.gz",
    "https://archive.stsci.edu/hlsps/legus/ugc5340/ugc5340_drc.tar.gz",
    "https://archive.stsci.edu/hlsps/legus/ugc5139/ugc5139_drc.tar.gz",
    "https://archive.stsci.edu/hlsps/legus/ugc4459/ugc4459_drc.tar.gz",
    "https://archive.stsci.edu/hlsps/legus/ugc4305/ugc4305_drc.tar.gz",
    "https://archive.stsci.edu/hlsps/legus/ugc1249/ugc1249_drc.tar.gz",
    "https://archive.stsci.edu/hlsps/legus/ngc7793-e/ngc7793-e_drc.tar.gz",
    "https://archive.stsci.edu/hlsps/legus/ngc6744-n/ngc6744-n_drc.tar.gz",
    "https://archive.stsci.edu/hlsps/legus/ngc6744-c/ngc6744-c_drc.tar.gz",
    "https://archive.stsci.edu/hlsps/legus/ngc6503/ngc6503_drc.tar.gz",
    "https://archive.stsci.edu/hlsps/legus/ngc628-e/ngc628-e_drc.tar.gz",
    "https://archive.stsci.edu/hlsps/legus/ngc628-c/ngc628-c_drc.tar.gz",
    "https://archive.stsci.edu/hlsps/legus/ngc5949/ngc5949_drc.tar.gz",
    "https://archive.stsci.edu/hlsps/legus/ngc5477/ngc5477_drc.tar.gz",
    "https://archive.stsci.edu/hlsps/legus/ngc5474/ngc5474_drc.tar.gz",
    "https://archive.stsci.edu/hlsps/legus/ngc5457-se/ngc5457-se_drc.tar.gz",
    "https://archive.stsci.edu/hlsps/legus/ngc5457-nw3/ngc5457-nw3_drc.tar.gz",
    "https://archive.stsci.edu/hlsps/legus/ngc5457-nw2/ngc5457-nw2_drc.tar.gz",
    "https://archive.stsci.edu/hlsps/legus/ngc5457-nw1/ngc5457-nw1_drc.tar.gz",
    "https://archive.stsci.edu/hlsps/legus/ngc5457-c/ngc5457-c_drc.tar.gz",
    "https://archive.stsci.edu/hlsps/legus/ngc5253/ngc5253_drc.tar.gz"
]

# Pasta de destino no servidor local
dest_folder = r'legus/frc'

# Função para fazer o download do arquivo
def download_file(url, dest_folder):
    # Pega o nome do arquivo a partir da URL
    filename = os.path.join(dest_folder, url.split('/')[-1])

    # Verifica se o arquivo já foi baixado
    if os.path.exists(filename):
        print(f"Arquivo {filename} já existe. Pulando download.")
        return
    
    # Faz o download
    print(f"Baixando {url}...")
    response = requests.get(url, stream=True)
    
    # Se a requisição for bem-sucedida, salva o arquivo
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        print(f"Arquivo {filename} baixado com sucesso!")
    else:
        print(f"Erro ao baixar {url}: {response.status_code}")

# Função para baixar todos os arquivos
def download_all_files(urls, dest_folder):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)  # Cria o diretório se não existir
    
    for url in urls:
        download_file(url, dest_folder)

# Rodar o script
if __name__ == '__main__':
    download_all_files(urls, dest_folder)
