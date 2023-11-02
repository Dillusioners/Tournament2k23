from getpass import getpass
import json
import os
from platform import system as sys
from time import sleep
from random import randint
from datetime import datetime
import pprint
import requests

# Python 3.10 and later supported ONLY

# function to reduce syntax in the actual class
def sleeping_print(text: str, duration: int = 2):
    print(text)
    sleep(duration)

# function to clear the terminal
def clear():
    # if the os is Windows
    if sys() == 'Windows':
        os.system('cls')
    
    else:
        os.system('clear')


# class for secure account system
class LoginSecurity:
    # constructor
    def __init__(
            self, *,
            online_storage=True, # whether accounts will be stored in API or in user's drive
            database='USERS', # the default database where the accounts will be stored
            file_folder='login_files', # folder for logs and account files
            file_name='accounts.json', # account file
            logs_file='logs.txt', # logs file
            clear_terminal=True, # bool to store whether the terminal will be cleared beforehand
            timeout_duration=30, # amount of time (in sec) user is timed out for incorrect password
            timeout_tries=3 # tries before the user is timed out
        ):
        # stores whether the user is currently logged in or not
        self.__logged_in = False

        # stores the username of the currently logged used
        self.__current_user = ''

        # stores all user accounts
        # key -> string (username), value -> string (password)
        self.__accounts = {}

        # the database in which the accounts will be stored
        self.__database = database

        # amount of seconds of timeout if the user gets
        # the password wrong in timeout_tries amount
        self.timeout_duration = timeout_duration
        self.timeout_tries = timeout_tries

        # configures whether the terminal will be cleared beforehand or not
        self.clear_terminal = clear_terminal

        # stores whether the user data will be stored in the device or in the API
        # if True, then the user data will be stored in the API
        # if False, then data will be stored in json files inside the user's desktop
        self.__online_storage = online_storage

        # the API which is used for online accounts storage
        self.__api = 'http://snowflakedillusionersdb.pythonanywhere.com'

        # the key which is required for encryption and decryption of passwords

        # this specific range of keys is selected because it facilitates the encryption
        # as it allows only 4-digit numbers to generate when used in encryption

        # random value used to facilitate file-to-file and user-to-user encryption
        self.__key = randint(32, 79)

        # storing the file folder and the file name where the accounts will be saved
        self.file_folder = file_folder
        self.file_name = file_name
        self.file_loc = os.path.join(file_folder, file_name)
        self.logs = os.path.join(file_folder, logs_file) # logs file

        # colored messages to be printed in the console
        self.error = 'ERROR:  '
        self.program = 'PROGRAM:  '

        # if the logs files does not exist
        if not os.path.exists(self.logs):
            os.mkdir(self.file_folder)
            with open(self.logs, 'w') as file:
                print(f'[{datetime.now()}]\nCreated Log File.\n', file=file)

        # if the user is in offline storage
        if not self.__online_storage:
            # if the file folder is not created, create one
            if not os.path.exists(self.file_folder):
                self.__save_logs(f'Created file folder {self.file_folder}')
                os.mkdir(self.file_folder)

            # if the file itself is not created, create one
            if not os.path.exists(self.file_loc):
                with open(self.file_loc, 'w') as file:
                    self.__save_logs(f'Created accounts file {self.file_name}') 
                    # stores the encryption key which is generated for this file
                    json.dump({"key": chr(self.__key)}, file)

        # if the user chose online storage
        else:
            # viewing database
            data = self.__view_database()

            # if null data isnot received
            if data != None:
                # if USERS key is not present
                if not 'USERS' in data.keys():
                    self.__create_database('USERS')

                # if KEY db is not present
                if not 'KEY' in data.keys():
                    self.__create_database('KEY')
                    self.__add_to_database('KEY', 'E', 'key')

        # loading the file into the accounts dict
        self.__load_file()

    # private function to update the logs
    def __save_logs(self, message):
        # opening the logs file in append mode
        with open(self.logs, 'a') as file:
            print(f'[{datetime.now()}]\n{message}\n', file=file)
    
    # private function to load the file into the accounts dict
    def __load_file(self):
        if not self.__online_storage:
            # opening the file and updating the accounts dict
            with open(self.file_loc, 'r') as file:
                self.__accounts = json.load(file)

            self.__key = ord(self.__accounts['key'])

        else:
            data = self.__view_database()

            if data != None:
                self.__accounts = data['USERS']
                self.__key = ord(data['KEY']['key'])

    # private function to update the file from the accounts dict
    def __save_file(self):
        if self.__online_storage:
            return

        # converting json to string in a human-friendly format
        accounts_str = pprint.pformat(self.__accounts, compact=True, indent=4).replace('\'', '\"')

        # opening the file, clearing the entire file and dumping the dict into the file
        with open(self.file_loc, 'w') as file:
            file.truncate()
            print(accounts_str, file=file)

    # private function to view the database
    def __view_database(self):
        url = self.__api + '/view'

        # recieving the response
        response = requests.get(url)

        # if the response returns an error
        if not response.status_code in [200, 201]:
            sleeping_print(f'{self.error}Could not load the database.')
            return None

        # converting the entire database into json
        data = json.loads(response.text)

        return data

    # private function to create a database
    def __create_database(self, database):
        url = self.__api + f'/create_database?name={database}'

        # POSTing a request to the db to create a database
        response = requests.post(url)

        # if the API responds with an error
        if not response.status_code in [200, 201]:
            sleeping_print(f'{self.error}Could not create the {database} database.')

    # private function to add data to an existing database
    def __add_to_database(self, database, data, key):
        url = self.__api + f'/add_to_database/{database}?key={key}'

        # POSTing a request to the API with the given data
        response = requests.post(url, json=data)

        # if the API responds with an error
        if not response.status_code in [200, 201]:
            sleeping_print(f'{self.error}Could not add {key} to {database} database.')

    # private function to delete data from a database
    def __delete_from_database(self, database, key):
        url = self.__api + f'/delete_from_database/{database}/{key}'

        # DELETE request sent to database
        response = requests.delete(url)

        # if the response is an error
        if not response.status_code in [200, 201]:
            sleeping_print(f'{self.error} Could not remove {key} from {database} database')
        
    # private function which returns the password of a given user
    def __get_password(self, name: str):
        return self.__accounts[name]
    
    # function which returns the currently logged user
    def get_current_user(self):
        return self.__current_user
    
    # function which returns whether the user is logged in
    def is_logged_in(self):
        return self.__logged_in
    
    # private function which encrypts the given password
    def __encrypt_password(self, password):
        encrypted = ''

        # iterating through the password
        for ch in password:
            # for each character, it is first converted to its ascii value, then
            # the ascii value is multiplied with the key and the result is added to the string
            # this is how this simple encryption works
            encrypted += str(ord(ch) * self.__key)

        return encrypted

    # private function which decrypts the encrypted password
    def __decrypt_password(self, password):
        # dividing the string into four-digit substrings in a list
        listed_text = [password[i : i + 4] for i in range(0, len(password), 4)]

        # every value in the list is divided by the key to obtain the original ascii values
        listed_text = [int(int(i) / self.__key) for i in listed_text]

        # each value is converted to its character form
        listed_text = [chr(i) for i in listed_text]

        # concatenating all values, resulting in the decryption
        return ''.join(listed_text)

    # private function to verify that if a user-entered password is appropriate or not
    def __verified_password(self, password):
        if password == '':
            print(f'{self.error}Password is empty.\n')
            return False
        
        # if the password contains whitespaces
        if ' ' in password:
            print(f'{self.error}Detected whitespaces in password.\n')
            return False
        
        # iterating through the password
        for ch in password:
            # ascii value of the character
            ascii_value = ord(ch)

            # if the ascii value is not applicable to be a good password
            if ascii_value < 33 or ascii_value > 126:
                print(f'{self.error}{ch} is an invalid character.\n')
                return False
            
        # checking the strength of the password
        self.__check_password_strength(password)

        # returns True if all the conditions are met
        return True

    # function to check the strength of a password
    def __check_password_strength(self, password):
        strength = 'Bad' # Bad, Weak, Good, Strong

        # if the password has 8 or more characters
        if len(password) >= 8:
            strength = 'Weak'

        has_lowercase = has_uppercase = False

        # iterating through the password
        for ch in password:
            # ascii value of character
            ascii_value = ord(ch)

            # if the character is lowercase
            if 97 <= ascii_value <= 122:
                has_lowercase = True

            # if the character is uppercase
            elif 65 <= ascii_value <= 90:
                has_uppercase = True

            # if the password contains characters of both cases and the strength is Weak
            if has_uppercase and has_lowercase and strength == 'Weak':
                strength = 'Good'
                break

        # stores a list of special characters
        special_chars = '%!@#$^&*(){}[];:\'\"<>.,?+-*/=-_~`'
        
        # iterating through the password and finding if it has special characters or not
        # if it has special characters, then the variable is set to True, else it becomes false
        has_special_chars = [True if ch in special_chars else False for ch in password].count(True) > 0

        # if the password has special characters and the strength is 'Good'
        if has_special_chars and strength == 'Good':
            strength = 'Strong'

        # printing the password strength
        print(end=f'\n{self.program}Your password is ')
        print(strength + '.')

        # if the password is not strong
        if strength != 'Strong':
            sleeping_print(f'Use an insecure password at your own risk.')


    # function to register accounts
    def register(self):
        # if the terminal is allowed to clean
        if self.clear_terminal: clear()

        print('REGISTRATION PAGE\n')
        name = password = ''

        # loop running until user provides valid response
        while True:
            # username input
            name = input('Enter your username: ')

            # if there is already an account with the given username or name is empty
            if name in self.__accounts or name == '':
                print(f'{self.error}This account already exists.\n')
                self.__save_logs('Failed Register attempt since account name already exists.')
                continue

            break
        
        # loop running until user provides valid response
        while True:
            # getting the password
            password = getpass('Enter your password: ')

            # if the password is not verified
            if not self.__verified_password(password):
                self.__save_logs('Failed Register attempt since password is invalid.')
                continue
            
            break

        # creating new account, logging in the user and updating the current user
        self.__accounts[name] = self.__encrypt_password(password)

        if self.__online_storage:
            self.__add_to_database('USERS', self.__accounts[name], name)

        self.__current_user = name
        self.__logged_in = True

        # updating the file
        self.__save_file()

        # updating logs
        self.__save_logs(f'Account registered: {name}')

        sleeping_print(f'\n{self.program}Successfully registered your account.')

    # function to log in to an existing account
    def login(self):
        # if the terminal is allowed to clean
        if self.clear_terminal: clear()

        print('LOGIN PAGE\n')

        name = password = ''

        # loop running until user provides valid response
        while True:
            # username input
            name = input('Enter your username: ')

            # if the name is empty or the name is the encryption key or the name is not logged in already
            if not name in self.__accounts or name == '' or name == 'key':
                print(f'{self.error}Account with specified name does not exist.\n')
                self.__save_logs('Failed Login attempt since account does not exists.')
                continue
            
            break

        # stores the account password
        acc_password = self.__get_password(name)

        # number of tries until user is timed out
        tries = self.timeout_tries

        # loop running until user provides valid response
        while True:
            # if the user runs out of tries
            if tries == 0:
                self.__save_logs(f'Failed Login attempt since account timed out ({name}).')
                sleeping_print(
                    f'\n{self.program}You have been timed out for {self.timeout_duration} seconds.',
                    duration=self.timeout_duration
                )
                tries = self.timeout_tries
            
            # password input
            password = getpass('Enter your password: ')

            # if the input password is equal to the original account password
            if password == self.__decrypt_password(acc_password):
                self.__logged_in = True
                self.__current_user = name
                sleeping_print(f'\n{self.program}Successfully logged in.')

                # updating logs
                self.__save_logs(f'Account logged in: {name}')
                break

            # if wrong password is given
            self.__save_logs(f'Failed Login attempt since wrong password provided ({name}).')
            print(f'{self.error}Incorrect Password.\n')
            tries -= 1

    # function to change the username of the currently logged user
    def change_username(self):
        # if the terminal is allowed to clean
        if self.clear_terminal: clear()
        
        print('CHANGE USERNAME PAGE\n')

        # if the user is not logged in
        if not self.is_logged_in():
            self.__save_logs('Failed Username Change attempt since no one is logged in.')
            sleeping_print(f'{self.error}User is not logged in.\n')
            return
        
        old_password = new_username = ''

        # stores the account password
        acc_password = self.__get_password(self.__current_user)

        # number of tries until user is timed out
        tries = self.timeout_tries

        # loop running until user provides valid response
        while True:
            # if the user runs out of tries
            if tries == 0:
                self.__save_logs(f'Failed Username Change attempt since account timed out ({self.__current_user}).')
                sleeping_print(
                    f'\n{self.program}You have been timed out for {self.timeout_duration} seconds.',
                    duration=self.timeout_duration
                )
                tries = self.timeout_tries
            
            # old password as user input
            old_password = getpass('Enter your old password: ')

            # if the old password is given wrong
            if old_password != self.__decrypt_password(acc_password):
                self.__save_logs(f'Failed Username Change attempt since wrong password entered ({self.__current_user}).')
                print(f'{self.error}Wrong password entered.\n')
                tries -= 1
                continue

            break

        # loop running until user provides valid response
        while True:
            # new username input
            new_username = input('Enter your new username: ')

            # if no username is provided
            if new_username == '':
                self.__save_logs(f'Failed Username Change attempt since new name is blank ({self.__current_user}).')
                print(f'{self.error}Invalid username provided.\n')
                continue

            # if the new username is already defined
            if new_username in self.__accounts.keys():
                self.__save_logs(f'Failed Username Change attempt since new name already exists ({self.__current_user}).')
                print(f'{self.error}This username already exists.\n')
                continue
            
            break
        
        # updating logs
        self.__save_logs(f'Account changed name: {self.__current_user} ---> {new_username}')

        if self.__online_storage:
            self.__add_to_database('USERS', self.__get_password(self.__current_user), new_username)
            self.__delete_from_database('USERS', self.__current_user)

        # setting the password for the new user, deleting the old user and changing the current user
        self.__accounts[new_username] = self.__get_password(self.__current_user)
        self.__accounts.pop(self.__current_user)
        self.__current_user = new_username

        # updating the file
        self.__save_file()

        sleeping_print(f'\n{self.program}Successfully changed your username.')

    # function to change password of the user's account
    def change_password(self):
        # if the terminal is allowed to clean
        if self.clear_terminal: clear()
        
        print('CHANGE PASSWORD PAGE\n')

        # if the user is not logged in
        if not self.is_logged_in():
            self.__save_logs('Failed Password Change attempt since no one is logged in.')
            sleeping_print(f'{self.error}User is not logged in.\n')
            return

        old_password = new_password = ''

        # stores the account password
        acc_password = self.__get_password(self.__current_user)

        # number of tries until user is timed out
        tries = self.timeout_tries

        # loop running until user provides valid response
        while True:
            # if the user runs out of tries
            if tries == 0:
                self.__save_logs(f'Failed Password Change attempt since account timed out ({self.__current_user}).')
                sleeping_print(
                    f'\n{self.program}You have been timed out for {self.timeout_duration} seconds.',
                    duration=self.timeout_duration
                )
                tries = self.timeout_tries
            
            # old password as user input
            old_password = getpass('Enter your old password: ')

            # if the old password is given wrong
            if old_password != self.__decrypt_password(acc_password):
                self.__save_logs(f'Failed Password Change attempt since wrong password entered ({self.__current_user}).')
                print(f'{self.error}Wrong password entered.\n')
                tries -= 1
                continue
            
            break

        # loop running until user provides valid response
        while True:
            # getting the new password for the user
            new_password = getpass('Enter your new password: ')

            # if the new password is not verified
            if not self.__verified_password(new_password):
                self.__save_logs(f'Failed Password Change attempt since invalid password ({self.__current_user}).')
                continue

            break

        encrypted_pass = self.__encrypt_password(new_password)

        if self.__online_storage:
            self.__delete_from_database('USERS', self.__current_user)
            self.__add_to_database('USERS', encrypted_pass, self.__current_user)

        # storing the new password
        self.__accounts[self.__current_user] = encrypted_pass

        # updating the file
        self.__save_file()

        # updating logs
        self.__save_logs(f'Account changed password: {self.__current_user}')

        sleeping_print(f'\n{self.program}Successfully changed your password.')

    # logging out of existing account
    def logout(self):
        # if the terminal is allowed to clean
        if self.clear_terminal: clear()
        
        print('LOGOUT PAGE\n')

        # if the user is not logged in
        if not self.is_logged_in():
            self.__save_logs('Failed Logout attempt since no one is logged in.')
            sleeping_print(f'{self.error}User is not logged in.\n')
            return

        # verifying if the user is sure about their decision
        surety = input('Are you sure you want to log out? (y/n): ') == 'y'

        # if the user is unsure
        if not surety:
            self.__save_logs(f'Failed Logout attempt since user is unsure ({self.__current_user}).')
            sleeping_print(f'\n{self.program}Aborting your choice.')
            return
        
        # updating logs
        self.__save_logs(f'Account logged out: {self.__current_user}')

        # logging out and changing the current_user to empty
        self.__logged_in = False
        self.__current_user = ''

        sleeping_print(f'\n{self.program}Successfully logged out of your account.')

    # function to delete user accounts
    def delete_account(self):
        # if the terminal is allowed to clean
        if self.clear_terminal: clear()
        
        print('ACCOUNT DELETION PAGE\n')

        # if the user is not logged in
        if not self.is_logged_in():
            self.__save_logs('Failed Delete Account attempt since user is not logged in.')
            sleeping_print(f'{self.error}User is not logged in.\n')
            return

        # retrieving the actual password of the user
        acc_password = self.__get_password(self.__current_user)

        # number of tries until user is timed out
        tries = self.timeout_tries

        # loop running until user provides valid response
        while True:
            # if the user runs out of choice
            if tries == 0:
                self.__save_logs(f'Failed Delete Account attempt since account ran out of tries ({self.__current_user}).')
                sleeping_print(
                    f'\n{self.program}You have been timed out for {self.timeout_duration} seconds.',
                    duration=self.timeout_duration
                )
                tries = self.timeout_tries

            # accepting user password
            password = getpass('Enter your password to verify your choice: ')

            # if input password is not the same as account password
            if not password == self.__decrypt_password(acc_password):
                self.__save_logs(f'Failed Delete Account attempt since wrong password entered ({self.__current_user}).')
                print(f'{self.error}Wrong password entered.\n')
                tries -= 1
                continue

            break
        
        # updating logs
        self.__save_logs(f'Account deleted: {self.__current_user}')

        if self.__online_storage:
            self.__delete_from_database('USERS', self.__current_user)

        # removing the account from the 'accounts' dict, and logging out the user
        self.__accounts.pop(self.__current_user)
        self.__logged_in = False
        self.__current_user = ''

        # updating the file
        self.__save_file()

        sleeping_print(f'\n{self.program}Successfully deleted your account.')



# main function of the program
def main():
    # creating object
    login_security = LoginSecurity(online_storage=True)

    # running until user stops
    while True:
        clear()

        # if the user isnt logged in
        if not login_security.is_logged_in():
            print('Choose any of the following options: ')
            print('1. Register\n2. Login\n3. Exit\n')
            choice = input('>> ')

            match choice:
                case '1':
                    login_security.register()

                case '2':
                    login_security.login()

                case '3':
                    break

                case _:
                    pass

        # if the user is logged in
        else:
            print(f'Welcome {login_security.get_current_user()}!\nChoose any of the following options: ')
            print('1. Change username\n2. Change password\n3. Logout\n4. Delete Account\n5. Exit\n')
            choice = input('>> ')

            match choice:
                case '1':
                    login_security.change_username()

                case '2':
                    login_security.change_password()

                case '3':
                    login_security.logout()

                case '4':
                    login_security.delete_account()

                case '5':
                    break

                case _:
                    pass

# running the program
if __name__ == '__main__':
    main()
