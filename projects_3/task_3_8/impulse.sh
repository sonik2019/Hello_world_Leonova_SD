#!/bin/bash

if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Ошибка: Недостаточно аргументов!"
    echo "Использование: ./impulse.sh <имя_гена> <уровень_экспрессии>"
    echo "Пример: ./impulse.sh BRCA1 150"
    exit 1
fi

GENE_NAME=$1
EXPRESSION_LEVEL=$2

if ! [[ "$EXPRESSION_LEVEL" =~ ^-?[0-9]+$ ]]; then
    echo "Ошибка: Уровень экспрессии должен быть целым числом!"
    exit 1
fi

echo "Экспрессия гена [$GENE_NAME] составляет [$EXPRESSION_LEVEL] единиц"
