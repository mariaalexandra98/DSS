import csv
import os
from random import randrange


def write_to_csv(*argv):
    with open("rezultate.csv", 'a', newline='') as file:
        writer = csv.writer(file)
        file_is_empty = os.stat('rezultate.csv').st_size == 0
        if file_is_empty:
            writer.writerow(["numar_generat", "numar_incercare", "numar_introdus", "success"]) #eroare in cazul in care folosesc diacritice
            writer.writerow(argv)
        else:
            writer.writerow(argv)


welcome_message = "Hei hei! Mă gândesc la un număr între 1 și 20... Reușești să îl ghcești din 5 încercări?"
print(welcome_message)


def guess_the_number():
    random_number = randrange(1, 20)
    for i in range(1, 6):
        success_state = False
        picked_number = input("\nÎncercarea numărul " + str(i) + ".\nNumărul ales de tine este...: ")
        if picked_number.isdigit() and 1 <= int(picked_number) <= 20:
            if int(picked_number) < random_number:
                print("Hmm... Numărul la care m-am gândit este mai mare decât " + str(picked_number))
            elif int(picked_number) > random_number:
                print("Numărul la care m-am gândit este mai mic decât " + str(picked_number))
            else:
                print("\nGG. Ai reușit să ghicești numărul din " + str(i) + " încercări")
                success_state = True
                break
        else:
            print("Valoarea aleasa trebuie sa apartina intervalului [1, 20]!")
    print("\nJocul s-a terminat!")
    write_to_csv(random_number, i, picked_number, success_state)


guess_the_number()
