import mysql.connector
import random
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

db = mysql.connector.connect(
    host = config['mysql']['host'],
	user = config['mysql']['user'],
	passwd = config['mysql']['passwd'],
	db = config['mysql']['db']
)

cursor = db.cursor()

cursor.execute('SELECT name FROM topic')
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

while True:
    table = user_choice()

    

    countRowsQ = "SELECT COUNT(*) FROM topic_item WHERE topic_id = {}".format(table)

    cursor.execute(countRowsQ)

    for x in cursor:
        numOfWords = x[0]

    points = 0
    array = []

    cursor.execute("SELECT id FROM topic_item WHERE topic_id = {}".format(table))

    for x in cursor:
        array.append(x[0])

    random.shuffle(array)

    for a in array:

        questionNumber = a

        wordSelectQ = "SELECT word FROM topic_item WHERE id = {}".format(questionNumber)

        cursor.execute(wordSelectQ)

        for x in cursor:
            wordToTranslate = x[0]

            answerQ = "SELECT translation FROM topic_item WHERE id = {}".format(questionNumber)

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
    print('Do you want to play again? (yes or no): ')
    if not input('> ').lower().startswith('y'):
        break

print('Thanks for playing!')