journal_lab = "Электронный лабораторный журнал"
name = input ("Введите ФИО исследователя: ")
date = ("Введите дату исследование: ")
experiment = input ("Введите эксперимент: ")
conclusion = input ("Напишите вывод: ")
minus = "-" * 41
with open ("journal.txt", "w", encoding="utf-8") as journal:
   journal.write (f"{minus}\n")
   journal.write (f"| {journal_lab}\t |\n")
   journal.write (f"{minus}\n")
   journal.write (f"| ФИО исследователя: {name}\t\t |\n")
   journal.write (f"| дата: {date}\t |\n")
   journal.write (f"| эксперимент: {experiment}\t\t |\n")
   journal.write (f"{minus}\n")
   journal.write (f"| Вывод: {conclusion}\t\t |\n")
   journal.write (f"{minus}\n")


   
   