dna = input("Введите последовательность ДНК: ").upper()

count_A = dna.count("A")
count_T = dna.count("T")
count_C = dna.count("C")
count_G = dna.count("G")
count_nucleus = len(dna)

print(f"Подсчёт нуклеотидов: {count_nucleus}")
print(f"A: {count_A}")
print(f"T: {count_T}")
print(f"C: {count_C}")
print(f"G: {count_G}")