nutritional_environment = input ("Введите название питательной среды: ")
agar_concentration = input ("Введите концентрацию агара в %: ")
sterilization_temperature = input ("Введите температуру стерилизцаии: ")
with open ("recipe.txt", "w", encoding="utf-8") as report:
    report.write(f"\t{nutritional_environment}\n")
    report.write(f"Концентрация агара:\t{agar_concentration}\n")
    report.write(f"Температура стерилизации:\t{sterilization_temperature}\n")
    print ("Файл 'recipe.txt' ")