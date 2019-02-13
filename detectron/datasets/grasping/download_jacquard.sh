#! /bin/bash

for i in $(seq -f "%01g" 1 11)
do
    echo $i

    wget https://jacquard.liris.cnrs.fr/data/Download/Jacquard_Dataset_$i.zip -P jacquard/
    unzip jacquard/Jacquard_Dataset_$i.zip -d jacquard/Jacquard_Dataset_$i/
    rm jacquard/Jacquard_Dataset_$i.zip

done
