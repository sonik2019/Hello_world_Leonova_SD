#!/bin/bash

STUDENTS_FILE="students.txt"

if [ ! -f "$STUDENTS_FILE" ]; then
    echo "Ошибка: Файл $STUDENTS_FILE не найден!"
    exit 1
fi

echo "========================================="
echo "Обработка файла: $STUDENTS_FILE"
echo "========================================="

echo "1. Имена студентов:"
echo "-----------------------------------------"
cut -d ' ' -f 1 "$STUDENTS_FILE"
echo ""

echo "2. Оценки студентов:"
echo "-----------------------------------------"
cut -d ' ' -f 2 "$STUDENTS_FILE"
echo ""


echo "3. Номер строки и имя студента:"
echo "-----------------------------------------"
awk '{print NR, $1}' "$STUDENTS_FILE"
echo ""

echo "========================================="
