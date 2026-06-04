#!/bin/bash

if [ -z "$1" ]; then
    echo "Ошибка: Укажите путь к папке с FASTA-файлами"
    echo "Использование: ./nucleotides_count.sh <путь_к_папке>"
    exit 1
fi

FASTA_DIR="$1"
if [ ! -d "$FASTA_DIR" ]; then
    echo "Ошибка: Папка '$FASTA_DIR' не существует!"
    exit 1
fi

cd "$FASTA_DIR" || exit 1

echo "=========================================================="
printf "%-20s %-8s %-8s %-8s %-8s\n" "Файл" "A" "T" "G" "C"
echo "=========================================================="

for file in *.fasta; do

if [ ! -f "$file" ]; then
        echo "Файлы *.fasta не найдены в папке '$FASTA_DIR'"
        exit 1
    fi

if [ ! -s "$file" ]; then
        continue
    fi

 SEQUENCE=$(grep -v "^>" "$file" | tr -d '\n' | tr -d '\r')

 COUNT_A=$(echo "$SEQUENCE" | grep -o "A" | wc -l)
    COUNT_T=$(echo "$SEQUENCE" | grep -o "T" | wc -l)
    COUNT_G=$(echo "$SEQUENCE" | grep -o "G" | wc -l)
    COUNT_C=$(echo "$SEQUENCE" | grep -o "C" | wc -l)

  printf "%-20s %-8s %-8s %-8s %-8s\n" "$file" "$COUNT_A" "$COUNT_T" "$COUNT_G" "$COUNT_C"
done

echo "=========================================================="
