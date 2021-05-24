import random

peeps_list = []
peeps = int(input("Enter the number of friends joining (including you): "))

if peeps <= 0:
    print("\nNo one is joining for the party")
    exit()

print("\nEnter the name of every friend (including you), each on a new line: ")

for i in range(peeps):
    name = input()
    peeps_list.append(name)

print()
bill = int(input("Enter the total bill value:"))
print()
lucky = input('Do you want to use the "Who is lucky?" feature? Write Yes/No: ')

if lucky.lower() == "yes":
    winner = random.choice(peeps_list)
    print(f"\n{winner} is the lucky one!")
    part = round(bill / (peeps - 1), 2)
    peeps_dic = dict.fromkeys(peeps_list, 0)
    for n in peeps_dic:
        if n != winner:
            peeps_dic[n] = part
        else:
            peeps_dic[n] = 0
    print(peeps_dic)
elif lucky.lower() == "no":
    print("\nNo one is going to be lucky")
    part = round(bill / peeps, 2)
    peeps_dic = dict.fromkeys(peeps_list, part)
    print()
    print(peeps_dic)