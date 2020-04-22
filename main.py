import string, os, sys, hashlib, base64, time, random

# Variables to be declared at the start of the program when it runs for some default values
user_access_granted = False
can_log_in = False

# Uses world grade MD5 encryption to encrypt data througout the program
def encrypt(item_to_encrypt):
    for i in range(8):
        item_to_encrypt = hashlib.md5(item_to_encrypt.encode())
        item_to_encrypt = str(item_to_encrypt.hexdigest())
    return str(item_to_encrypt)


def register_func():
    # These two lines outside of the with is to create the file "accounts.txt" if it doesnt exist
    f_register = open('accounts.txt','a+')
    f_register.close()
    with open('accounts.txt','r+') as f_register:
        print('    Please enter information below:\n')
        print('    Your username must: \n    - only contain lower case letters and numbers\n    - no special characters allowed\n    - longer than 8 (eight) digits\n')

        while True:
            login = str(input('    Enter your username here >> ')).lower()
            if encrypt(login) in f_register.read():
                print('\n    There is already an account with this username!\n    Please login with it or make an account with a different username!')
            elif len(login) < 8:
                print(f'\n    Your username is not long enough, it must be atleast 8 (eight) digits long, you have only entered {len(login)} digits')
            elif login.isalnum():
                break
            else:
                print('\n    Your username must only contain letters and numbers')

        while True:  
            password = str(input('    Enter your password here >> '))
            confirm_password = str(input('    Confirm your password here >> '))
            if password == confirm_password:
                break
            else:
                print('    Your entered password do not match! Please enter it correctly\n')

        for i in range(8): # this encrypts the password through a md5 encryption cycle as much times as entered in the range()
            password = hashlib.md5(password.encode())
            password = str(password.hexdigest())

        f_register.write(f'{encrypt(login)}:{password}\n')
        print('\n    ==================================================\n    Checking for ./users folder...')
        if os.path.isdir('./users'):
            print('    Directory exists!')
        else:
            print('    Creating directory...')
            os.mkdir('./users')
            print('    Finished creating directory')
        print('    Checking if there are already files for current account...')
        if os.path.isfile(f'./users/{encrypt(login)}'):
            print('    Account already exists in file directories!')
        else:
            print('    Creating files for current user!')
            acc_f = open(f'./users/{encrypt(login)}','a+')
            if os.path.isfile(f'./users/{encrypt(login)}'):
                print('\n    Succesfully created')
            else:
                print('\n    FATAL ERROR: Failed to create file, this problem should not exist, but it just happened, so ah... idk help yourself')
            acc_f.close()
        print('    ==================================================\n')
        f_register.close()



def login_func():
    # Username Part of login below
    save_login_details_hashed = []
    while True:
        with open('accounts.txt','r') as f_login_files:
            if len(save_login_details_hashed) == 0:
                print('\n    Enter your login details below:')
                login_username = str(input('    Username >> ')).lower()
            
                if len(save_login_details_hashed) == 0:
                    for lines in f_login_files:
                        if lines.startswith(f'{encrypt(login_username)}'):
                            print('\n    User Found, please continue:')
                            save_login_details_hashed.append(lines)

                if len(save_login_details_hashed) == 0:
                    print('\n    Unable to find username')
            else:
                break

    # Password Part of login below
    while True:
        with open('accounts.txt','r') as f_login_files:
            login_password = str(input('    Password >> '))
            extracted_password = str(save_login_details_hashed[0].split(':')[1].rstrip('\n'))

            print(extracted_password)
            print(encrypt(login_password))

            if encrypt(login_password) == extracted_password:
                can_log_in = True
                f_login_files.close()
                break
            else:
                print('\n    The password you have entered does not match the one we have in our data base\n    Plase enter try again')
    
    if can_log_in == True:
        user_access_granted = True
        print('\n    You have been successfully logged in!')
    else:
        print('\n    FATAL ERROR: Login Unsucess')



def menu():
    menu_text = """
                   Welcome to the BeeWang Password Manager

    ========================= Available Options =========================

                      1.  Registering an account
                      2.  Logging in to an account


  
    =====================================================================

        (Please select an option by entering the corresponding number)

    """
    while True:
        print(menu_text)
        menu_choice = input('    Plase Enter number here >> ')
        if menu_choice == '1':
            register_func()
        elif menu_choice == '2':
            login_func()
        else:
            print('    \nThere is no such option avaliable, please enter again!\n')



try:
    menu()
except KeyboardInterrupt:
    print('\n    User Closed Program')