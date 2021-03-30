import random

def convertlist(s):

    newstr = ""
    for i in s:
        newstr += i
    return newstr

def checklist(answerlst, answer):

    repeated = False
    for i in answerlst:
        if i == answer:
            repeated = True
    return repeated

def win(wordlst):
    win = True
    for i in wordlst:
        if i == "-":
            win = False
    return win

names = ["python", "kotlin", "java", "javascript"]
word = random.choice(names)
char_list = list("-" * len(word))
attempts = 8
answer_list = []

print("H A N G M A N\n")
print(convertlist(char_list))
option = input('Type "play" to play the game, "exit" to quit:')

while option == "play":

    while attempts > 0:

        if win(char_list):
            print("You guessed the word!")
            print("You survived!")
            break

        answer = input("Input a letter:")
        aux = True
        boolattempts = False
        if len(answer) != 1:
            print("You should input a single letter")
            aux = False
        elif not answer.isalpha() or not answer.islower():
            print("Please enter a lowercase English letter")
            aux = False
        else:
            if checklist(answer_list, answer):
                print("You've already guessed this letter")
                aux = False
            else:
                for i in range(0, len(word)):
                    if answer == word[i]:
                        char_list[i] = answer
                        aux = False

        if aux:
            print("That letter doesn't appear in the word")
            boolattempts = True
            aux = False

        if boolattempts:
            attempts -= 1

        if attempts == 0:
            print("You lost!")
            break
        else:
            print()
            print(convertlist(char_list))

        answer_list.append(answer)

    option = input('Type "play" to play the game, "exit" to quit:')





