phenotype_1 = input("Введите фенотип группы крови (I, II, III, IV): ").strip().upper()
phenotype_2 = input("Введите фенотип группы крови донора (I, II, III, IV): ").strip().upper()
if phenotype_1 == "I":
    print("Группа крови: 0 (I)")
elif phenotype_1 == "II":
    print("Группа крови: A (II)")
elif phenotype_1 == "III":
    print("Группа крови: B (III)")
elif phenotype_1 == "IV":
    print("Группа крови: AB (IV)")
else:
    print("Такой группы крови не существует")

if phenotype_1 == phenotype_2:
    print ("Кровь подходит для переливания")
elif phenotype_2 == "I":
    print ("Кровь подходит для переливания")
else:
    print ("Кровь не подходит для переливания")