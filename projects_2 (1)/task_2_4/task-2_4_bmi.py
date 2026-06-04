weight = float(input("Введите вес (кг): "))
height = float(input("Введите рост (м): "))
bmi = weight / (height ** 2)

print ("-*-Отчёт о состоянии здоровья-*-")
print (f"Рост:\t{height:.1f} см")
print (f"Вес:\t{weight:.1f} кг")
print(f"Индекс массы тела пациента: {bmi:.2f}")