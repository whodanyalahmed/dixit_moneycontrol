# name = "Pooja Entertainment & Films Ltd"
# names= name.split(" ")
# print(names)
# names_len = len(names)

# if(names_len > 1):    
#     for part_name in range(len(names[1])):
#         if(part_name == len(names[1])):
#             break
#         else:
#             if(names[1][:-part_name-1] == ""):
#                 break
#             else:
#                 print("Trying on: " + names[0] + " " + names[1][:-part_name-1])
# else:
#     print(name)



from spread import GetCF
cf = ["-1.64","-1.49","-2.2","-0.31","-0.36"]
if(len(cf) >= 10 ):
    cf = cf[-10:]
else:
    len_cf = len(cf)
    remaining = 10-len_cf
    d_list = [' ']*remaining
    for e in d_list:
        cf.insert(0,e)
cf_format = []
cf_format.append(cf)
print(cf_format)
# d = GetCF("1Hhd2acGqabwFKnHfT3YW5qqBAKNBkQKw1FQPoRTb8fM")
# print(d)