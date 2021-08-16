import mysql.connector
import random
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

db = mysql.connector.connect(
    host = '{}'.format(config['mysql']['host']),
	user = '{}'.format(config['mysql']['user']),
	passwd = '{}'.format(config['mysql']['passwd']),
	db = '{}'.format(config['mysql']['db'])
)

cursor = db.cursor()

cursor.execute('show tables')
topics = {}
counter = 1

for x in cursor:
	# print(f'{counter})',x[0])
	topics.update({int('{}'.format(counter)): '{}'.format(x[0])})
	counter += 1

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

        translatedWord = space_check(translatedWord)

        if translatedWord.lower() == answer.lower():
            points += 1
        else:
            print("{} nije tacno prevod reci je {}".format(translatedWord, answer))


print("Number of your points: {}/{}".format(points, numOfWords))
