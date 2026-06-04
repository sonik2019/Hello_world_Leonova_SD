#!/bin/bash

echo "Обработка файла sequences.txt..."
echo "Замена пробелов на табуляции..."

cp sequences.txt sequences.txt.bak

sed -i 's| |\t|g' sequences.txt

echo "Замена выполнена!"
echo ""
echo "Результат:"
echo "-----------------------------------"
cat sequences.txt
echo "-----------------------------------"
