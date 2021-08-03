import mysql.connector
import random

db = mysql.connector.connect(
    host="localhost", user="root", passwd="root", database="pokusaj"
)

cursor = db.cursor()

topics = {
    1: "zivotinje",
    2: "transport",
    3: "boje",
    4: "lokacije",
    5: "ljudi",
    6: "odeca",
    7: "poslovi",
    8: "umetnost",
}


def generate_topics():
    for x in range(1, len(topics) + 1):
        print("{}) {}".format(x, topics[x]))


def user_choice():

    choice = "wrong"
    acceptable_range = range(1, len(topics) + 1)
    within_range = False

    print("Choose a topic: ")

    while choice.isdigit() == False or within_range == False:
        generate_topics()

        choice = input()

        if choice.isdigit() == False:
            print("That's not a number. Please try again.")

        if choice.isdigit():
            if int(choice) in acceptable_range:
                within_range = True
            else:
                print(
                    f"There is not that number. Please insert a number between 1 and {len(topics)}."
                )

    return int(choice)


table = user_choice()

table = topics[table]

countRowsQ = "SELECT COUNT(*) FROM {}".format(table)

cursor.execute(countRowsQ)

for x in cursor:
    numOfWords = x[0]

points = 0
array = list(range(1, numOfWords + 1))
random.shuffle(array)

for a in array:

    questionNumber = a

    wordSelectQ = "SELECT rec FROM {} WHERE id = {}".format(table, questionNumber)

    cursor.execute(wordSelectQ)

    for x in cursor:
        wordToTranslate = x[0]

        answerQ = "SELECT prevod FROM {} WHERE id = {}".format(table, questionNumber)

        cursor.execute(answerQ)

        for x in cursor:
            answer = x[0]

        translatedWord = input("Prevedi rec {}: ".format(wordToTranslate))

        if translatedWord.lower() == answer.lower():
            points += 1
        else:
            print("{} nije tacno prevod reci je {}".format(translatedWord, answer))


print("Broj vasih poena je {}/{}".format(points, numOfWords))
