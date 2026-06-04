volume = float(input("Введите нужную массу раствора"))
salt_mass = volume * 0.009
lines = '-' * 23
with open("recipe.txt", "w", encoding="utf-8") as file:
    file.write("ОТЧЕТ ПО ПРИГОТОВЛЕНИЮ:\n")
    file.write(f"{lines}\n")
    file.write(f"Общий объем:\t{volume} мл\n")
    file.write(f"Масса соли:\t{salt_mass:.2f} г\n")
    file.write(f"Объем воды:\t{volume} мл")
