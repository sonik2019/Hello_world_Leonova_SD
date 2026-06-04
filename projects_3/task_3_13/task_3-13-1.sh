#!/bin/bash

echo "Замена пути в файле settings.php..."
echo "Старый путь: /var/lib/mysql/data"
echo "Новый путь: /mnt/ssd/mysql"


cp settings.php settings.php.bak

sed -i 's|/var/lib/mysql/data|/mnt/ssd/mysql|g' settings.php

echo "Замена выполнена!"
echo "Проверьте результат:"
grep "db_data_path" settings.php
