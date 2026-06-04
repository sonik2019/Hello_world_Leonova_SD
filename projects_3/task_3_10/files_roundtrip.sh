#!/bin/bash

echo "=== Часть 1: Создание файлов (цикл for) ==="

for i in {1..10}; do
    FILENAME="test${i}.txt"
    touch "$FILENAME"
    echo "Создан файл: $FILENAME"
done

echo ""
echo "=== Список созданных файлов ==="
ls -la test*.txt 2>/dev/null
echo ""

echo "=== Часть 2: Удаление файлов в обратном порядке (цикл while) ==="

counter=10
while [ $counter -ge 1 ]; do
    FILENAME="test${counter}.txt"
    

 if [ -f "$FILENAME" ]; then
        rm "$FILENAME"
        echo "Удалён файл: $FILENAME"
    else
        echo "Файл не найден: $FILENAME"
    fi

 counter=$((counter - 1))
done

echo ""
echo "=== Проверка: остались ли файлы? ==="
ls -la test*.txt 2>/dev/null || echo "Файлов test*.txt не осталось"

echo ""
echo "Скрипт завершен."
