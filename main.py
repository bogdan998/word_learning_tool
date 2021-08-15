import mysql.connector
import random

<<<<<<< HEAD
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
    9: "drustvo",
    10: "pice",
    11: "hrana"
}

def space_check(word):
    word = word.split()
    word = " ".join(word)

    return word

def generate_topics():
    for x in range(1, len(topics) + 1):
        print("{}) {}".format(x, topics[x].capitalize()))


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

=======

db = mysql.connector.connect(
	host = 'localhost',
	user = 'root',
	passwd = 'root',
	database = 'pokusaj'
	)
while True:
	topic = input("Choose your topic:\n1) Boje\n2) Lokacije\n3) Zivotinje\n4) Transport \n5) Ljudi\n\n>")
	if topic == '1':
		table = 'boje'
		break
	if topic == '2':
		table = 'lokacije'
		break
	if topic == '3':
		table = 'zivotinje'
		break
	if topic == '4':
		table = 'transport'
		break
	if topic == '5':
		table = 'ljudi'
		break
	else:
		print("Thats not an option. Please try again \n\n>")

cursor = db.cursor()

>>>>>>> 2907f23f9192acbc533a0441fe27b0dc3122c925
countRowsQ = "SELECT COUNT(*) FROM {}".format(table)

cursor.execute(countRowsQ)

for x in cursor:
<<<<<<< HEAD
    numOfWords = x[0]

points = 0
array = list(range(1, numOfWords + 1))
=======
	numOfWords = x[0]

points = 0
array = list(range(1,numOfWords+1))
>>>>>>> 2907f23f9192acbc533a0441fe27b0dc3122c925
random.shuffle(array)

for a in array:

<<<<<<< HEAD
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

        translatedWord = space_check(translatedWord)

        if translatedWord.lower() == answer.lower():
            points += 1
        else:
            print("{} nije tacno prevod reci je {}".format(translatedWord, answer))


print("Broj vasih poena je {}/{}".format(points, numOfWords))
=======
	questionNumber = a

	wordSelectQ = "SELECT rec FROM {} WHERE id = {}".format(table,questionNumber)

	cursor.execute(wordSelectQ)

	for x in cursor:
		wordToTranslate = x[0]

		answerQ = "SELECT prevod FROM {} WHERE id = {}".format(table,questionNumber)

		cursor.execute(answerQ)

		for x in cursor:
			answer = x[0]

		translatedWord = input("Prevedi rec {}: ".format(wordToTranslate))

		if translatedWord.lower() == answer.lower():
			points += 1
		else:
			print("{} nije tacno prevod reci je {}".format(translatedWord,answer))


print("Broj vasih poena je {}/{}".format(points,numOfWords))
>>>>>>> 2907f23f9192acbc533a0441fe27b0dc3122c925
