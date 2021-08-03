import mysql.connector
import random


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

countRowsQ = "SELECT COUNT(*) FROM {}".format(table)

cursor.execute(countRowsQ)

for x in cursor:
	numOfWords = x[0]

points = 0
array = list(range(1,numOfWords+1))
random.shuffle(array)

for a in array:

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