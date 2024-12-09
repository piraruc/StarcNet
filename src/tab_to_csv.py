import csv
import os

# Função para converter .tab para .csv
def tab_to_csv(tab_file, csv_file):
    try:
        # Abrir o arquivo .tab para leitura
        with open(tab_file, 'r', encoding='utf-8') as tab_f:
            # Ler o conteúdo do arquivo .tab
            reader = csv.reader(tab_f, delimiter='\t')
            
            # Abrir o arquivo .csv para escrita
            with open(csv_file, 'w', newline='', encoding='utf-8') as csv_f:
                writer = csv.writer(csv_f)
                
                # Escrever as linhas no arquivo .csv
                for row in reader:
                    writer.writerow(row)
                
        print(f"Conversão concluída! O arquivo CSV foi salvo em '{csv_file}'.")
    
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

# Função para substituir espaços por vírgulas no arquivo CSV
def replace_spaces_in_csv(csv_file):
    try:
        # Ler o arquivo .csv original
        with open(csv_file, 'r', encoding='utf-8') as file:
            content = file.readlines()

        # Substituir espaços em branco por vírgulas (somente entre palavras)
        updated_content = []
        for line in content:
            # Substituir os espaços por vírgulas
            updated_line = ','.join(line.split())
            updated_content.append(updated_line + '\n')

        # Escrever o conteúdo modificado no arquivo CSV
        with open(csv_file, 'w', encoding='utf-8') as file:
            file.writelines(updated_content)
        
        print(f"Espaços substituídos por vírgulas no arquivo CSV '{csv_file}'.")
    
    except Exception as e:
        print(f"Ocorreu um erro ao modificar o arquivo CSV: {e}")

# Função para adicionar cabeçalhos ao arquivo CSV
def add_headers_to_csv(csv_file):
    headers = [
        'source id', 'x', 'y',
        'RA coordinates in the ref frame', 'DEC coordinates in the ref frame', 
        'final total mag in WFC3/F275W', 'final photometric error in WFC3/F275W',
        'final total mag in WFC3/F336W', 'final photometric error in WFC3/F336W',
        'final total mag in WFC3/F438W', 'final photometric error in WFC3/F438W',
        'final total mag in WFC3/F555W', 'final photometric error in WFC3/F555W',
        'final total mag in WFC3/F814W', 'final photometric error in WFC3/F814W',
        'CI=mag(1px)-mag(3px) measured in the F555W. This catalogue contains only sources with CI>=1.35.',
        'best age in yr', 'max age in yr (within 68 %% confidence level)', 
        'min age in yr (within 68 %% confidence level)', 'best mass in solar masses',
        'max mass in solar masses (within 68 %% confidence level)', 
        'min mass in solar masses (within 68 %% confidence level)', 'best E(B-V)', 
        'max E(B-V) (within 68 %% confidence level)', 'min E(B-V) (within 68 %% confidence level)',
        'chi2 fit residual in F275W', 'chi2 fit residual in F336W', 'chi2 fit residual in F438W',
        'chi2 fit residual in F555W', 'chi2 fit residual in F814W', 'reduced chi2',
        'Q probability', 'Number of filter', 'class(mode)',
        'Final class(mean)'
    ]
    
    try:
        # Ler o conteúdo do arquivo .csv existente
        with open(csv_file, 'r', encoding='utf-8') as file:
            content = file.readlines()

        # Adicionar os cabeçalhos à primeira linha
        content.insert(0, ','.join(headers) + '\n')

        # Escrever o conteúdo de volta no arquivo CSV
        with open(csv_file, 'w', encoding='utf-8') as file:
            file.writelines(content)
        
        print(f"Cabeçalhos adicionados ao arquivo CSV '{csv_file}'.")
    
    except Exception as e:
        print(f"Ocorreu um erro ao adicionar os cabeçalhos: {e}")

def path_tab(galaxy='ngc3344'):
    # Possíveis valores para filter_name e n
    filter_names = ['wfc3', 'acs']
    n_values = [1, 2]
    
    # Itera sobre todas as combinações de filter_name e n
    for filter_name in filter_names:
        for n in n_values:
            tab_file = f'legus/tab_files/hlsp_legus_hst_{filter_name}_{galaxy}_multiband_v{n}_padagb-mwext-avgapcor.tab'
            
            # Verifica se o arquivo existe
            if os.path.exists(tab_file):
                return tab_file  # Retorna o caminho do arquivo encontrado
    
    # Caso não encontre nenhum arquivo correspondente, retorna uma mensagem ou None
    return None


tab_file = path_tab(galaxy)# Caminho para o arquivo .tab
csv_file = 'output/original.csv'  # Caminho para salvar o arquivo .csv

# Converter o arquivo .tab para .csv
tab_to_csv(tab_file, csv_file)

# Substituir os espaços por vírgulas no arquivo .csv
replace_spaces_in_csv(csv_file)

# Adicionar os cabeçalhos ao arquivo .csv
add_headers_to_csv(csv_file)