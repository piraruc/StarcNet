# Define a lista de alvos (targets)
TARGETS=("eso486-g021" "ic4247"  
 "ic559" "ugc5139" "ngc1313-e" 
"ngc1313-w" "ngc1433" "ngc1566" "ngc1705" 
"ngc3274" "ngc3344" "ngc3351" "ngc3738" 
"ngc4242" "ngc4248" "ngc4395-n" "ngc4395-s" 
"ngc4449" "ngc4485" "ngc45" "ngc4656" 
"ngc5238" "ngc5253" "ngc5474" "ngc5477"
 "ngc628-c" "ngc628-e" "ngc6503" "ngc7793-e" 
 "ngc7793-w" "ugc1249" "ugc4305" "ugc4459"
  "ugc5340" "ugc685" "ugc695" "ugc7242"
  "ugc7408" "ugca281")

# Número de repetições (baseado no número de alvos)
REPEAT_COUNT=${#TARGETS[@]}

DOWNLOAD=${1:-0}
STARTTIME=$(date +%s)

mkdir -p legus/tab_files
mkdir -p legus/frc_fits_files
mkdir -p model
mkdir -p data
mkdir -p output

if [ -d "data/raw_32x32" ]; then rm -Rf data/raw_32x32; fi

# Loop para repetir o processo para cada target
for (( i=0; i<$REPEAT_COUNT; i++ ))
do
    # Define o target atual (o próximo da lista)
    CURRENT_TARGET=${TARGETS[$i]}
    
    # Atualiza o arquivo target.txt com o valor atual
    echo $CURRENT_TARGET > target.txt
    
    echo "-----------------------------------"
    echo "Repetindo a iteração $((i + 1)) de $REPEAT_COUNT"
    echo "Target atual: $CURRENT_TARGET"
    
    # Se DOWNLOAD=1, baixa os arquivos novamente
    if [ $DOWNLOAD -eq 1 ]
    then
        echo "Baixando mosaicos de galáxias..."
        wget -P legus/frc_fits_files -q --show-progress -i frc_fits_links.txt
        
        cd legus/frc_fits_files/
        ls ./*.tar.gz | xargs -n1 tar -xvzf
        rm -r ./*.tar.gz
        cd ../../
    fi

    # Chama o script de criação de dataset
    bash create_dataset.sh 1
    
    # Classificando os objetos
    echo "Classificando objetos..."
    python src/test_net.py \
            --test-batch-size 64 \
            --data_dir data/ \
            --dataset raw_32x32 \
            --save_dir model/ \
            --cuda --gpu 0 \
            --checkpoint starcnet.pth
    
    python src/preds2output.py
    python src/tab_to_csv.py
    python src/confusion_matrix.py
    python src/fits2png.py
    # Calcular o tempo de execução
    ENDTIME=$(date +%s)
    echo "---------------------------------------------"
    echo "| Fim da classificação | tempo: $(($ENDTIME - $STARTTIME))s"
    echo "---------------------------------------------"
    
    
    # Resetando o tempo de início para a próxima iteração
    STARTTIME=$(date +%s)
done

echo "Processo concluído após $REPEAT_COUNT iterações."
