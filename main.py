import mysql.connector
import random
import configparser
import os
from os import system, name
from getpass import getpass
import pathlib
import sys

config = configparser.ConfigParser()
path = pathlib.Path(__file__).parent.resolve()
config.read(os.path.join(path,'config.ini'))

db = mysql.connector.connect(
    host = config['mysql']['host'],
	user = config['mysql']['user'],
	passwd = config['mysql']['passwd'],
	db = config['mysql']['db']
)
# db = mysql.connector.connect(
#     host = 'localhost',
#     user = 'root',
#     passwd = 'root',
#     db = 'database'
# )
cursor = db.cursor()
class User():

    def __init__(self,firstName,lastName,username,email,password):
        self.firstName = firstName
        self.lastName = lastName
        self.username = username
        self.email = email
        self.password = password

    def add_user(self):
        
        q = "INSERT INTO user (first_name,last_name,username,email,password) VALUES (%s,%s,%s,%s,%s)"
        values = (self.firstName.capitalize(),self.lastName.capitalize(),self.username,self.email,self.password)

        cursor.execute(q,values)
        db.commit()

        clear()
        print('User added.\n')
        print("Please log in.")
        menu()

    def __str__(self):
        return f"{self.firstName} {self.lastName}"

def welcome():
    print("Welcome to word translation training.")
    print('\n\n\n\n\n')
    input('Press Enter to continue...')
    clear()

def clear():

    if name == 'nt':
        _ = system('cls')

def create_account():
    
    first_name = input("Enter your first name: ")
    
    last_name = input("Enter your last name: ")
    
    username = input("Enter your username: ")
    
    email = input("Enter your email: ")

    password = input("Enter your password: ")
    if len(first_name) == 0  or len(last_name) == 0 or len(username) == 0 or len(email) == 0 or len(password) == 0:
    
        print("You must enter all data.")
        print("Please try again.")
        create_account()
    else:
        global user
        user = User(first_name,last_name,username,email,password)


def login():

    username_from_user = input("Enter your username: ")
    passwd_from_user = input("Enter your password: ")

    q1 = "SELECT username FROM user WHERE password = '{}'".format(passwd_from_user)
    q2 = "SELECT password FROM user WHERE username = '{}'".format(username_from_user) 
    # q3 = "SELECT first_name FROM user WHERE username = {}".format(username_from_user)

    username_from_db = 'wrong'
    cursor.execute(q1)
    for x in cursor:
        username_from_db = x[0]

    passwd_from_db = 'wrong'
    cursor.execute(q2)
    for x in cursor:
        passwd_from_db = x[0]
    
    if passwd_from_db is None:
        print("Invalid password or username. Please try again.")
        login()
    
    while True:
        if username_from_db == username_from_user and passwd_from_db == passwd_from_user:
            print(f"Welcome {username_from_db}")
        if username_from_db != username_from_user or passwd_from_db != passwd_from_user:
            print("Invalid password or username. Please try again.")
            
            login()
        break
    # if role_id == 1 adminMenu elif user == 2 studentMenu...
    start_training()

def menu():

    print('1. Login')
    print('2. Create account')
    choice = input()
    if choice.isnumeric():
        if int(choice) == 1:
            login()
        elif int(choice) == 2:
            create_account()    
            user.add_user()
        else:
            print("That's not an option. Please enter a valid choice.")
            menu()
    if not choice.isnumeric():
        print("That's not an option. Please enter a valid choice.")
        menu() 

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
    print('\n\n0) for exit')

def user_choice():

    choice = "wrong"
    acceptable_range = range(len(topics)) #(1, len(topics) + 1)
    within_range = False

    print("Choose a topic: ")

    while choice.isdigit() == False or within_range == False:
        generate_topics()

        choice = input()
        if choice == 0:
            exit()
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

def start_training():
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


clear()
welcome()
menu()
print('Thanks for playing!')