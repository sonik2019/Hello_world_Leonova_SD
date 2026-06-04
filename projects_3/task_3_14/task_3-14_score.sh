#!/bin/bash

STUDENTS_FILE="students.txt"

if [ ! -f "$STUDENTS_FILE" ]; then
    echo "Ошибка: Файл $STUDENTS_FILE не найден!"
    exit 1
fi

echo "========================================="
echo "Анализ успеваемости студентов"
echo "========================================="

echo "1. Студенты с оценкой ВЫШЕ 80:"
echo "-----------------------------------------"
awk '$2 > 80 {print $1 " - " $2}' "$STUDENTS_FILE"
if [ $? -ne 0 ] || [ -z "$(awk '$2 > 80 {print $0}' "$STUDENTS_FILE")" ]; then
    echo "Нет студентов с оценкой выше 80"
fi
echo ""

echo "2. Студенты с оценкой НИЖЕ 70:"
echo "-----------------------------------------"
awk '$2 < 70 {print $1 " - " $2}' "$STUDENTS_FILE"
if [ $? -ne 0 ] || [ -z "$(awk '$2 < 70 {print $0}' "$STUDENTS_FILE")" ]; then
    echo "Нет студентов с оценкой ниже 70"
fi
echo ""

echo "3. Первая строка файла:"
echo "-----------------------------------------"
head -n 1 "$STUDENTS_FILE"
echo ""

echo "========================================="
