#!/bin/bash

check_root() {

if [ "$EUID" -eq 0 ]; then
        echo "OK: Скрипт запущен от имени суперпользователя (root)"
        return 0
    else
        echo "ОШИБКА: Этот скрипт должен запускаться от имени суперпользователя!"
        echo "Пожалуйста, используйте: sudo ./check_root.sh"
        exit 1
    fi
}

check_root

echo "Продолжаем выполнение скрипта..."
echo "Ваш UID: $EUID"


