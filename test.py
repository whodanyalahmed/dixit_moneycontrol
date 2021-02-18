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


# d = GetCF("1Hhd2acGqabwFKnHfT3YW5qqBAKNBkQKw1FQPoRTb8fM")
# print(d)



from screen import Fill_data


d = Fill_data("https://www.screener.in/screens/59/Magic-Formula")
print(d)