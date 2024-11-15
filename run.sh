# Define a lista de alvos (targets)
TARGETS=("eso486-g021" "ic4247" "ngc628-c" "ngc628-e" "ngc6503" "ngc3274" "ngc3351" "ngc3738" "ngc4248" "ngc4395" "ngc3351" "ngc3351" "ngc3351" "ngc3351"
 "ngc3351" "ngc3351" "ngc3351" "ngc3351" "ngc3351" "ngc3351" "ngc3351" "ngc3351" "ngc3351" "ngc3351" "ngc3351" "ngc3351" "ngc3351" "ngc3351" "ngc3351")

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
    
    # Calcular o tempo de execução
    ENDTIME=$(date +%s)
    echo "---------------------------------------------"
    echo "| Fim da classificação | tempo: $(($ENDTIME - $STARTTIME))s"
    echo "---------------------------------------------"
    
    python src/tab_to_csv.py
    python confusion_matrix.py
    # Resetando o tempo de início para a próxima iteração
    STARTTIME=$(date +%s)
done

echo "Processo concluído após $REPEAT_COUNT iterações."
