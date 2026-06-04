seq = [ "ATATACGCGTA", "CTTCGGNGGA" ] 
combined = seq[0] + seq[1]
print (combined)
print ("=" * 20)
for name in seq:
    print (name)
    for letter in name:
        print(letter) 
print ("Цикл выполнен")