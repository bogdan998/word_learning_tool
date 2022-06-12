from asyncore import read
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

cursor = db.cursor()

class User():

    def __init__(self,first_name,last_name,username,email,password,role=2):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.password = password
        self.role = role

    def add_user(self):
        
        q = "INSERT INTO user (first_name,last_name,username,email,password,role_id) VALUES (%s,%s,%s,%s,%s,%s)"
        values = (self.first_name.capitalize(),self.last_name.capitalize(),self.username,self.email,self.password,self.role)

        cursor.execute(q,values)
        db.commit()

        clear()
        print('User added.\n')
        print("Please log in.")
        menu()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

def welcome():
    print("Welcome to word translation training.")
    print('\n\n\n')
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
    q3 = "SELECT role_id FROM user WHERE username = '{}' AND password = '{}' ".format(username_from_db,passwd_from_db)
    global role_id 
    cursor.execute(q3)
    for x in cursor:
        role_id = x[0]
    # if role_id == 1 adminMenu elif user == 2 studentMenu...
    if role_id == 1:
        admin_menu()
    elif role_id == 2:
        student_menu()
    elif role_id == 3:
        instructor_menu()

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

def admin_menu():
    print("1. Add user")
    print("2. Remove user")
    print("3. Reset users score")
    print("4. Add topic")
    print("5. Add word")    
    print("\n0) Exit the program :(") # --> this can be a dictionary, use del dict['key'] to remove 
                                      # unnecessary keys and dict['key'] = 'value' to add key-value

    choice = input()
    if choice.isnumeric():
        if int(choice) == 1:
            add_user()
        elif int(choice) == 2:
            remove_user()
        elif int(choice) == 3:
            reset_score()
        elif int(choice) == 4:
            add_topic()
        elif int(choice) == 5:
            add_word()
        elif int(choice) == 0:
            quit()
        else:
            print("That's not an option. Please enter a valid choice.")
    if not choice.isnumeric():
        print("That's not an option. Please enter a valid choice.")
        admin_menu()
        


def instructor_menu():
    print("You are in the instructor_menu()")


def student_menu():
    print("1. Choose a topic")
    print("2. Add a word")
    print("3. See your score")
    print("\n0) Exit the program :(")

    choice = input()
    if choice.isnumeric():
        if int(choice) == 1:
            start_training()
        elif int(choice) == 2:
            add_word()
        elif int(choice) == 3:
            check_score()
        elif int(choice) == 0:
            quit()
        else:
            print("That's not an option. Please enter a valid choice.")
            student_menu()
    if not choice.isnumeric():
        print("That's not an option. Please enter a valid choice.")
        student_menu()
    
def read_from_database(table_name: str):
    counter = 1
    dict = {}
    cursor.execute(f'SELECT name FROM {table_name}')
    for x in cursor:
        # print(f'{counter})',x[0])
        dict.update({int('{}'.format(counter)): '{}'.format(x[0])})
        counter += 1
    return dict

topics = read_from_database('topic')
languages = read_from_database('languages')

def space_check(word):
    word = word.split()
    word = " ".join(word)

    return word

def add_word():
    print("inside the add_word()")


def check_score():
    print("inside the check score")

def add_user():
    print("inside the add_user()")

def remove_user():
    print("inside the remove_user()")

def reset_score():
    print("inside the remove_score()")

def add_topic():
    print("inside the add_topic()")

def generate_choice_list(var):
    for x in range(1, len(var) + 1):
        print("{}) {}".format(x, var[x].capitalize()))
    print('\n\n0) for back')
    
def user_choice(var):

    choice = "wrong"
    # acceptable_range = range(len(var)) #(1, len(topics) + 1)
    acceptable_range = range(1,len(var) + 1)
    within_range = False

    while choice.isdigit() == False or within_range == False:
        generate_choice_list(var)

        choice = input()
        if choice == 0:
            quit()  # student_menu() # if choice == 0 and role == student return student_menu() if role == admin return admin_menu()
        if choice.isdigit() == False:
            print("That's not a number. Please try again.")

        if choice.isdigit():
            if int(choice) in acceptable_range:
                within_range = True
            else:
                print(
                    f"There is not that number. Please insert a number between 1 and {len(var)}."
                )

    return int(choice)

def chose_language():
    print("Choose from which language you want to translate: ")
    translate_from = user_choice(languages)
    print("Choose from which language you want to translate: ")
    translate_to = user_choice(languages)

    return translate_from, translate_to


def start_training():
    
    while True:
        translate_from, translate_to = chose_language()
        table = user_choice(topics)
        count_rows_q = "SELECT COUNT(*) FROM words WHERE topic_id = {} and language_id = {}".format(table, translate_from)

        cursor.execute(count_rows_q)

        for x in cursor:
            num_of_words = x[0]

        points = 0
        array = []

        cursor.execute("SELECT word_id FROM words WHERE topic_id = {} and language_id = {}".format(table, translate_from))

        for x in cursor:
            array.append(x[0])

        random.shuffle(array)

        for a in array:

            question_number = a

            word_select_q = "SELECT word FROM words WHERE word_id = {} and topic_id = {} and language_id = {}".format(question_number,table,translate_from)

            cursor.execute(word_select_q)

            for x in cursor:
                word_to_translate = x[0]

                answer_q = "select word from words where topic_id = {} and language_id = {} and word_id in(SELECT word_id from words where word = '{}')".format(table,translate_to,word_to_translate)

                cursor.execute(answer_q)

                for x in cursor:
                    answer = x[0]

                translated_word = input("Prevedi rec {}: ".format(word_to_translate))

                translated_word = space_check(translated_word)

                if translated_word.lower() == answer.lower():
                    points += 1
                else:
                    print("{} nije tacno prevod reci je {}".format(translated_word, answer))

        if table == 0:
            if role_id == 1:
                admin_menu()
            elif role_id == 2:
                student_menu()
            elif role_id == 3:
                instructor_menu()

        print("Number of your points: {}/{}".format(points, num_of_words))
        print('Do you want to play again? (yes or no): ')
        if not input('> ').lower().startswith('y'):
            break


clear()
welcome()
menu()
print('Thanks for playing!')