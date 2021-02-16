name = "Pooja Entertainment & Films Ltd"
names= name.split(" ")
print(names)
names_len = len(names)

if(names_len > 1):    
    for part_name in range(len(names[1])):
        print(part_name)
        print(part_name-1)
        print("Trying on: " + names[0] + " " + names[1][:-part_name-1])
else:
    print(name)