operator_name = input("Введите имя оператора: ")
sensor_number = input("Введите текущее значение давления (Па): ")
with open("sensor_log.txt", "w", encoding="utf-8") as report:
    report.write(f"Введите имя оператора: {operator_name}\n")
    report.write(f"Введите текущее значение давления (Па): {sensor_number}")
    print ("Данные успешно сохранены в sensor_log.txt")