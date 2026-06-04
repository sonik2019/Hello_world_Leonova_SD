#!/bin/bash

STUDENTS_FILE="students.txt"

if [ ! -f "$STUDENTS_FILE" ]; then
    echo "Ошибка: Файл $STUDENTS_FILE не найден!"
    exit 1
fi

echo "========================================="
echo "Статистический анализ оценок студентов"
echo "========================================="

echo "1. Сумма всех оценок:"
echo "-----------------------------------------"
SUM=$(awk '{sum+=$2} END {print sum}' "$STUDENTS_FILE")
echo "Сумма: $SUM"
echo ""

echo "2. Средняя оценка:"
echo "-----------------------------------------"
AVG=$(awk '{sum+=$2} END {printf "%.2f", sum/NR}' "$STUDENTS_FILE")
echo "Средняя оценка: $AVG"
echo ""

echo "3. Максимальная оценка:"
echo "-----------------------------------------"
MAX=$(awk 'NR==1{max=$2} $2>max{max=$2} END {print max}' "$STUDENTS_FILE")
echo "Максимальная оценка: $MAX"

echo ""
echo "4. Минимальная оценка (дополнительно):"
echo "-----------------------------------------"
MIN=$(awk 'NR==1{min=$2} $2<min{min=$2} END {print min}' "$STUDENTS_FILE")
echo "Минимальная оценка: $MIN"

echo ""
echo "========================================="
